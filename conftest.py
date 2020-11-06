# import os

import requests


def pytest_addoption(parser):
    parser.addoption("--ip", action="store_true")
    # parser.addoption("--proxy", action="store_true")


def pytest_sessionstart(session):
    if session.config.option.ip:
        ip_info()
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
