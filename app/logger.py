import logging
import sys
from pathlib import Path
from settings import Settings

settings = Settings()

log_level_mapping = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}


def setup_logger() -> None:
    # When debug is True show filename and rule number in logging rule
    format_template = "%s[%%(levelname)s] %%(message)s" % ("%s::%%(lineno)d " % "%(filename)s" if settings.debug else "")
    log = Path(__file__).parent.parent / "log" / "log"
    log.parent.mkdir(parents=True, exist_ok=True)   # Directory should exist before writing a log file.
    log.touch(mode=0o777)  # Set read/write permission on all users.

    log_level = log_level_mapping.get(settings.log_level, logging.INFO)

    logging.basicConfig(
        filename=log,
        encoding="utf-8",
        level=logging.DEBUG if settings.debug else log_level,
        filemode="w",
        format='%(asctime)s '+format_template,
        datefmt="%Y-%m-%d %H:%M",  # Set the timestamp format
    )

    # Add logging handler which redirects to stdout.
    logger = logging.getLogger()
    formatter = logging.Formatter(format_template)

    # Add the console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG if settings.debug else log_level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
