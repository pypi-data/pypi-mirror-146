from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from wintersweet.framework.exception_handlers import http_exception_handler
from wintersweet.framework.middlewares import RequestIDMiddleware

DEBUG = True
SECRET = f'__access_control_{DEBUG}_@5806fecc-93b3-11ec-beda-e2b55ff3da64__'

LISTEN_PORT = 8080

# process
PROCESS_NUM = 2


APP_CONFIG = {
    'debug': DEBUG,
    'routes': [],
}


LOGGING_CONFIG = {
    'level': 'debug',
    'file_path': '',
    'file_rotation': None,
    'file_retention': None,
}

# MIDDLEWARES
MIDDLEWARES = [
    {
        'cls': RequestIDMiddleware,
        'options': {}
    },
    {
        'cls': CORSMiddleware,
        'options': {
            'allow_origins': '*',
            'allow_methods': '*',
            'allow_headers': '*',
            'allow_credentials': True
        }
    },

]

EXCEPTION_HANDLERS = [
    # {
    #     'cls': HTTPException,
    #     'handler': http_exception_handler
    # },
]

DATABASES = {
    # 'default': {
    #     'echo': True,
    #     'host': "localhost",
    #     'user': 'root',
    #     'password': "",
    #     'db': 'test',
    #     'port': 3306,
    #     'charset': r'utf8',
    #     'autocommit': True,
    #     'cursorclass': aiomysql.DictCursor,
    # }
}

REDIS_CONFIG = {
    # 'default': {
    #     'address': "redis://localhost:6379",
    #     'password': None,
    #     'db': 0,
    #     'encoding': 'utf-8',
    #     'minsize': 10
    # }
}