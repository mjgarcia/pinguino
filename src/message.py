import mail
import logging
import base64

logger = logging.getLogger(__name__)

def decode_base64_string(base64_string):

    if base64_string != None:

        # Replace the following characters to have a valid base64 string
        base64_string = base64_string.replace('-','+')
        base64_string = base64_string.replace('_','/')

        return base64.b64decode(base64_string)

def is_message_part_the_body(part):

    return (not part['filename']) and (part['mimeType'] == 'text/plain')

def get_message_body_from_parts(parts):

    for part in parts:
        if is_message_part_the_body(part):
            return decode_base64_string(part['body']['data'])

class Message:

    def __init__(self, id):

        self.id = id
        self.is_valid_type = False

    def fetch(self):

        message = mail.get_message_from_id(self.id)
        payload = message['payload']

        self.build_message_from_payload(payload)

    def build_message_from_payload(self, payload):

        headers = payload['headers']

        self.sender = next(h['value'] for h in headers if h['name'] == 'From')
        self.subject = next(h['value'] for h in headers if h['name'] == 'Subject')
        self.date = next(h['value'] for h in headers if h['name'] == 'Date')

        self.build_message_contents_from_payload(payload)

    def build_message_contents_from_payload(self, payload):

        if payload['mimeType'] == 'text/plain':

            self.body = decode_base64_string(payload['body']['data'])
            self.attachments = []
            self.is_valid_type = True

        elif payload['mimeType'] == 'multipart/mixed':

            self.body = get_message_body_from_parts(payload['parts'])
            self.attachments = self.get_message_attachments_from_parts(payload['parts'])
            self.is_valid_type = True

    def get_message_attachments_from_parts(self, parts):

        attachments = {}

        for part in parts:

            if part['filename']:
                attachment_id = part['body']['attachmentId']
                attachment_data = mail.get_attachment_from_id(self.id, attachment_id)
                attachments[part['filename']] = decode_base64_string(attachment_data['data'])

        return attachments
