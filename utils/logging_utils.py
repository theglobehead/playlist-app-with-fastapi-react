from loguru import logger

from controllers.constants import LOGS_PATH


class LoggingUtils:
    @staticmethod
    def log(message: str) -> None:
        logger.log("INFO", message, colorize=True)
        logger.add(f"{ LOGS_PATH }logs.log", rotation="1 week")

    @staticmethod
    def exception(exc: Exception) -> None:
        logger.exception("ERROR", exc, colorize=True)
        logger.add(f"{ LOGS_PATH }exceptions.log", rotation="1 week")
