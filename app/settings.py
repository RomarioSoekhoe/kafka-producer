import os
from enum import Enum
from typing import Optional

from pydantic import validator
from pydantic_settings import BaseSettings


class LogLevelEnum(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Settings(BaseSettings):
    debug: bool = os.environ.get("DEBUG", False)    # When True, log_level will be DEBUG and filename and rulenumber in logging
    log_level: Optional[LogLevelEnum] = os.environ.get("LOG_LEVEL", None)   # Defaults to INFO if DEBUG = False

    kafka_bootstrap_servers: str = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "confluent-local-broker-1:40923")
    json_data_path: str = os.environ.get("JSON_DATA_PATH", "/data")
    avsc_data_path: str = os.environ.get("AVSC_DATA_PATH", "/schemas")

    @validator("log_level", pre=True, always=True)
    def validate_log_level(cls, value):
        if value is None:
            return LogLevelEnum.INFO
        return value
