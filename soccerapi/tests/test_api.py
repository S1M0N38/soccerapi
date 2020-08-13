import abc
import csv
import json
import os
from typing import List, Tuple

import pytest
import requests

from soccerapi.api import Api888Sport, ApiBet365, ApiUnibet


def competitions(name: str) -> List[Tuple[str, str]]:
    competitions = []
    url = (
        'https://raw.githubusercontent.com/'
        'S1M0N38/soccerapi-competitions/master/competitions.csv'
    )
    data = requests.get(url).text.splitlines()
    rows = csv.DictReader(data)
    for row in rows:
        if row[name] != '':
            competitions.append((row['country'], row['league']))
    return competitions


class BaseTest(abc.ABC):
    @abc.abstractmethod
    def api():
        pass

    def test_wrong_country(self, api):
        with pytest.raises(KeyError, match='.*not supported'):
            api._competition('fake_country', 'serie_a')

    def test_wrong_league(self, api):
        with pytest.raises(KeyError, match='.*not supported'):
            api._competition('italy', 'fake_league')

    def test_right_country_league(self, api):
        competition = api._competition('italy', 'serie_a')
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
