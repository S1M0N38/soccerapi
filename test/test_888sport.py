import json
import os
from typing import List, Tuple

import pytest

from soccerapi import Api888Sport as API


def competitions() -> List[Tuple[str, str]]:
    competitions = []
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    table_path = os.path.join(base_dir, 'soccerapi', '888sport.json')
    with open(table_path) as f:
        table = json.load(f)
    for country, value in table.items():
        for league in value['leagues']:
            competitions.append((country, league))
    return competitions


class TestAPI:
    @pytest.fixture(scope='module')
    def api(self):
        api = API()
        yield api

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

    @pytest.mark.parametrize('country,league', competitions())
    def test_odds(self, api, country, league):
        odds = api.odds(country, league)
        assert odds
