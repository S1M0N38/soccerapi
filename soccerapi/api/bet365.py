import re
from datetime import datetime
from typing import Dict, List, Tuple

import requests

from .base import ApiBase, NoOddsError


class ParserBet365:
    """ Implementation of parsers for ApiBet365 """

    def full_time_result(self, data: str) -> List:
        odds = []
        events = self._parse_events(data)
        full_time_result = self._parse_odds(data)

        assert len(events) == len(full_time_result) / 3

        le = len(events)
        assert le == len(full_time_result) / 3
        _1s = full_time_result[:le]
        _Xs = full_time_result[le : 2 * le]
        _2s = full_time_result[2 * le :]

        for event, _1, _X, _2 in zip(events, _1s, _Xs, _2s):
            odds.append({**event, 'odds': {'1': _1, 'X': _X, '2': _2}})
        return odds

    def both_teams_to_score(self, data: str) -> List:
        odds = []
        events = self._parse_events(data)
        both_teams_to_score = self._parse_odds(data)

        assert len(events) == len(both_teams_to_score) / 2
        yess = both_teams_to_score[: len(events)]
        nos = both_teams_to_score[len(events) :]

        for event, yes, no in zip(events, yess, nos):
            odds.append({**event, 'odds': {'yes': yes, 'no': no}})

        return odds

    def double_chance(self, data: str) -> List:
        odds = []
        events = self._parse_events(data)
        double_chance = self._parse_odds(data)

        le = len(events)
        assert le == len(double_chance) / 3
        _1Xs = double_chance[:le]
        _2Xs = double_chance[le : 2 * le]
        _12s = double_chance[2 * le :]

        for event, _1X, _2X, _12 in zip(events, _1Xs, _2Xs, _12s):
            odds.append({**event, 'odds': {'1X': _1X, '12': _12, '2X': _2X}})

        return odds

    def draw_no_bet(self, data: str) -> List:
        odds = []
        events = self._parse_events(data)
        draw_no_bet = self._parse_odds(data)

        le = len(events)
        assert le == len(draw_no_bet) / 2
        _1 = draw_no_bet[:le]
        _2 = draw_no_bet[le:]

        for event, _1, _2 in zip(events, _1, _2):
            odds.append({**event, 'odds': {'1': _1, '2': _2}})

        return odds

    def asian_handicap(self, data: Tuple) -> List:
        # parsing odds for asian handicap : data[0]
        odds = []
        events = self._parse_events(data[0])
        asian_handicap = self._parse_odds(data[0])

        le = len(events)
        assert le == len(asian_handicap) / 2
        _1 = asian_handicap[:le]
        _2 = asian_handicap[le:]

        home_handicaps = self._get_values(data[0], 'HD')[:le]
        away_handicaps = self._get_values(data[0], 'HD')[le:]

        zipped = zip(events, home_handicaps, away_handicaps, _1, _2)
        for event, hH, aH, _1, _2 in zipped:
            odds.append(
                {
                    **event,
                    'odds': {
                        '1': {hH: _1},
                        '2': {aH: _2},
                    },
                }
            )

        # parsing odds for alternative asian handicap: data[1]
        events = data[1].split('MG;')[2:-1]
        le = len(events)  # potentially different from the one at line 83

        alt_asian_handicaps = self._parse_odds(data[1])
        for i, odd, event in zip(range(le), odds[:le], events):
            # find leght of odds per event
            lo = len(self._get_values(event, 'OD')) // 2

            _1 = alt_asian_handicaps[i * lo : lo * (i + 1)]
            _2 = alt_asian_handicaps[lo * (i + 1) : lo * (i + 2)]

            home_handicaps = self._get_values(event, 'NA')[:lo]
            away_handicaps = self._get_values(event, 'NA')[lo:]

            for hH, aH, _1, _2 in zip(home_handicaps, away_handicaps, _1, _2):
                odd['odds']['1'][hH] = _1
                odd['odds']['2'][hH] = _2

        return odds

    def under_over(self, data: str) -> List:
        odds = []

        # parse events for U/O2.5 different from the others
        events = data.split('MG;')[2:-1]

        datetimes = [event.split('BC=')[1][:14] for event in events]
        datetimes = [datetime.strptime(dt, '%Y%m%d%H%M%S') for dt in datetimes]

        matches = [event.split('NA=')[1].split(';')[0] for event in events]
        home_teams = [match.split(' v ')[0] for match in matches]
        away_teams = [match.split(' v ')[1] for match in matches]

        events = []
        for dt, home_team, away_team in zip(datetimes, home_teams, away_teams):
            if dt > datetime.utcnow():
                events.append(
                    {'time': dt, 'home_team': home_team, 'away_team': away_team}
                )

        under_over = self._parse_odds(data)

        le = len(events)
        assert le == len(under_over) / 2
        over = under_over[:le]
        under = under_over[le:]

        for event, over, under in zip(events, over, under):
            odds.append({**event, 'odds': {'O2.5': over, 'U2.5': over}})

        return odds

    # Auxiliary methods

    @staticmethod
    def _xor(msg: str, key: int) -> str:
        """ Applying xor algo to a message in order to make it readable """

        value = ''
        for char in msg:
            value += chr(ord(char) ^ key)
        return value

    @staticmethod
    def _get_values(data: str, value: str) -> List:
        """ Get value from data str XX=... return ...) """

        values = []
        for row in data.split('|'):
            if row.startswith('PA'):
                for data in row.split(';'):
                    if data.startswith(value):
                        values.append(data[3:])
        return values

    def _parse_datetimes(self, data: str) -> List:
        """ Parse datetimes in human readable ftm """

        datetimes = []
        values = self._get_values(data, 'BC')
        for dt in values:
            datetimes.append(datetime.strptime(dt, '%Y%m%d%H%M%S'))
        return datetimes

    def _parse_teams(self, data: str) -> List:
        """ Parse teams names from data str """

        home_teams, away_teams = [], []
        values = self._get_values(data, 'FD')
        for teams in values:
            if ' v ' in teams:
                home_team, away_team = teams.split(' v ')
                home_teams.append(home_team)
                away_teams.append(away_team)
        return home_teams, away_teams

    def _parse_odds(self, data: str) -> List:
        """ Get odds from data str, xoring and convert to decimal """

        odds = []
        values = self._get_values(data, 'OD')
        if len(values) == 0:
            raise NoOddsError

        TK = data.split(';')[1][3:]
        key = ord(TK[0]) ^ ord(TK[1])

        for obfuscated_odd in values:
            # Event exists but no odds are available
            if obfuscated_odd == '':
                odd = None
            else:
                n, d = self._xor(obfuscated_odd, key).split('/')
                # it seem that is the conversion formula used by bet365 to
                # convert from fractional to decimal format
                odd = int((int(n) / int(d) + 1) * 100) * 10
            odds.append(odd)
        return odds

    def _parse_events(self, data: str) -> List:
        """ Parse datetime, home_team, away_team and return list of events """

        events = []
        datetimes = self._parse_datetimes(data)
        home_teams, away_teams = self._parse_teams(data)

        for dt, home_team, away_team in zip(datetimes, home_teams, away_teams):
            if dt > datetime.utcnow():
                events.append(
                    {'time': dt, 'home_team': home_team, 'away_team': away_team}
                )

        return events


class ApiBet365(ApiBase, ParserBet365):
    """The ApiBase implementation of bet365.com
    In order to init a new Session for bet365 cookies and headers are required.
    """

    def __init__(self):
        self.name = 'bet365'
        self.session = requests.Session()

    def url_to_competition(self, url: str) -> str:
        re_bet365 = re.compile(
            r'https?://www\.bet365\.\w{2,3}/#/'
            r'AC/B1/C1/D7/E40/F4/G[0-9]+/H3/?'
        )
        if re_bet365.match(url):
            return url.split('/')[10]
        else:
            msg = f'Cannot parse {url}'
            raise ValueError(msg)

    def competitions(self, base_url='https://www.bet365.com/#') -> str:
        table = {}
        table_country = self._request(
            '#AM#B1#C1#D7#E40#F4#G96703929#H3#Z^1#Y^1_7_40_4_96703929#S1#',
        ).split('|')

        for row in table_country[2:-1]:
            country = row.split('NA=')[1].split(';')[0]
            country_link = row.split('PD=')[1].split(';')[0]

            table[country] = {}
            table_league = self._request(country_link).split('|')
            for row2 in table_league[3:-1]:
                league = row2.split('NA=')[1].split(';')[0]
                league_link = row2.split('PD=')[1].split(';')[0]
                link = base_url + league_link.replace('#', '/')
                table[country][league] = link

        return table

    def requests(self, competition: str) -> Tuple[Dict]:
        return {
            'full_time_result': self._request(
                f'#AC#B1#C1#D7#E40#F4#{competition}#H3#'
            ),
            'both_teams_to_score': self._request(
                f'#AC#B1#C1#D7#E10150#F4#{competition}#H3#'
            ),
            'double_chance': self._request(
                f'#AC#B1#C1#D7#E50401#F4#{competition}#H3#'
            ),
            'draw_no_bet': self._request(
                f'#AC#B1#C1#D7#E10544#F4#{competition}#H3#'
            ),
            'asian_handicap': (
                self._request(f'#AC#B1#C1#D7#E938#F4#{competition}#H3#'),
                self._request(f'#AC#B1#C1#D7#E50138#F4#{competition}#H3#'),
            ),
            'under_over': self._request(
                f'#AC#B1#C1#D7#E981#F4#{competition}#H3#'
            ),
        }

    # Auxiliary methods

    def _request(self, pd: str) -> str:
        """Make the single request using the active session.
        The pd is a string that contains information about competition
        and market (i.e. 'full_time_result', 'double_chance', ...)
        """

        response = requests.get('http://localhost:5000/bet365').json()
        self.session.headers.update(response['headers'])
        for cookie in response['cookies']:
            self.session.cookies.set(cookie['name'], cookie['value'])

        url = 'https://www.bet365.it/SportsBook.API/web'
        params = (
            ('lid', '1'),  # language id, 1 == english
            ('zid', '0'),
            ('pd', pd),
            ('cid', '97'),
            ('ctid', '97'),
        )
        return self.session.get(url, params=params).text
