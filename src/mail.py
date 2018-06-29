from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
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

    for h in headers:

        name = h['name']
        value = h['value']

        if name == 'From':
            message['From'] = value
        elif name == 'Subject':
            message['Subject'] = value
        elif name == 'Date':
            message['Date'] = value

    return message

def get_message_from_id(message_id):

    message = service.users().messages().get(userId=user_id, id=message_id).execute()
    payload = message['payload']
    headers = payload['headers']

    message = get_message_from_headers(headers)

    return message

def get_unread_messages():

    messages_ids = get_unread_messages_ids()

    all_messages = []

    for id in messages_ids:

        message = get_message_from_id(id['id'])

        all_messages.append(message)

    return all_messages





