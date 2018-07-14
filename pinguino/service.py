import re
import mail
from tasks import task
from message import Message
import logging

logger = logging.getLogger(__name__)
subject_pattern = re.compile(r'\[(.*)\] Task (\d+) of the Eudyptula Challenge')

def process_task(message, user_id, task_id):

    if task_id not in task.task_processors:
        logger.info('Invalid task id %s.', task_id)
        #TODO: Send response.
        return

    task_processor = task.task_processors[task_id]

    task_processor.process(message)

def process_message(message):

    if not message.is_valid_type:
        logger.info('Invalid message type with id %s.', message.id)
        #TODO: Send response.
        return

    matches = subject_pattern.match(message.subject)

    if not matches or len(matches.groups()) != 2:
        logger.info('Unable to parse subject %s.', message.subject)
        #TODO: Send response.
        return

    user_id = matches.group(1)
    task_id = matches.group(2)

    process_task(message, user_id, task_id)

def run():

    messages_ids = mail.get_unread_messages_ids()

    logger.info('Got %s messages', len(messages_ids))

    for id in messages_ids:

        logger.info('Working on message with id %s', id)

        message = Message(id['id'])

        message.fetch()

        process_message(message)
