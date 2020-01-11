import json
import os
from typing import Dict

s = ''


def table(bookmaker: str) -> Dict:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    table_path = os.path.join(base_dir, 'api', f'{bookmaker}.json')
    with open(table_path) as f:
        table = json.load(f)
    return table


# 888sport
s += '# 888sport'

table_888sport = table('888sport')

old_country = ''
for country, value in table_888sport.items():
    if old_country != country:
        s += f'\n## {country}\n'
        old_country = country
    for league in value['leagues']:
        s += f'- {league}\n'

s += '\n------------------------------\n'

s += '# Others...'

with open('competitions.md', 'w') as f:
    f.write(s)
