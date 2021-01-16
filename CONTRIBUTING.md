# How to contribute to soccerapi

At the moment the main focus is to have a stable api that can works when run
from every location. In order to solve this issue the api must be tested from
many different location across the world. It's not as simple as setting up a
VPN because many bookmaker have some sort of VPN detection (they have to verify
the location of users so they can apply the correct country gambling
regulation). You can contribute your self by run the api test suite and then
report the result [this issue](https://github.com/S1M0N38/soccerapi/issues/17)
so I can update the documentation.

## Installing the development version

[Poetry](https://python-poetry.org/) is used as package manager so you
have to install it on your local machine.

Then clone this Github repository with
```bash
git clone https://github.com/S1M0N38/soccerapi.git
```
and then go into it

```bash
cd soccerapi
```

Then install the dependencies with
```bash
poetry install
```

## Running the test suite

Go into soccerapi directory (the same directory where is README.md) and run
tests with `pipenv run pytest`.
