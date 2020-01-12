# API

Before use Soccer API (soccerapi), first you need to install it.

## Installation

Use your favorite python package manager (like *pip*, *pipenv*, *poetry*). For
example if you use *pip* type in your terminal:

```bash
pip install soccerapi
```

done.

Alternatively, you can also install Soccer API directly from source code by
first cloning the repository from github

```bash
git clone https://github.com/S1M0N38/soccerapi.git
```

then move into the cloned directory and run setup.py

```bash
cd soccerapi && python setup.py
```

## Usage

Import the *soccerapi* bookmaker, define the *api* varibale, reuquest the *odds*.

```python
from soccerapi.api import Api888Sport

api = Api888Sport()
odds = api.odds('italy', 'serie_a')

"""
>>> print(odds)
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
"""
```

the *odds* is a list of next event of the request competition. For a complete
list of supported bookmakers and releated competitons visit the [competitons
section](https://s1m0n38.github.io/soccerapi/#/competitions) of the
documentation.
