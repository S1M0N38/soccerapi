import json
import pathlib

import requests

from soccerapi.api import Api888Sport, ApiBet365, ApiUnibet

# import os


def pytest_addoption(parser):
    parser.addoption("--ip", action="store_true")
    parser.addoption("--urls", action="store_true")
    # parser.addoption("--proxy", action="store_true")


def pytest_sessionstart(session):
    if session.config.option.ip:
        ip_info()
    if session.config.option.urls:
        generate_urls()
    # if session.config.option.proxy:
    #     config_proxy()


def ip_info():
    url = 'https://wtfismyip.com/json'
    info = requests.get(url).json()
    print(f'ip address: {info["YourFuckingIPAddress"]}')
    print(f'location: {info["YourFuckingLocation"]}')
    print(f'hostname: {info["YourFuckingHostname"]}')
    print(f'ips: {info["YourFuckingISP"]}')
    print(f'country code: {info["YourFuckingCountryCode"]}')


# def config_proxy():
#     if os.getenv('HTTP_PROXY') is None:
#         proxy = os.environ['PROXY']
#         username = os.environ['PROXY_USERNAME']
#         password = os.environ['PROXY_PASSWORD']
#         os.environ['HTTPS_PROXY'] = f'http://{username}:{password}@{proxy}/'
#     print('HTTPS_PROXY environment variable has been set')


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
    response = requests.get('http://localhost:5000/bet365').json()
    api = ApiBet365(response['headers'], response['cookies'])
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


def generate_urls():

    urls = {
        '888sport': generate_888sport_urls(),
        'bet365': generate_bet365_urls(),
        'unibet': generate_unibet_urls(),
    }

    print('Successfully generated urls for testing')

    here = pathlib.Path(__file__).parent.absolute()
    filename = here / 'soccerapi' / 'tests' / 'urls.json'
    with open(filename, 'w') as f:
        json.dump(urls, f, indent=4)
