import pytest

from api import Api888Sport as API


class TestAPI:
    @pytest.fixture(scope='module')
    def api(self):
        api = API()
        yield api

    def test_wrong_country(self, api):
        with pytest.raises(KeyError, match='.*countries'):
            country, league = api._country_league('fake_country', 'serie_a')

    def test_wrong_league(self, api):
        with pytest.raises(KeyError, match='.*leagues'):
            country, league = api._country_league('italy', 'fake_league')

    def test_right_country_league(self, api):
        country, league = api._country_league('italy', 'serie_a')
        assert country
        assert league
