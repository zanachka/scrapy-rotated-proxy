import base64
from six.moves.urllib.parse import unquote
from scrapy.utils.python import to_bytes

import six


def _basic_auth_header(username, password, auth_encoding=None):
    if six.PY2:
        username = username.encode(self.auth_encoding)
        password = password.encode(self.auth_encoding)
    user_pass = to_bytes(
        '{username}:{password}'.format(username=unquote(username), password=unquote(password)),
        encoding=auth_encoding
    )
    return base64.b64encode(user_pass).strip()


if __name__ == '__main__':
    pass
