import abc
from typing import Dict, List, Tuple


class ApiBase(abc.ABC):
    """The Abstract Base Class on which every Api[Bookmaker] is based on."""

    @abc.abstractmethod
    def requests(self, competition: str, **kwargs) -> Tuple:
        """Perform requests to various markets."""
        pass

    @abc.abstractmethod
    def url_to_competition(self, url: str) -> str:
        """Convert url to the correspoing the competition.
        First check it validity using regex, then exstract
        competition from it"""
        pass

    @abc.abstractmethod
    def competitions(self) -> Dict:
        """Get a dict of available competitions."""
        pass

    def odds(self, url: str) -> List:
        """Get odds from url."""

        odds_to_parse = self.requests(self.url_to_competition(url))
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
                # needed check for no odds for some match in some markets
                if event['home_team'] == odds[i]['home_team'] and \
                   event['away_team'] == odds[i]['away_team']:
                    odds[i][category] = event['odds']

        return odds


class NoOddsError(Exception):
    """ No odds are found."""
