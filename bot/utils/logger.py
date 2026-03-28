import logging, sys
from pythonjsonlogger import jsonlogger
from config import settings
def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.log_level))
    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s', timestamp=True)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger