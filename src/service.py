
import mail
import logging

logger = logging.getLogger(__name__)

def run():

    unread_messages = mail.get_unread_messages()

    logger.info('Got %s messages', len(unread_messages))