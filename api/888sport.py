import json
import os
from typing import Dict, Tuple


class Api888Sport:
    def __init__(self):
        self.name = '888sport'
        self.table = self._read_table()

    def _read_table(self) -> Dict:
        """ Read json table that store the relation between standard names and
        bookmaker names, ids and other. File name is {bookmaker}.json """

        here = os.path.dirname(__file__)
        table_path = os.path.join(here, f'{self.name}.json')
        with open(table_path) as f:
            table = json.load(f)
        return table

    def _country_league(self, country: str, league: str) -> Tuple[str, str]:
        """ Get standard country-league and convert to bookmaker country-league
        using self.table """

        try:
            country = self.table[country]['name']
        except KeyError:
            msg = (
                f'{country} is not in {self.name} table. '
                'Check the docs for a list of supported countries.'
            )
            raise KeyError(msg)
        try:
            league = self.table[country]['leagues'][league]
        except KeyError:
            msg = (
                f'{league} is not in {self.name} table. '
                'Check the docs for a list of supported leagues.'
            )
            raise KeyError(msg)
        return country, league
