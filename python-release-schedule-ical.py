#!/bin/python3

import re
import requests
import sys
from bs4 import BeautifulSoup
from ics import Calendar, Event
import dateutil.parser

python_version_pep = {
    '3.5': 'pep-0478',
    '3.6': 'pep-0494',
    '3.7': 'pep-0537',
    '3.8': 'pep-0569',
    '3.9': 'pep-0596',
}

pep_url = 'https://www.python.org/dev/peps/'


def uid(name):
    user = re.sub(r'[^a-z0-9\.]+', '', name.lower())
    return f'{user}@python.org'


c = Calendar()


for version, pep in python_version_pep.items():
    url = pep_url + pep
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    for item in soup.find("div", {"id": "release-schedule"}).find_all("li"):
        try:
            name, start_date = item.text.splitlines()[0].split(':')
            if not name.startswith('Python '):
                name = f'Python {name}'
            e = Event(name=name, uid=uid(name), url=url)
            e.begin = dateutil.parser.parse(start_date)
            e.make_all_day()
            c.events.add(e)
        except Exception:
            print(f'Warning: Cannot parse {item.text!r}', file=sys.stderr)

with open('python-releases.ics', 'w') as my_file:
    my_file.writelines(c)
