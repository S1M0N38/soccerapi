import re
from typing import Dict, Tuple

import requests

from .base import ApiBase
from .kambi import ParserKambi as ParserUnibet


class ApiUnibet(ApiBase, ParserUnibet):
    """ The ApiKambi implementation for unibet.com """

    def __init__(self):
        self.name = 'unibet'
        self.session = requests.Session()

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

    def requests(self, competition: str) -> Tuple[Dict]:
        return {
            'full_time_result': self._request(competition, 12579),
            'both_teams_to_score': self._request(competition, 11942),
            'double_chance': self._request(competition, 12220),
        }

    # Parsers (implemented in ApiKambi)

    # Auxiliary methods

    def _request(
        self, competition: str, category: int, market: str = 'IT'
    ) -> Dict:
        """ Make the single request using the active session """

        base_url = (
            'https://eu-offering.kambicdn.org/'
            'offering/v2018/ub/listView/football'
        )
        url = '/'.join([base_url, competition]) + '.json'
        params = (
            ('lang', 'en_US'),
            ('market', market),
            ('category', category),
        )
        return self.session.get(url, params=params).json()
