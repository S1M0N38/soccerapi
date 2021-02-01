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
    def setup(self):
        pass

    def test_competitions(self):
        competitions = self.api.competitions()
        pprint(competitions)
        assert competitions


@pytest.mark.Api888Sport
class TestApi888Sport(BaseTest):
    name = '888sport'

    def setup(self):
        self.api = Api888Sport()

    @pytest.mark.parametrize('url', urls['888sport'])
    def test_odds(self, url):
        odds = self.api.odds(url)
        pprint(odds)
        assert odds


@pytest.mark.ApiBet365
class TestApiBet365(BaseTest):
    name = 'bet365'

    def setup(self):
        self.api = ApiBet365()

    @pytest.mark.parametrize('url', urls['bet365'])
    def test_odds(self, url):
        odds = self.api.odds(url)
        pprint(odds)
        assert odds


@pytest.mark.ApiUnibet
class TestApiUnibet(BaseTest):
    name = 'unibet'

    def setup(self):
        self.api = ApiUnibet()

    @pytest.mark.parametrize('url', urls['unibet'])
    def test_odds(self, url):
        odds = self.api.odds(url)
        pprint(odds)
        assert odds
