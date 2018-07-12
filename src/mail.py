from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import logging
import secrets

logger = logging.getLogger(__name__)

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

store = file.Storage(secrets.GMAIL_CREDENTIALS_STORE)
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(secrets.GMAIL_SECRETS_FILE, SCOPES)
    creds = tools.run_flow(flow, store)

service = build('gmail', 'v1', http=creds.authorize(Http()))

user_id = 'me'
label_inbox = 'INBOX'
label_unread = 'UNREAD'

def get_unread_messages_ids():

    unread_messages = service.users().messages().list(userId=user_id, labelIds=[label_inbox, label_unread]).execute()

    if unread_messages['resultSizeEstimate'] == 0:
        logger.info('No new messages found. Returning empty list.')
        return []

    messages_list = unread_messages['messages']

    logger.info('Got %s unread message ids', len(messages_list))

    return messages_list

def get_message_from_payload(payload):

    message = {}

    headers = payload['headers']

    message['From'] = next(h['value'] for h in headers if h['name'] == 'From')
    message['Subject'] = next(h['value'] for h in headers if h['name'] == 'Subject')
    message['Date'] = next(h['value'] for h in headers if h['name'] == 'Date')

    message['contents'] = get_message_contents_from_payload(payload)

    return message

def decode_message_body_from_payload(payload):

    base64_body = payload['body']['data']

    if base64_body != None:

        # Replace the following characters to have a valid base64 string
        base64_body = base64_body.replace('-','+')
        base64_body = base64_body.replace('_','/')

        return base64.b64decode(base64_body)

def is_message_part_the_body(part):

    return (not part['filename']) and (part['mimeType'] == 'text/plain')

def get_message_body_from_parts(parts):

    for part in parts:
        if is_message_part_the_body(part):
            return decode_message_body_from_payload(part)

def get_attachment_from_id(attachment_id):

    attachment = service.users().messages().attachments.get(userId=user_id, messageId=message_id, id=attachment_id).execute()

    return attachment

def get_message_attachments_from_parts(parts):

    attachments = []

    for part in parts:

        if part['filename']:
            attachment = {}
            attachment['filename'] = part['filename']
            attachment_id = part['body']['attachmentId']
            attachment_data = get_attachment_from_id(attachment_id)
            attachments.append(attachment)

    return attachments

def get_message_contents_from_parts(parts):

    contents = {}
    contents['Body'] = get_message_body_from_parts(parts)
    contents['Attachements'] = get_message_attachments_from_parts(parts)

    return contents

def get_message_contents_from_payload(payload):

    if payload['mimeType'] == 'text/plain':

        contents = {}
        contents['Body'] = decode_message_body_from_payload(payload)

    elif payload['mimeType'] == 'multipart/mixed':

        contents = get_message_contents_from_parts(payload['parts'])

    return contents

def get_message_from_id(message_id):

    logger.info('Getting message with id %s', message_id)

    message = service.users().messages().get(userId=user_id, id=message_id).execute()
    payload = message['payload']

    message = get_message_from_payload(payload)

    return message