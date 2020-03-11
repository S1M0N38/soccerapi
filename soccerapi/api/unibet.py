from .base import ApiKambi


class ApiUnibet(ApiKambi):
    """ The ApiBase implementation for unibet.com """

    def __init__(self):
        self.name = 'unibet'
        self.table = self._read_table()
        self.base_url = (
            'https://eu-offering.kambicdn.org/offering/v2018/ub/listView/football'
        )
