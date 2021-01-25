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

        odds_to_parse = self.requests(self.competition(url))
        odds_to_merge = {}

        # parse odds
        for parser, data in odds_to_parse.items():
            odds_to_merge[parser] = getattr(self, parser)(data)

        # collect events from full_time_result
        odds = [
            {
                'time': e['time'],
                'home_team': e['home_team'],
                'away_team': e['away_team'],
            }
            for e in odds_to_merge['full_time_result']
        ]

        for category, events in odds_to_merge.items():
            for i, event in enumerate(events):
                assert event['home_team'] == odds[i]['home_team']
                assert event['away_team'] == odds[i]['away_team']
                odds[i][category] = event['odds']

        return odds


class NoOddsError(Exception):
    """ No odds are found. """
