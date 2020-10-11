import re

from .base import ApiKambi


class Api888Sport(ApiKambi):
    """ The ApiKambi implementation for 888sport.com """

    def __init__(self):
        self.name = '888sport'
        self.base_url = (
            'https://eu-offering.kambicdn.org/'
            'offering/v2018/888/listView/football'
        )
        self.parsers = [
            self._full_time_result,
            self._both_teams_to_score,
            self._double_chance,
        ]

    def competition(self, url: str) -> str:
        re_888sport = re.compile(
            r'https?://www\.888sport\.\w{2,3}/'
            r'#/filter/football/[0-9a-zA-Z/]+/?'
        )
        if re_888sport.match(url):
            return '/'.join(url.split('/')[6:8])
        else:
            msg = f'Cannot parse {url}'
            raise ValueError(msg)
