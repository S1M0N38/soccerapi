import os

import requests


def pytest_addoption(parser):
    parser.addoption("--proxy", action="store")


def pytest_sessionstart(session):
    proxy = session.config.option.proxy
    if proxy:
        os.environ['HTTPS_PROXY'] = proxy
        print(f'HTTPS_PROXY={os.getenv("HTTPS_PROXY")}')
    ip_info()


def ip_info():
    url = 'https://wtfismyip.com/json'
    info = requests.get(url).json()
    print(f'ip address: {info["YourFuckingIPAddress"]}')
    print(f'location: {info["YourFuckingLocation"]}')
    print(f'hostname: {info["YourFuckingHostname"]}')
    print(f'ips: {info["YourFuckingISP"]}')
    print(f'country code: {info["YourFuckingCountryCode"]}')
