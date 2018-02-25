'''Rest4 settings

Settings for Rest4
'''


BATCH_FUNCTION_KEYWORDS = ("options", "list", "create", "extras", "batch")
FUNCTION_METHODS_MAP = {
    'options': 'OPTION',
    'list': 'GET',
    'create': 'POST',
    'extras': 'PUT',
    'option': 'OPTION',
    'get': 'GET',
    'update': 'PUT',
    'patch': 'PATCH',
    'delete': 'DELETE',
    'extra': 'POST'
}

DEFAULT_OPTION_RESPONSE_DATA = {"message": "I'm alive."}
DEFAULT_DEBUG_MESSAGE_DATA = {"message": "This is a debug message."}

DEFAULT_HEADERS = {}
CORS_HEADERS_ALLOW_HEADERS = ", ".join(
    ["origin", "accept", "content-type", "authorization"])
CORS_HEADERS_ALLOW_METHODS = ", ".join(
    ["OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"])
CORS_HEADERS_ALLOW_ORIGIN = '*'
CORS_HEADERS_ALLOW_CREDENTIALS = True
CORS_HEADERS_MAX_AGE = 86400

DEFAULT_API_METHODS = ("POST", )
DEFUALT_OPTION_METHODS = ("OPTION", )

ENDPOINT_KEY_NAME = "action"
