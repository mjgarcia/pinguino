import os
from exception import InvalidMessageException

SANDBOX_FOLDER = '/etc/pinguino/sandbox'

def create_sandbox_folder(id):

    full_path = os.path.join(SANDBOX_FOLDER, id)

    if not os.path.exists(full_path):
        os.makedirs(full_path)

    return full_path

def create_file(filename, contents):

    with open(filename,"w+") as f:
        f.write(contents)

def extract_attachments(attachments_required, message):

    sandbox_folder = create_sandbox_folder(message.id)

    for attachment in attachments_required:

        attachment_data = message.attachments[attachment]
        attachment_path = os.path.join(sandbox_folder, attachment)
        create_file(attachment_path, attachment_data)

    return sandbox_folder

def validate_attachments(attachments_required, message_attachments):

    if not message_attachments or len(message_attachments) != len(attachments_required):
        raise InvalidMessageException('Invalid message attachments')

    missing_attachments = []

    for attachment in attachments_required:
        if not attachment in message_attachments:
            missing_attachments.append(attachment)

    if missing_attachments:
        joined = ", ".join(missing_attachments)
        raise InvalidMessageException('Missing attachment(s) {}'.format(joined))

def compile(sandbox_folder):

    pass