> :warning:
> At the moment this project is not actively developed. 
> Due to bookmakers' sites update some functionality may be broken.
> :warning:

# soccerapi

[![PyPI version](https://badge.fury.io/py/soccerapi.svg)](https://badge.fury.io/py/soccerapi)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Soccerapi (Application Programming Interface) is a simple wrapper build on top
of some bookmakers (888sport, bet365 and Unibet) in order to get data about
soccer (aka football) odds using python commands.

## ⚽️ The goal

The goal of the project is to provide an enjoyable way to get odds data for
different soccer leagues. If you want to get these types of data you usually
have to build a program by yourself (and from scratch) being able to scrape the
betting site or to use some kind of paid API. Soccer API try to address this problem.

## 💡 The philosophy

Keep it simple. Simple API, simple http requests, few dependencies. In the past
we tried to build some heavy framework, able to scrape dinamic sites (using
selenium, handling complex JavaScript): was an *unmaintainable nightmare*.

## 📘 The documentation

The following section contain all the useful information to use this API at
its best. Read it carefully.

### Installation

Use your favorite python package manager (like *pip*, *pipenv*, *poetry*). For
example if you use *pip* type in your terminal:

```bash
pip install --upgrade soccerapi
```

It's important to keep soccerapi updated to the last version because bookmakers
sometimes change their website so soccerapi could break. We the last version on
the master branch we try to keep up.

------------------------------------------------------------------------------

Alternatively, if you want a kind of testing/developing setup, you can install
soccerapi directly from source code by first cloning the repository from
GitHub and then install dev dependencies
([poetry](https://python-poetry.org/) is required)

```bash
git clone https://github.com/S1M0N38/soccerapi.git
cd soccerapi
poetry install
```

Finally activate the environment

```bash
poetry shell
```

------------------------------------------------------------------------------

In order to obtain data from [Bet365](https://www.bet365.com/) you need to 
run a docker which posts on a local server a needed header to make requests
to the Bet365 api. The docker run separeately from the api since it is written
in JavaScript and it runs a *chromedirver* to run JavaScript and acquire the
header.

Checkout [soccerapi-server](https://github.com/S1M0N38/soccerapi-server) to 
install the docker and run it.

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

The *odds()* method return a list of next events of the request competition
(in the example: the url points to *italy-serie_a*)

To get a dict of valid urls that you can pass to `odds()` use the method
`competitions()`.

```python
odds = api.competitions()

print(odds)
```

```python
{

'Algeria': {
    'Ligue 1': 'https://www.888sport.com/#/filter/football/algeria/ligue_1',
    'Ligue 1 U21': 'https://www.888sport.com/#/filter/football/algeria/ligue_1_u21'
},

'Argentina': {
    'Primera D Metropolitana': 'https://www.888sport.com/#/filter/football/argentina/primera_d_metropolitana'
},

'Australia': {
    'A-League': 'https://www.888sport.com/#/filter/football/australia/a-league',
    'W-League (W)': 'https://www.888sport.com/#/filter/football/australia/w-league__w_'
},

...

}
```

This python dict is dynamically generated every time the `competitions()` method
is run.  This method crawls the bookmaker site looking for the available
competitions and extract the url for every competitions offered by the bookmaker.

For some bookmakers (Bet365) many http requests are perform by `competitions()`,
so there is the risk of receiving an IP ban. Use this method wisely
(e.g. store the competitions in a json file and update them only when necessary).

The main reasons we introduced the `competitions()` method is due to the fact that 
some bookmakers (Bet365) change the url for a competitions over time in order to 
contrast bot scraping, so do not trust on a static list of urls for every bookmaker.

### Country restriction

The regulation of online gambling varies from country to country. There are
different versions of the bookmaker site depending on the provenience of your
http request. Moreover, most bookmakers implement some kind of VPN detection
which block VPN-http requests. Due to this constrains it's difficult to test
soccerapi for worldwide usability. In the following are reported some results
of the availability of bookmaker in different countries.

|            | bet365 | 888sport / unibet |
|----------- | :----: | :---------------: |
|accessible  | :it: :brazil:  | :us: :canada: :australia: :brazil: :switzerland: :it: :de: :denmark: :es: :finland: :jp: :netherlands: :norway: :sweden: :ireland: :india: :singapore: :hong_kong: :new_zealand: :mexico: :romania:|
|inaccessible|        | :fr: :uk:         |

### Contributing

If you like to contribute to the project read
[CONTRIBUTING.md](https://github.com/S1M0N38/soccerapi/blob/master/CONTRIBUTING.md)
