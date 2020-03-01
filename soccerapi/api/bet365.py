from typing import Dict, Tuple

import requests

from .base import ApiBase


class ApiBet365(ApiBase):
    def __init__(self):
        self.name = 'bet365'
        self.table = self._read_table()

    @staticmethod
    def _full_time_result():
        # TODO
        ...

    @staticmethod
    def _both_teams_to_score():
        # TODO
        ...

    @staticmethod
    def _double_chance():
        # TODO
        ...

    @staticmethod
    def _under_over():
        # TODO
        ...

    def _request(self, s: requests.Session, league: str, category: int) -> Dict:
        url = 'https://www.bet365.it/SportsBook.API/web'
        params = (
            ('lid', '1'),
            ('zid', '0'),
            ('pd', f'#AC#B1#C1#D{category}#{league}#F2#'),
            ('cid', '97'),
            ('ctid', '97'),
        )
        response = s.get(url, params=params).text
        # TODO decode (xor)
        # TODO parse response
        return response

    def _requests(self, league: str) -> Tuple[Dict]:
        """ Build URL starting from league (an unique id) and requests data for
            - full_time_result
            ...
        """
        config_url = 'https://www.bet365.it/defaultapi/sports-configuration'
        cookies = {'aps03': 'ct=97&lng=6'}
        headers = {
            'Connection': 'keep-alive',
            'Origin': 'https://www.bet365.it',
            'DNT': '1',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://www.bet365.it/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,it;q=0.8,la;q=0.7',
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/79.0.3945.117 Safari/537.36'
            ),
        }
        s = requests.Session()
        s.headers.update(headers)
        s.get(config_url, cookies=cookies)

        return (
            # full_time_result
            self._request(s, league, 13),
            # both_teams_to_score
            self._request(s, league, 170),
            # double_chance
            self._request(s, league, 195),
            # under_over
            # self._request(s, league, 56),
        )

    def odds(self, country: str, league: str) -> Dict:

        # Convert to standard country - league names
        country, league = self._country_league(country, league)

        # reuquest odds data
        odds = self._requests(league)

        # parse json response
        odds = []
        return odds
        '''
        return [{**i, **j, **k} for i, j, k in zip(*odds)]
        '''
