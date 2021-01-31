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

    def url_to_competition(self, url: str) -> str:
        re_unibet = re.compile(
            r'https?://www\.unibet\.\w{2,3}/'
            r'betting/sports/filter/[0-9a-zA-Z/]+/(?:matches)?/?'
        )
        if re_unibet.match(url):
            return '/'.join(url.split('/')[7:9])
        else:
            msg = f'Cannot parse {url}'
            raise ValueError(msg)

    def competitions(
        self,
        base_url='https://www.unibet.com/betting/sports/filter/football/',
        market='IT',
    ) -> Dict:
        url = 'https://eu-offering.kambicdn.org/offering/v2018/ub/group.json'
        params = {'lang': 'en_US', 'market': market}
        competitions_to_parse = self.session.get(url, params=params).json()
        return self._parse_competitions(base_url, competitions_to_parse)

    def requests(self, competition: str) -> Tuple[Dict]:
        return {
            'full_time_result': self._request(competition, 12579),
            'under_over': self._request(competition, 12580),
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
