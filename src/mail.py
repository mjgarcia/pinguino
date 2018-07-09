from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import logging

logger = logging.getLogger(__name__)

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
SECRETS_FILE = 'client_secret.json'
CREDENTIALS_STORE = 'credentials.json'

store = file.Storage(CREDENTIALS_STORE)
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(SECRETS_FILE, SCOPES)
    creds = tools.run_flow(flow, store)

service = build('gmail', 'v1', http=creds.authorize(Http()))

user_id = 'me'
label_inbox = 'INBOX'
label_unread = 'UNREAD'

def get_unread_messages_ids():

    unread_messages = service.users().messages().list(userId=user_id, labelIds=[label_inbox, label_unread]).execute()
    messages_list = unread_messages['messages']

    logger.info('Got %s unread message ids', len(messages_list))

    return messages_list

def get_message_from_headers(headers):

    message = {}

    message['From'] = next(h['value'] for h in headers if h['name'] == 'From')
    message['Subject'] = next(h['value'] for h in headers if h['name'] == 'Subject')
    message['Date'] = next(h['value'] for h in headers if h['name'] == 'Date')

    return message

def get_message_body_from_payload(payload):
    """
    Recursively returns the first payload part that
    has mime type text/plain
    """

    logger.info('Payload has mime type %s', payload['mimeType'])

    if payload['mimeType'] == 'text/plain':

        return payload['body']['data']

    elif 'parts' in payload:

        logger.info('Message has %s parts', len(payload['parts']))

        for part in payload['parts']:
            return get_message_body_from_payload(part)

def decode_message_body_from_payload(payload):

    base64_body = get_message_body_from_payload(payload)

    if base64_body != None:

        # Replace the following characters to have a valid base64 string
        base64_body = base64_body.replace('-','+')
        base64_body = base64_body.replace('_','/')

        return base64.b64decode(base64_body)

    else:
        logger.info('Not found text/plain payload in message')

def get_message_from_id(message_id):

    logger.info('Getting message with id %s', message_id)

    message = service.users().messages().get(userId=user_id, id=message_id).execute()
    payload = message['payload']
    headers = payload['headers']

    message = get_message_from_headers(headers)

    message['body'] = decode_message_body_from_payload(payload)

    return message

def get_unread_messages():

    messages_ids = get_unread_messages_ids()

    all_messages = []

    for id in messages_ids:

        message = get_message_from_id(id['id'])

        all_messages.append(message)

    return all_messages





