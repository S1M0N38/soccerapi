import abc
import json
import os
from typing import List, Tuple

import pytest

from soccerapi.api import Api888Sport, ApiBet365, ApiUnibet


def competitions(name: str) -> List[Tuple[str, str]]:
    competitions = []
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    table_path = os.path.join(base_dir, 'api', name, f'{name}.json')
    with open(table_path) as f:
        table = json.load(f)
    for country, value in table.items():
        for league in value['leagues']:
            competitions.append((country, league))
    return competitions


class BaseTest(abc.ABC):
    @abc.abstractmethod
    def api():
        pass

    def test_wrong_country(self, api):
        with pytest.raises(KeyError, match='.*countries'):
            api._country_league('fake_country', 'serie_a')

    def test_wrong_league(self, api):
        with pytest.raises(KeyError, match='.*leagues'):
            api._country_league('italy', 'fake_league')

    def test_right_country_league(self, api):
        country, league = api._country_league('italy', 'serie_a')
        assert country
        assert league


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
