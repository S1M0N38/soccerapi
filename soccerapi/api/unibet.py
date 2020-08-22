from .base import ApiKambi


class ApiUnibet(ApiKambi):
    """ The ApiBase implementation for unibet.com """

    def __init__(self):
        self.name = 'unibet'
        self.competitions = self._load_competitions()
        self.base_url = 'https://eu-offering.kambicdn.org/offering/v2018/ub/listView/football'
        self.parsers = [
            self._full_time_result,
            self._both_teams_to_score,
            self._double_chance,
        ]
