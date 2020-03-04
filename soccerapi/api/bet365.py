import datetime
from typing import Dict, List, Tuple

import requests

from .base import ApiBase


class ApiBet365(ApiBase):
    def __init__(self):
        self.name = 'bet365'
        self.table = self._read_table()

    @staticmethod
    def _xor(msg: str, key: int) -> str:
        """ Applying xor algo to a message in order to make it readable """

        value = ''
        for char in msg:
            value += chr(ord(char) ^ key)
        return value

    def _guess_xor_key(self, encoded_msg: str) -> int:
        """ Try different key (int) until the msg is human readable """

        for key in range(150):  # TODO choose more narrow range
            msg = self._xor(encoded_msg, key)
            try:
                n, d = msg.split('/')
                if n.isdigit() and d.isdigit():
                    # TODO Collecting data for debug
                    with open('keys.txt', 'a') as f:
                        f.write(key)
                    return key
            except ValueError:
                pass
        raise ValueError('Key not found !')

    @staticmethod
    def _get_values(data: str, value: str) -> List:
        values = []
        for row in data.split('|'):
            if row.startswith('PA'):
                for data in row.split(';'):
                    if data.startswith(value):
                        values.append(data[3:])
        return values

    def _parse_datetimes(self, data: str) -> List:
        datetimes = []
        values = self._get_values(data, 'BC')
        for dt in values:
            datetimes.append(datetime.strptime(dt, '%Y%m%d%H%M%S'))
        return datetimes

    def _parse_teams(self, data: str) -> List:
        home_teams, away_teams = [], []
        values = self._get_values(data, 'NA')
        for teams in values:
            if ' v ' in teams:
                home_team, away_team = teams.split(' v ')
                home_teams.append(home_team)
                away_teams.append(away_team)
        return home_teams, away_teams

    def _parse_odds(self, data: str) -> List:
        odds = []
        values = self._get_values(data, 'OD')
        key = self._get_xor_key(values[0])
        for odd in values:
            n, d = self._xor(odd, key).split('/')
            # TODO Watch out, the conversion between frac and dec
            # is not perfect due to rounding
            decimal_odd = round(int(n) / int(d) + 1, 3)
            odds.append(decimal_odd)
        return odds

    def _parse_events(self, data: str) -> List:
        """ Parse datetime, home_team, away_team and return list of events """

        events = []
        datetimes = self.parse_datetimes(data)
        home_teams, away_teams = self.parse_teams(data)

        for dt, home_team, away_team in zip(datetimes, home_teams, away_teams):
            events.append(
                {'time': dt, 'home_team': home_team, 'away_team': away_team}
            )

        return events

    def _full_time_result(self, data: str) -> List:
        """ Parse the raw data for full_time_result """

        odds = []
        events = self.parse_events(data)
        full_time_result = self.parse_odds(data)
        _1s = full_time_result[0::3]
        _Xs = full_time_result[1::3]
        _2s = full_time_result[2::3]

        for event, _1, _X, _2 in zip(events, _1s, _Xs, _2s):
            odds.append(
                {**event, 'full_time_result': {'1': _1, 'X': _X, '2': _2}}
            )

        return odds

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

    def _request(self, s: requests.Session, league: str, category: int) -> str:
        url = 'https://www.bet365.it/SportsBook.API/web'
        params = (
            ('lid', '1'),
            ('zid', '0'),
            ('pd', f'#AC#B1#C1#D{category}#{league}#F2#'),
            ('cid', '97'),
            ('ctid', '97'),
        )
        return s.get(url, params=params).text

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
        odds = [
            self._full_time_result(odds[0]),
        ]
        return odds
        '''
        return [{**i, **j, **k} for i, j, k in zip(*odds)]
        '''
