import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tasks import task_common

def test_extract_attachments():

    task_common.extract_attachments()