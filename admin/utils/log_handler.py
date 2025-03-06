import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import os

class CustomLogRecord(logging.LogRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_module = self.pathname.split(os.path.sep)[-2]  # Parent directory name

def custom_logger_factory(*args, **kwargs):
    return CustomLogRecord(*args, **kwargs)

logging.setLogRecordFactory(custom_logger_factory)

def get_logger():
    logger = logging.getLogger('chetu_project')
    logger.setLevel(logging.DEBUG)  # Log everything from DEBUG and above

    # Define log directory inside the project
    log_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log')
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Rotating log handler (max 10MB per file, keeps 3 backups)
    file_handler = RotatingFileHandler(
        os.path.join(log_directory, 'app.log'),
        maxBytes=10 * 1024 * 1024,  # 10MB per file
        backupCount=3
    )

    # Time-based log rotation (daily)
    time_handler = TimedRotatingFileHandler(
        os.path.join(log_directory, 'app.log'),
        when='midnight',
        interval=1,
        backupCount=7  # Keeps last 7 days' logs
    )

    # Log message format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - [%(custom_module)s] - %(module)s.%(funcName)s() - %(levelname)s - %(message)s'
    )

    file_handler.setFormatter(formatter)
    time_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(time_handler)

    return logger
