import abc
from pprint import pprint

import pytest
from soccerapi.api import Api888Sport, ApiBet365, ApiUnibet

from urls import urls_888sport, urls_bet365, urls_unibet


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
