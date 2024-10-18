import logging
import logging.config
import os

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s at line %(lineno)d: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.getenv('LOGPATH', '/var/application/log/app.log'), 
            'formatter': 'default',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': os.getenv('LOGLEVEL', "DEBUG"),
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

def get_logger(name):
    return logging.getLogger(name)