
import mail
from message import Message
import logging

logger = logging.getLogger(__name__)

def run():

    messages_ids = mail.get_unread_messages_ids()

    logger.info('Got %s messages', len(messages_ids))

    for id in messages_ids:

        logger.info('Working on message with id %s', id)

        message = Message(id['id'])

        message.fetch()
