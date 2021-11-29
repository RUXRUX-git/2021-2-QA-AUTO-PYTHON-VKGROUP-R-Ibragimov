import os.path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')

MOCK_LOG_FILE_NAME = 'flask_mock.log'
MOCK_LOG_FILE_PATH = os.path.join(LOG_DIR, MOCK_LOG_FILE_NAME)

REQUESTS_HANDLER_FILE_NAME = 'handler.log'
REQUESTS_HANDLER_FILE_PATH = os.path.join(LOG_DIR, REQUESTS_HANDLER_FILE_NAME)

MOCK_HOST = '127.0.0.1'
MOCK_PORT = 8080

DEFAULT_HTTP_VERSION = 'HTTP/1.1'
