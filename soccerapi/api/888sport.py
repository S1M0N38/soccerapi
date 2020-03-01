import json
import os
from typing import Dict, List, Tuple

import requests


class Api888Sport:
    def __init__(self):
        self.name = '888sport'
        self.table = self._read_table()

    def _read_table(self) -> Dict:
        """ Read json table that store the relation between standard names and
        bookmaker names, ids and other. File name is {bookmaker}.json """

        here = os.path.dirname(__file__)
        table_path = os.path.join(here, f'{self.name}.json')
        with open(table_path) as f:
            table = json.load(f)
        return table

    def _country_league(self, country: str, league: str) -> Tuple[str, str]:
        """ Get standard country-league and convert to bookmaker country-league
        using self.table """

        try:
            country = self.table[country]['name']
        except KeyError:
            msg = (
                f'{country} is not in {self.name} table. '
                'Check the docs for a list of supported countries.'
            )
            raise KeyError(msg)
        try:
            league = self.table[country]['leagues'][league]['name']
        except KeyError:
            msg = (
                f'{league} is not in {self.name} table. '
                'Check the docs for a list of supported leagues.'
            )
            raise KeyError(msg)
        return country, league

    @staticmethod
    def _full_time_result(data: Dict) -> List:
        """ Parse the raw json requests for full_time_result & under_over """

        odds = []
        for event in data['events']:
            if event['event']['state'] == 'STARTED':
                continue
            try:
                full_time_result = {
                    '1': event['betOffers'][0]['outcomes'][0].get('odds'),
                    'X': event['betOffers'][0]['outcomes'][1].get('odds'),
                    '2': event['betOffers'][0]['outcomes'][2].get('odds'),
                }
            except IndexError:
                full_time_result = None

            odds.append(
                {
                    'time': event['event']['start'],
                    'home_team': event['event']['homeName'],
                    'away_team': event['event']['awayName'],
                    'full_time_resut': full_time_result,
                }
            )
        return odds

    @staticmethod
    def _both_teams_to_score(data: Dict) -> List:
        """ Parse the raw json requests for both_teams_to_score """

        odds = []
        for event in data['events']:
            if event['event']['state'] == 'STARTED':
                continue
            try:
                both_teams_to_score = {
                    'yes': event['betOffers'][0]['outcomes'][0].get('odds'),
                    'no': event['betOffers'][0]['outcomes'][1].get('odds'),
                }
            except IndexError:
                both_teams_to_score = None
            odds.append(
                {
                    'time': event['event']['start'],
                    'home_team': event['event']['homeName'],
                    'away_team': event['event']['awayName'],
                    'both_teams_to_score': both_teams_to_score,
                }
            )
        return odds

    @staticmethod
    def _double_chance(data: Dict) -> List:
        """ Parse the raw json requests for double chance """

        odds = []
        for event in data['events']:
            if event['event']['state'] == 'STARTED':
                continue
            try:
                double_chance = {
                    '1X': event['betOffers'][0]['outcomes'][0].get('odds'),
                    '12': event['betOffers'][0]['outcomes'][1].get('odds'),
                    '2X': event['betOffers'][0]['outcomes'][2].get('odds'),
                }
            except IndexError:
                double_chance = None
            odds.append(
                {
                    'time': event['event']['start'],
                    'home_team': event['event']['homeName'],
                    'away_team': event['event']['awayName'],
                    'double_chance': double_chance,
                }
            )
        return odds

    def _requests(self, country: str, league: str, market: str = 'IT') -> Dict:
        """ Build URL starting from country and league and request data for
            - full_time_result
            - both_teams_to_score
            - double_chance
        """

        s = requests.Session()
        base_params = {'lang': 'en_US', 'market': market}
        base_url = 'https://eu-offering.kambicdn.org/offering/v2018/888it/listView/football'
        url = '/'.join([base_url, country, league]) + '.json'

        return (
            # full_time_result
            s.get(url, params={**base_params, 'category': 12579}).json(),
            # both_teams_to_score
            s.get(url, params={**base_params, 'category': 11942}).json(),
            # double_chance
            s.get(url, params={**base_params, 'category': 12220}).json(),
        )

    def odds(self, country: str, league: str, market: str = 'IT') -> Dict:
        """ Get the odds for the contry-league competion as a python dict """

        # Convert to standard country - league names
        country, league = self._country_league(country, league)

        # reuquest odds data
        odds = self._requests(country, league, market)

        # parse json response
        odds = [
            self._full_time_result(odds[0]),
            self._both_teams_to_score(odds[1]),
            self._double_chance(odds[2]),
        ]
        return [{**i, **j, **k} for i, j, k in zip(*odds)]
