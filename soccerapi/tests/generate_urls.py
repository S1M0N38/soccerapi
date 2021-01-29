import json
from pprint import pprint

from soccerapi.api import Api888Sport, ApiBet365, ApiUnibet


def generate_888sport_urls():
    api = Api888Sport()
    competitions = api.competitions()
    return [
        competitions['Italy']['Serie A'],
        competitions['Italy']['Serie B'],
        competitions['England']['Premier League'],
        competitions['England']['The Championship'],
        competitions['Germany']['Bundesliga'],
        competitions['Germany']['2. Bundesliga'],
    ]


def generate_bet365_urls():
    api = ApiBet365()
    competitions = api.competitions()
    return [
        competitions['Italy']['Italy Serie A'],
        competitions['Italy']['Italy Serie B'],
        competitions['United Kingdom']['England Premier League'],
        competitions['United Kingdom']['England Championship'],
        competitions['Germany']['Germany Bundesliga I'],
        competitions['Germany']['Germany Bundesliga II'],
    ]


def generate_unibet_urls():
    api = ApiUnibet()
    competitions = api.competitions()
    return [
        competitions['Italy']['Serie A'],
        competitions['Italy']['Serie B'],
        competitions['England']['Premier League'],
        competitions['England']['The Championship'],
        competitions['Germany']['Bundesliga'],
        competitions['Germany']['2. Bundesliga'],
    ]


urls = {
    '888sport': generate_888sport_urls(),
    'bet365': generate_bet365_urls(),
    'unibet': generate_unibet_urls(),
}

pprint(urls)

with open('urls.json', 'w') as f:
    json.dump(urls, f, indent=4)
