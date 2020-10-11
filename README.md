# Soccer API

[![CI Badge](https://github.com/S1M0N38/soccerapi/workflows/CI/badge.svg)](https://github.com/S1M0N38/soccer-api/actions)
[![Coverage Badge](https://api.codacy.com/project/badge/Coverage/5bad465c97414d86ba0931c40f0a2c95)](https://www.codacy.com/manual/S1M0N38/soccer-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=S1M0N38/soccer-api&amp;utm_campaign=Badge_Coverage)
[![Quality Badge](https://api.codacy.com/project/badge/Grade/5bad465c97414d86ba0931c40f0a2c95)](https://www.codacy.com/manual/S1M0N38/soccer-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=S1M0N38/soccer-api&amp;utm_campaign=Badge_Grade)
[![PyPI version](https://badge.fury.io/py/soccerapi.svg)](https://badge.fury.io/py/soccerapi)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Soccer API (Application Programming Interface) is a simple wrapper build on top
of some bookmakers (888sport, bet365 and Unibet) in order to get data about
soccer (aka football) odds using python commands.

## ⚽️ The goal

The goal of the project is provided an enjoyable way to get odds data for
different soccer leagues. Usually, if someone wants to get these types of data,
have to build by him self (and from scratch) a program able to scrape the
betting site or use some kind paid API. Soccer API try to address this problem.

## 💡 The philosophy

Keep it simple. Simple API, simple http requests, few dependencies. In the past
I have tried to build some heavy framework able to scraping site (using
selenium able to handle complex JavaScript): was an *unmaintainable nightmare*.

## 📘 The documentation

The following section contain all the useful information to use this API at
its best. Read it carefully.

### Installation

Use your favorite python package manager (like *pip*, *pipenv*, *poetry*). For
example if you use *pip* type in your terminal:

```bash
pip install soccerapi
```

------------------------------------------------------------------------------

Alternatively, if you want a kind of testing/developing setup, you can install
Soccer API directly from source code by first cloning the repository from
github and then install dev dependencies
([pipenv](https://pipenv.pypa.io/en/latest/) is required)

```bash
git clone https://github.com/S1M0N38/soccerapi.git
cd soccerapi
pip install -e .
pipenv install --dev
```

and then activate the environment

```bash
pipenv shell
```

### Usage

Import the *soccerapi* bookmaker, define the *api* variable and request
*odds*.

```python
from soccerapi.api import Api888Sport
# from soccerapi.api import ApiUnibet
# from soccerapi.api import ApiBet365

api = Api888Sport()
url = 'https://www.888sport.com/#/filter/football/italy/serie_a'
odds = api.odds(url)

print(odds)
```

```python
[
  {
    'time': '2020-01-12T19:45:00Z'
    'home_team': 'Roma',
    'away_team': 'Juventus',
    'both_teams_to_score': {'no': 2380, 'yes': 1560},
    'double_chance': {'12': 1320, '1X': 1710, '2X': 1360},
    'full_time_resut': {'1': 3200, '2': 2160, 'X': 3450},
  },

  ...

  {
    'time': '2020-01-13T19:45:00Z'
    'home_team': 'Parma',
    'away_team': 'Lecce',
    'both_teams_to_score': {'no': 2280, 'yes': 1600},
    'double_chance': {'12': 1270, '1X': 1270, '2X': 1960},
    'full_time_resut': {'1': 1850, '2': 3850, 'X': 3800},
  }
]
```

The _odds_ method return a list of next events of the request competition
(in the example: the url points to *italy-serie_a*, try to open on your
browser). To get these url, open the bookmaker site and browser to competitions
you want to scrape: that's the urls you have to pass to *odds()*.

For example urls for *england-premier_league* are:
- **bet365** `https://www.bet365.it/#/AC/B1/C1/D13/E51761579/F2/`
- **888sport** `https://www.888sport.com/#/filter/football/england/premier_league`
- **unibet** `https://www.unibet.com/betting/sports/filter/football/england/premier_league/matches`
(note that these are urls that works for me, maybe your urls are not `.it` but
`.com`)

### Country restriction

The regulation of online gambling varies from country to country. There are
different versions of the betting site depending on the provenience of your
http request. Moreover, most bookmakers implement some kind of VPN detection
that block VPN-http requests. Due to this constrains it's difficult to test
soccerapi for worldwide usability. Here is reported some results about bookmaker
accessibility from various country.

|            | bet365 | 888sport / unibet |
|----------- | :----: | :---------------: |
|accessible  | :it:   | :us: :canada: :australia: :brazil: :switzerland: :it: :de: :denmark: :es: :finland: :jp: :netherlands: :norway: :sweden: :ireland: :india: :singapore: :hong_kong: :new_zealand: :mexico: :romania:|
|inaccessible|        | :fr: :uk:         |
