import logging
import sys


def configure_logging(level: str = "INFO") -> None:
    """Structured-enough logging for local dev and for reading in hosting-provider logs."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s :: %(message)s",
        stream=sys.stdout,
    )
