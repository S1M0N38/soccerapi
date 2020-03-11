import importlib

package = 'soccerapi.api'
Api888Sport = importlib.import_module('.888sport', package).Api888Sport


class ApiUnibet(Api888Sport):
    """ The ApiBase implementation of unibet.com """

    def __init__(self):
        self.name = 'unibet'
        self.table = self._read_table()
        self.base_url = 'https://eu-offering.kambicdn.org/offering/v2018/ub/listView/football'

    # 888sport and unibet uses the same CDN (eu-offering.kambicdn)
    # so the requetsting and parsing process is exaclty the same.
    # The only thing that chage is the base_url
