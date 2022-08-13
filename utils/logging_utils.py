from loguru import logger


class LoggingUtils:
    @staticmethod
    def log(message: str) -> None:
        logger.log("INFO", message, colorize=True)

    @staticmethod
    def exception(exc: Exception) -> None:
        logger.exception("ERROR", exc, colorize=True)
