# Test Producer
This project contains code to produce messages on kafka topics. The confluentic local kafka is required.

## Pre-requirements
- confluentic cli has started local kafka instance
    - ./confluent local kafka start
- topics are created:
    - simple-topic
    - simpler-topic
    - user-topic

## Data
Adjust data and topics or schema's to fit your needs.

## Run

```bash
docker-compose up -d
```