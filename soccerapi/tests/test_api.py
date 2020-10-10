import abc
# import csv
from pprint import pprint

import pytest
# import requests
from soccerapi.api import Api888Sport, ApiBet365, ApiUnibet

# from typing import List, Tuple


# def competitions(name: str) -> List[Tuple[str, str]]:
#     competitions = []
#     url = (
#         'https://docs.google.com/spreadsheets/d/'
#         '1kHFeE1hsiCwzLBNe2gokCOfVDSocc0mcKTF3HEhQ3ec/'
#         'export?format=csv&'
#         'id=1kHFeE1hsiCwzLBNe2gokCOfVDSocc0mcKTF3HEhQ3ec&'
#         'gid=1816911805'
#     )
#     data = requests.get(url).text.splitlines()
#     rows = csv.DictReader(data)
#     for row in rows:
#         if row[name] != '' and row['country'] != 'test_country':
#             competitions.append((row['country'], row['league']))
#     return competitions


urls_bet365 = [
    'https://www.bet365.it/#/AC/B1/C1/D13/E52224631/F2/',  # italy-seria_a
    'https://www.bet365.it/#/AC/B1/C1/D13/E52547961/F2/I1/',  # italy-serie-b
    'https://www.bet365.it/#/AC/B1/C1/D13/E51761579/F2/',  # england-premier_league
    'https://www.bet365.it/#/AC/B1/C1/D13/E51791071/F2/I1/',  # england-championship
    'https://www.bet365.it/#/AC/B1/C1/D13/E51669667/F2/I1/',  # germany-bundesliga
    'https://www.bet365.it/#/AC/B1/C1/D13/E51669781/F2/I1/',  # germany-bundesliga2
]

urls_888sport = [
    'https://www.888sport.it/#/filter/football/italy/serie_a',  # italy-seria_a
    'https://www.888sport.it/#/filter/football/italy/serie_b',  # italy-serie-b
    'https://www.888sport.it/#/filter/football/england/premier_league',  # england-premier_league
    'https://www.888sport.it/#/filter/football/england/the_championship',  # england-championship
    'https://www.888sport.it/#/filter/football/germany/bundesliga',  # germany-bundesliga
    'https://www.888sport.it/#/filter/football/germany/2__bundesliga',  # germany-bundesliga2
]

urls_unibet = [
    'https://www.unibet.com/betting/sports/filter/football/italy/serie_a/matches',  # italy-seria_a
    'https://www.unibet.com/betting/sports/filter/football/italy/serie_b/matches',  # italy-serie-b
    'https://www.unibet.com/betting/sports/filter/football/england/premier_league/matches',  # england-premier_league
    'https://www.unibet.com/betting/sports/filter/football/england/the_championship/matches',  # england-championship
    'https://www.unibet.com/betting/sports/filter/football/germany/bundesliga/matches',  # germany-bundesliga
    'https://www.unibet.com/betting/sports/filter/football/germany/2__bundesliga/',  # germany-bundesliga2
]


class BaseTest(abc.ABC):
    @abc.abstractmethod
    def api(self):
        pass


@pytest.mark.Api888Sport
class TestApi888Sport(BaseTest):
    name = '888sport'

    @pytest.fixture(scope='module')
    def api(self):
        yield Api888Sport()

    # TODO add test competition

    @pytest.mark.parametrize('url', urls_888sport)
    def test_odds(self, api, url):
        odds = api.odds(url)
        pprint(odds)
        assert odds


@pytest.mark.ApiBet365
class TestApiBet365(BaseTest):
    name = 'bet365'

    @pytest.fixture(scope='module')
    def api(self):
        yield ApiBet365()

    # TODO add test competition

    @pytest.mark.parametrize('url', urls_bet365)
    def test_odds(self, api, url):
        odds = api.odds(url)
        pprint(odds)
        assert odds


@pytest.mark.ApiUnibet
class TestApiUnibet(BaseTest):
    name = 'unibet'

    @pytest.fixture(scope='module')
    def api(self):
        yield ApiUnibet()

    # TODO add test competition

    @pytest.mark.parametrize('url', urls_unibet)
    def test_odds(self, api, url):
        odds = api.odds(url)
        pprint(odds)
        assert odds
