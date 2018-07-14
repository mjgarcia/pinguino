
from exception import InvalidMessageException
import task_common

MAKEFILE = 'Makefile'
MODULE_FILE = 'my_first_module.c'

attachments_required = [MAKEFILE, MODULE_FILE]

def process(message):

    task_common.validate_attachments(attachments_required, message.attachments)

    sandbox_folder = task_common.extract_attachments(attachments_required, message)

    task_common.compile(sandbox_folder)
