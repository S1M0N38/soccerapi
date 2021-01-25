from typing import Dict, List

import requests

from .base import ApiBase


class ParserExample:
    """ Implementation of parsers for ApiExample """

    # Parser class implements the data parsers (i.e. methods that take
    # raw data, json data, obfuscated data return them in an organized form)

    # Parser retrun list of events + odds.
    # Example for full_time_result -> [
    # {
    #   'time': datetime.datetime(2021, 1, 17, 12, 17, 39),
    #   'home_team': 'juventus',
    #   'away_team': 'inter',
    #   'odds': {'1': 1500, 'X': 1500, '2': 3350}
    # },
    # ...
    # {
    #   'time': datetime.datetime(2021, 1, 20, 12, 17, 39),
    #   'home_team': 'milan',
    #   'away_team': 'torino',
    #   'odds': {'1': 1250, 'X': 1500, '2': 4500}
    # },
    # ]
    #
    # 'time': python datetime object when the match starts
    # 'home_team': name of the home team that appears on the bookmaker site
    # 'away_team': name of the away team that appears on the bookmaker site
    # 'odds': dict of of odds in decimal (millesimal) format; the keys of the
    #   dict depend on the parser type.

    # Type of parsers:
    # - full_time_result    -> {  '1': 1250,  'X': 1500,  '2': 4500}
    # - double_chance       -> { '1X': 1250, '12': 1500, '2X': 4500}
    # - both_teams_to_score -> {'yes': 1250, 'no': 1500}

    def full_time_result(self, data) -> List[Dict]:

        # events = list of events parsed from data
        # odds = list of odds in decimal format parsed from data

        # For extraxting events or odds from row data, sometimes it's usefull
        # to define some auxiliary methods (e.g. parsing the time, teams or
        # for deobfuscate odds). Name of those methods should starts with
        # underscore (e.g. _time, _teams, ...)

        ...

        # return [
        #     {**e, 'odds': {'1': ..., 'X': ..., '2': ...}}
        #     for i, (e, o) in enumerate(zip(events, odds))
        # ]

    def both_teams_to_score(self, data) -> List[Dict]:
        ...

    def double_chance(self, data) -> List[Dict]:
        ...

    # Auxiliary methods

    # def _time(self, data):
    #   ...
    #
    # def _teams(self, data):
    #   ...
    #
    # def _events(self, data):
    #   ...
    #
    # def _odds(self, data):
    #   ...


class ApiExample(ApiBase, ParserExample):
    """ Api for Example bookmaker """

    def __init__(self):
        # bookmaker name
        self.name = 'example'

        # requests session used to the request to bookmaker site
        self.session = requests.Session()

    def competition(self, url: str) -> str:
        # Parese the bookmaker url containing the competition information
        # using some kind of regex
        ...
        # return 'Italia-SerieA'

    def requests(self, competition: str):
        # Perform requeests to various endpoints in order to get odds
        # for different categories (e.g. full_time_result, double_chance, ...)

        # Define here the session.headers and cookies.

        # Sometime is useful define an auxiliary method _request which
        # accepts the category param and send correct headers and params.
        # Auxiliary methods names should start with underscore (e.g. _request).

        ...
        # return {
        #     'full_time_result': self._request(competition, 13),
        #     'both_teams_to_score': self._request(competition, 170),
        #     'double_chance': self._request(competition, 195),
        # }

    # Auxiliary methods

    # def _request(self, competition: str, category: int):
    #   ...
