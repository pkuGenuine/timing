import logging

def log_exception(logger: logging.Logger, e: Exception):
    logger.error(f'{type(e)}: {str(e)}')
    #TODO: Traceback