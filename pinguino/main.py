import logging
import sys
import service

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

def main():

    logger.info('Starting')

    service.run()

    logger.info('Exiting')


if __name__ == "__main__":
    main()