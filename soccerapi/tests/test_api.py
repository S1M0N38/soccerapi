import abc
import json
from pprint import pprint

import pytest
from soccerapi.api import Api888Sport, ApiBet365, ApiUnibet

# from urls import urls_888sport, urls_bet365, urls_unibet

with open('urls.json') as f:
    urls = json.load(f)


class BaseTest(abc.ABC):
    @abc.abstractmethod
    def api(self):
        pass

    def test_competitions(self, api):
        competitions = api.competitions()
        pprint(competitions)
        assert competitions


@pytest.mark.Api888Sport
class TestApi888Sport(BaseTest):
    name = '888sport'

    @pytest.fixture(scope='module')
    def api(self):
        yield Api888Sport()

    @pytest.mark.parametrize('url', urls['888sport'])
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

    @pytest.mark.parametrize('url', urls['bet365'])
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

    @pytest.mark.parametrize('url', urls['unibet'])
    def test_odds(self, api, url):
        odds = api.odds(url)
        pprint(odds)
        assert odds
