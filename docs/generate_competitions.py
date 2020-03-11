import json
import os
from typing import Dict

s = ''


def table(bookmaker: str) -> Dict:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    table_path = os.path.join(base_dir, 'soccerapi', 'api', f'{bookmaker}.json')
    with open(table_path) as f:
        table = json.load(f)
    return table


# 888sport
s += '# [Api888Sport](http://888sport.com/)'

s += (
    '\n?> accessible from: '
    ':us: '
    ':canada: '
    ':australia: '
    ':brazil: '
    ':switzerland: '
    ':it: '
    ':de: '
    ':denmark: '
    ':es: '
    ':finland: '
    ':jp:'
    ':netherlands: '
    ':norway: '
    ':sweden: '
    ':ireland: '
    ':india: '
    ':singapore: '
    ':hong_kong: '
    ':new_zealand: '
    ':mexico: '
    ':romania: '
    '\n'
)

s += '\n?> inaccessible from: ' ':fr:' ':uk:' '\n'

table_888sport = table('888sport')

old_country = ''
for country, value in table_888sport.items():
    if old_country != country:
        s += f'\n## {country}\n'
        old_country = country
    for league, value in value['leagues'].items():
        s += f'- [{league}](https://s5.sir.sportradar.com/888sport/en/1/season/{value["id"]})\n'

s += '\n------------------------------\n'

# bet365
s += '# [ApiBet365](http://bet365.com/)'

s += '\n?> accessible from: ' ':it: ' '\n'

table_888sport = table('bet365')

old_country = ''
for country, value in table_888sport.items():
    if old_country != country:
        s += f'\n## {country}\n'
        old_country = country
    for league, value in value['leagues'].items():
        s += f'- [{league}](https://s5.sir.sportradar.com/bet365/en/1/season/{value["id"]})\n'

s += '\n------------------------------\n'

# unibet
s += '# [ApiUnibet](http://unibet.com/)'

s += (
    '\n?> accessible from: '
    ':us: '
    ':canada: '
    ':australia: '
    ':brazil: '
    ':switzerland: '
    ':it: '
    ':de: '
    ':denmark: '
    ':es: '
    ':finland: '
    ':jp:'
    ':netherlands: '
    ':norway: '
    ':sweden: '
    ':ireland: '
    ':india: '
    ':singapore: '
    ':hong_kong: '
    ':new_zealand: '
    ':mexico: '
    ':romania: '
    '\n'
)

s += '\n?> inaccessible from: ' ':fr:' ':uk:' '\n'

table_888sport = table('888sport')

old_country = ''
for country, value in table_888sport.items():
    if old_country != country:
        s += f'\n## {country}\n'
        old_country = country
    for league, value in value['leagues'].items():
        s += f'- [{league}](https://s5.sir.sportradar.com/unibet/en/1/season/{value["id"]})\n'

s += '\n------------------------------\n'

with open('competitions.md', 'w') as f:
    f.write(s)
