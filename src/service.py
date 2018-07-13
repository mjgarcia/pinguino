import re
import mail
from message import Message
import logging

logger = logging.getLogger(__name__)
subject_pattern = re.compile(r'\[(.*)\] Task (\d+) of the Eudyptula Challenge')

def run():

    messages_ids = mail.get_unread_messages_ids()

    logger.info('Got %s messages', len(messages_ids))

    for id in messages_ids:

        logger.info('Working on message with id %s', id)

        message = Message(id['id'])

        message.fetch()

        if not message.is_valid_type:
            logger.info('Invalid message type with id %s.', message.id)
            #TODO: Send response.
            continue

        matches = subject_pattern.match(message.subject)

        if not matches or len(matches.groups()) != 2:
            logger.info('Unable to parse subject %s.', message.subject)
            #TODO: Send response.
            continue

        user_id = matches.group(1)
        task = matches.group(2)
