import abc
from typing import List, Tuple


class ApiBase(abc.ABC):
    """ The Abstract Base Class on which every Api[Boolmaker] is based on. """

    @abc.abstractmethod
    def requests(self, competition: str, **kwargs) -> Tuple:
        """ Open a requests.Session and perform _request """
        pass

    @abc.abstractmethod
    def competition(self, url: str) -> str:
        """Get the competition from url.
        First check it validity using regex,then exstract competition from it
        """
        pass

    def odds(self, url: str) -> List:
        """ Get odds from url """
        odds = self.requests(self.competition(url))

        # parse odds
        for parser, data in odds.items():
            odds[parser] = getattr(self, parser)(data)

        # TODO merge odds
        return odds


class NoOddsError(Exception):
    """ No odds are found. """
