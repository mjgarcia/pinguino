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

def get_message_from_id(message_id):

    logger.info('Getting message with id %s', message_id)

    message = service.users().messages().get(userId=user_id, id=message_id).execute()

    return message

def get_attachment_from_id(message_id, attachment_id):

    logger.info('Getting attachment with id %s', attachment_id)

    attachment = service.users().messages().attachments.get(userId=user_id, messageId=message_id, id=attachment_id).execute()

    return attachment