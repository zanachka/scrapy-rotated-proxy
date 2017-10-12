import re
import json
from itertools import cycle
from urllib.parse import urlunparse
from urllib.request import _parse_proxy

from scrapy.utils.misc import load_object

from scrapy_rotated_proxy.extensions import default_settings
from scrapy_rotated_proxy import util


class FileProxyStorage():
    def __init__(self, settings):
        if settings.get('PROXY_FILE_PATH') or getattr(default_settings, 'PROXY_FILE_PATH'):
            file_path = settings.get('PROXY_FILE_PATH', getattr(default_settings, 'PROXY_FILE_PATH'))
            self.settings = json.load(open(file_path))
        else:
            self.settings = settings
        self.auth_encoding = settings.get('HTTPPROXY_AUTH_ENCODING')

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def _get_proxy(self, url, orig_type=''):
        proxy_type, user, password, hostport = _parse_proxy(url)
        proxy_url = urlunparse((proxy_type or orig_type, hostport, '', '', '', ''))

        creds = util._basic_auth_header(user, password, self.auth_encoding) if user else None

        return creds, proxy_url

    def proxies(self):
        pattern = re.compile(r'(?P<scheme>[A-Z]+)_PROXIES')

        def _filter(tuple_):
            m = pattern.match(tuple_[0])
            if m:
                scheme = m.group('scheme').lower()
                return scheme, {self._get_proxy(item, scheme) for item in tuple_[1]}

        proxies = []
        for item in self.settings.items():
            pair = _filter(item)
            if pair:
                proxies.append(pair)
        return dict(proxies)
