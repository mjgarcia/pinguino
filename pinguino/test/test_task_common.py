import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tasks import task_common
from message import Message

MAKEFILE = 'Makefile'
MODULE_FILE = 'hello_world_module.c'
TEST_RESOURCES_DIR = 'resources'

attachments_required = [MAKEFILE, MODULE_FILE]

def get_test_attachments():
    attachments = {}

    with open(MAKEFILE) as f:
        attachments[MAKEFILE] = f.read()

def test_extract_attachments():

    message = Message("test_message")

    task_common.extract_attachments(attachments_required, message)