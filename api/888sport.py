import json
import os
from typing import Dict, List, Tuple

import httpx


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
    def _full_time_result_under_over(data: Dict) -> List:
        """ Parse the raw json requests for full_time_result & under_over """

        odds = []
        for event in data['events']:
            if event['event']['state'] == 'STARTED':
                continue
            odds.append(
                {
                    'time': event['event']['start'],
                    'home_team': event['event']['homeName'],
                    'away_team': event['event']['awayName'],
                    'full_time_resut': {
                        '1': event['betOffers'][0]['outcomes'][0]['odds'],
                        'X': event['betOffers'][0]['outcomes'][1]['odds'],
                        '2': event['betOffers'][0]['outcomes'][2]['odds'],
                    },
                    'under_over': {
                        'under': event['betOffers'][1]['outcomes'][1]['odds'],
                        'over': event['betOffers'][1]['outcomes'][0]['odds'],
                    },
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
            odds.append(
                {
                    'time': event['event']['start'],
                    'home_team': event['event']['homeName'],
                    'away_team': event['event']['awayName'],
                    'both_teams_to_score': {
                        'yes': event['betOffers'][0]['outcomes'][0]['odds'],
                        'no': event['betOffers'][0]['outcomes'][1]['odds'],
                    },
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
            odds.append(
                {
                    'time': event['event']['start'],
                    'home_team': event['event']['homeName'],
                    'away_team': event['event']['awayName'],
                    'double_chance': {
                        '1X': event['betOffers'][0]['outcomes'][0]['odds'],
                        '12': event['betOffers'][0]['outcomes'][1]['odds'],
                        '2X': event['betOffers'][0]['outcomes'][2]['odds'],
                    },
                }
            )
        return odds

    def odds(self, country: str, league: str, market: str = 'US') -> Dict:
        """ Get the odds for the contry-league competion as a python dict """

        base_params = {'lang': 'en_US', 'market': market}
        base_url = 'https://eu-offering.kambicdn.org/offering/v2018/888it/listView/football'
        country, league = self._country_league(country, league)
        url = '/'.join([base_url, country, league]) + '.json'

        with httpx.Client(params=base_params) as client:
            odds = [
                self._full_time_result_under_over(
                    client.get(url, params={'useCombined': True}).json()
                ),
                self._both_teams_to_score(
                    client.get(url, params={'category': 11942}).json()
                ),
                self._double_chance(
                    client.get(url, params={'category': 12220}).json()
                ),
            ]
        return [{**i, **j, **k} for i, j, k in zip(*odds)]
