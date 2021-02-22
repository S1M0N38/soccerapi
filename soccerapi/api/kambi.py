from typing import Dict, List


class ParserKambi:
    """888sport, unibet and other use the same CDN (eu-offering.kambicdn)
    so the requetsting and parsing process is exaclty the same.
    This class implements parsers for variuos category for Kambi."""

    def full_time_result(self, data: Dict) -> List:
        """ Parse the raw json requests for full_time_result """

        odds = []
        for event in data['events']:
            if event['event'].get('state') == 'STARTED':
                continue
            try:
                full_time_result = {
                    '1': event['betOffers'][0]['outcomes'][0].get('odds'),
                    'X': event['betOffers'][0]['outcomes'][1].get('odds'),
                    '2': event['betOffers'][0]['outcomes'][2].get('odds'),
                }
            except IndexError:
                full_time_result = None

            odds.append(
                {
                    'time': event['event'].get('start'),
                    'home_team': event['event'].get('homeName'),
                    'away_team': event['event'].get('awayName'),
                    'odds': full_time_result,
                }
            )
        return odds

    def under_over(self, data: Dict) -> List:
        """ Parse the raw json requests for under_over """

        odds = []
        for event in data['events']:
            if event['event'].get('state') == 'STARTED':
                continue
            try:
                under_over = {
                    'O2.5': event['betOffers'][0]['outcomes'][0].get('odds'),
                    'U2.5': event['betOffers'][0]['outcomes'][1].get('odds'),
                }
            except IndexError:
                under_over = None

            odds.append(
                {
                    'time': event['event'].get('start'),
                    'home_team': event['event'].get('homeName'),
                    'away_team': event['event'].get('awayName'),
                    'odds': under_over,
                }
            )
        return odds

    def both_teams_to_score(self, data: Dict) -> List:
        """ Parse the raw json requests for both_teams_to_score """

        odds = []
        for event in data['events']:
            if event['event'].get('state') == 'STARTED':
                continue
            try:
                both_teams_to_score = {
                    'yes': event['betOffers'][0]['outcomes'][0].get('odds'),
                    'no': event['betOffers'][0]['outcomes'][1].get('odds'),
                }
            except IndexError:
                both_teams_to_score = None
            odds.append(
                {
                    'time': event['event'].get('start'),
                    'home_team': event['event'].get('homeName'),
                    'away_team': event['event'].get('awayName'),
                    'odds': both_teams_to_score,
                }
            )
        return odds

    def double_chance(self, data: Dict) -> List:
        """ Parse the raw json requests for double chance """

        odds = []
        for event in data['events']:
            if event['event'].get('state') == 'STARTED':
                continue
            try:
                double_chance = {
                    '1X': event['betOffers'][0]['outcomes'][0].get('odds'),
                    '12': event['betOffers'][0]['outcomes'][1].get('odds'),
                    '2X': event['betOffers'][0]['outcomes'][2].get('odds'),
                }
            except IndexError:
                double_chance = None
            odds.append(
                {
                    'time': event['event'].get('start'),
                    'home_team': event['event'].get('homeName'),
                    'away_team': event['event'].get('awayName'),
                    'odds': double_chance,
                }
            )
        return odds

    # Auxiliary methods

    def _parse_competitions(self, base_url: str, data: Dict) -> Dict:
        """ Parse the raw json request for competitions """

        table = {}
        for sport in data['group']['groups']:
            if sport['termKey'] == 'football':
                football = sport['groups']
                break

        for country in football:

            if country['name'] not in table:
                table[country['name']] = {}

            if 'groups' in country:
                for league in country['groups']:
                    link = f'{base_url}{country["termKey"]}/{league["termKey"]}/'
                    table[country['name']][league['name']] = link
            else:
                link = f'{base_url}{country["termKey"]}/'
                table[country['name']][country['name']] = link

        return table
