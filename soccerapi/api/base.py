import abc
from typing import List, Tuple


class ApiBase(abc.ABC):
    """ The Abstract Base Class on which every Api[Bookmaker] is based on. """

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
        to_parse = self.requests(self.competition(url))

        # parse odds
        to_format = dict()
        for parser, data in to_parse.items():
            to_format[parser]= getattr(self, parser)(data) # why not "self.parser(data)" ??

        # TODO format odds
        # get list of events
        odds = to_format[list(to_parse.keys())[0]].copy()
        for ind, event in enumerate(odds):
            for parser in to_parse.keys():
                # add market (parser) to event
                event[parser] = to_format[parser][ind].get('odds')
            # pop inherited odds key
            event.pop('odds')
            odds[ind] = event.copy()

        return odds


class NoOddsError(Exception):
    """ No odds are found. """
