import mail
import logging

logger = logging.getLogger(__name__)

class Message:

    def __init__(self, id):

        self.id = id

    def fetch(self):

        message = mail.get_message_from_id(self.id):
        payload = message['payload']

        get_message_from_payload(payload)

    def get_message_from_payload(self, payload):

        headers = payload['headers']

        self.From = next(h['value'] for h in headers if h['name'] == 'From')
        self.Subject = next(h['value'] for h in headers if h['name'] == 'Subject')
        self.Date = next(h['value'] for h in headers if h['name'] == 'Date')

        get_message_contents_from_payload(payload)

        return message

    def get_message_contents_from_payload(self, payload):

        if payload['mimeType'] == 'text/plain':

            self.Body = decode_message_body_from_payload(payload)

        elif payload['mimeType'] == 'multipart/mixed':

            get_message_contents_from_parts(payload['parts'])

    def decode_message_body_from_payload(payload):

        base64_body = payload['body']['data']

        if base64_body != None:

            # Replace the following characters to have a valid base64 string
            base64_body = base64_body.replace('-','+')
            base64_body = base64_body.replace('_','/')

            return base64.b64decode(base64_body)

    def get_message_contents_from_parts(self, parts):

        self.Body = get_message_body_from_parts(parts)
        self.Attachements = get_message_attachments_from_parts(parts)

    def is_message_part_the_body(part):

        return (not part['filename']) and (part['mimeType'] == 'text/plain')

    def get_message_body_from_parts(parts):

        for part in parts:
            if is_message_part_the_body(part):
                return decode_message_body_from_payload(part)

    def get_message_attachments_from_parts(self, parts):

        attachments = []

        for part in parts:

            if part['filename']:
                attachment = {}
                attachment['filename'] = part['filename']
                attachment_id = part['body']['attachmentId']
                attachment_data = mail.get_attachment_from_id(self.id, attachment_id)
                attachments.append(attachment)

        return attachments
