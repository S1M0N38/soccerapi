import re
from typing import Dict, Tuple

import requests

from .base import ApiBase
from .kambi import ParserKambi as Parser888Sport


class Api888Sport(ApiBase, Parser888Sport):
    """ The ApiKambi implementation for 888sport.com """

    def __init__(self):
        self.name = '888sport'
        self.session = requests.Session()

    def url_to_competition(self, url: str) -> str:
        re_888sport = re.compile(
            r'https?://www\.888sport\.\w{2,3}/'
            r'#/filter/football/[0-9a-zA-Z/]+/?'
        )
        if re_888sport.match(url):
            return '/'.join(url.split('/')[6:8])
        else:
            msg = f'Cannot parse {url}'
            raise ValueError(msg)

    def competitions(
        self,
        base_url='https://www.888sport.com/#/filter/football/',
        market='IT',
    ) -> Dict:
        url = 'https://eu-offering.kambicdn.org/offering/v2018/888/group.json'
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
            'offering/v2018/888/listView/football'
        )
        url = '/'.join([base_url, competition]) + '.json'
        params = (
            ('lang', 'en_US'),
            ('market', market),
            ('category', category),
        )
        return self.session.get(url, params=params).json()
