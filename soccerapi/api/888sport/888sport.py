from ..base import ApiKambi


class Api888Sport(ApiKambi):
    """ The ApiKambi implementation for 888sport.com """

    def __init__(self):
        self.name = '888sport'
        self.table = self._read_table()
        self.base_url = (
            'https://eu-offering.kambicdn.org/offering/v2018/888/listView/football'
        )
