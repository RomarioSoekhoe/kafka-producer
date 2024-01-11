import logging
from logger import setup_logger
from settings import Settings
from avro_producer import produce_avro_messages

setup_logger()
logger = logging.getLogger()
settings = Settings()


def main():
    logger.info("Start pushing messages to kafka.")
    produce_avro_messages()
    logger.info("Finished pushing messages...") 


if __name__ == "__main__":
    main()
