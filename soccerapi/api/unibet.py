import re

from .base import ApiKambi


class ApiUnibet(ApiKambi):
    """ The ApiBase implementation for unibet.com """

    def __init__(self):
        self.name = 'unibet'
        self.base_url = (
            'https://eu-offering.kambicdn.org/'
            'offering/v2018/ub/listView/football'
        )
        self.parsers = [
            self._full_time_result,
            self._both_teams_to_score,
            self._double_chance,
        ]

    def competition(self, url: str) -> str:
        re_unibet = re.compile(
            r'https?://www\.unibet\.\w{2,3}/'
            'betting/sports/filter/[0-9a-zA-Z/]+/(?:matches)?/?'
        )
        if re_unibet.match(url):
            return '/'.join(url.split('/')[7:9])
        else:
            msg = f'Cannot parse {url}'
            raise ValueError(msg)
