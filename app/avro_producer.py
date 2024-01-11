import json
import os
from io import BytesIO
from confluent_kafka import Producer
import fastavro
import logging

from settings import Settings

settings = Settings()
logger = logging.getLogger()

def load_avro_schema(schema_path):
    with open(schema_path, 'rb') as schema_file:
        avro_schema = fastavro.schema.parse_schema(json.load(schema_file))
    return avro_schema


def load_avro_records_from_json(json_file):
    with open(json_file, 'r') as json_data:
        avro_records = json.load(json_data)
    return avro_records


def setup_kafka_producer():
    producer_config = {
        'bootstrap.servers': settings.kafka_bootstrap_servers,
    }
    return Producer(producer_config)


def avro_serialize_and_produce(producer, avro_schema, avro_record, topic_name):
    try:
        # Serialize Avro record
        avro_binary = BytesIO()
        fastavro.schemaless_writer(avro_binary, avro_schema, avro_record)

        # Produce Avro message to the specified topic
        producer.produce(topic=topic_name, key=None, value=avro_binary.getvalue(), callback=delivery_report)

        logger.info(f"Produced message to topic: {topic_name}")

        # Reset the BytesIO buffer for the next record
        avro_binary.seek(0)
        avro_binary.truncate(0)

    except Exception as e:
        logger.error(f"Error producing message to topic {topic_name}: {e}")
        logger.info(f"Problematic record: {avro_record}")


def delivery_report(err, msg):
    if err is not None:
        logger.error("Message delivery failed {}: {}".format(msg.key(), err))
    else:
        logger.info('Record successfully produced to {} [{}] at offset {}'.format(
            msg.topic(), msg.partition(), msg.offset()))


def produce_avro_messages():
    try:
        for file_name in os.listdir(settings.json_data_path):
            if file_name.endswith(".json"):
                topic_name = os.path.splitext(file_name)[0]
                json_file_path = os.path.join(settings.json_data_path, file_name)

                # Load Avro schema for the specified topic
                avro_schema_path = os.path.join(settings.avsc_data_path, f"{topic_name}.avsc")

                if avro_schema_path is None:
                    logger.info(f"Avro schema not found for topic: {topic_name}")
                    continue

                avro_schema = load_avro_schema(avro_schema_path)

                # Load Avro records from JSON
                avro_records_from_json = load_avro_records_from_json(json_file_path)
                logger.debug(f"loaded json records:\n {avro_records_from_json}")
                # Create Kafka Producer
                producer = setup_kafka_producer()
                # Iterate over each record in the array and produce Avro messages
                for avro_record_from_json in avro_records_from_json:
                    # logger.debug(avro_record_from_json)
                    avro_serialize_and_produce(producer, avro_schema, avro_record_from_json, topic_name)

                # Wait for any outstanding messages to be delivered
                producer.flush()
    except Exception as e:
        logger.error(f"Error producing Avro messages: {e}")
