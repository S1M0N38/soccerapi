import abc
import csv
from typing import List, Tuple

import pytest
import requests

from soccerapi.api import Api888Sport, ApiBet365, ApiUnibet


def competitions(name: str) -> List[Tuple[str, str]]:
    competitions = []
    url = (
        'https://docs.google.com/spreadsheets/d/'
        '1kHFeE1hsiCwzLBNe2gokCOfVDSocc0mcKTF3HEhQ3ec/'
        'export?format=csv&'
        'id=1kHFeE1hsiCwzLBNe2gokCOfVDSocc0mcKTF3HEhQ3ec&'
        'gid=1816911805'
    )
    data = requests.get(url).text.splitlines()
    rows = csv.DictReader(data)
    for row in rows:
        if row[name] != '' and row['country'] != 'test_country':
            competitions.append((row['country'], row['league']))
    return competitions


class BaseTest(abc.ABC):
    @abc.abstractmethod
    def api(self):
        pass

    def test_wrong_country(self, api):
        with pytest.raises(KeyError, match='.*not supported'):
            api._competition('fake_country', 'test_league')

    def test_wrong_league(self, api):
        with pytest.raises(KeyError, match='.*not supported'):
            api._competition('test_country', 'fake_league')

    def test_right_country_league(self, api):
        competition = api._competition('test_country', 'test_league')
        assert competition


@pytest.mark.Api888Sport
class TestApi888Sport(BaseTest):
    name = '888sport'

    @pytest.fixture(scope='module')
    def api(self):
        yield Api888Sport()

    @pytest.mark.parametrize('country,league', competitions(name))
    def test_odds(self, api, country, league):
        odds = api.odds(country, league)
        assert odds


@pytest.mark.ApiBet365
class TestApiBet365(BaseTest):
    name = 'bet365'

    @pytest.fixture(scope='module')
    def api(self):
        yield ApiBet365()

    @pytest.mark.parametrize('country,league', competitions(name))
    def test_odds(self, api, country, league):
        odds = api.odds(country, league)
        assert odds


@pytest.mark.ApiUnibet
class TestApiUnibet(BaseTest):
    name = 'unibet'

    @pytest.fixture(scope='module')
    def api(self):
        yield ApiUnibet()

    @pytest.mark.parametrize('country,league', competitions(name))
    def test_odds(self, api, country, league):
        odds = api.odds(country, league)
        assert odds
