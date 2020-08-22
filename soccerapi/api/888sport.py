from .base import ApiKambi


class Api888Sport(ApiKambi):
    """ The ApiKambi implementation for 888sport.com """

    def __init__(self):
        self.name = '888sport'
        self.competitions = self._load_competitions()
        self.base_url = 'https://eu-offering.kambicdn.org/offering/v2018/888/listView/football'
        self.parsers = [
            self._full_time_result,
            self._both_teams_to_score,
            self._double_chance,
        ]
