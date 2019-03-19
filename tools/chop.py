from pathlib import Path
import json
import time
from collections import defaultdict


def work(folder):
    days = defaultdict(list)
    p = Path(folder)
    files = list(p.glob('*.json'))
    for f in files:
        txt = f.read_text()
        chop(txt, days)
    return days


def chop(json_txt, days):
    snapshots = json.loads(json_txt)["Snapshots"]
    for snapshot in snapshots:
        t = snapshot["Time"]
        t2=time.strptime(t,'%Y-%m-%dT%H:%M:%S.%f%z')
        if t2.tm_hour >= 9 and t2.tm_hour <= 16:
            y = t2.tm_year
            m = t2.tm_mon
            d = t2.tm_mday
            day = f'{y}_{m}_{d}'
            days[day].append(snapshot)


folder = '.'
days = work(folder)
for day, snapshots in days.items():
    with open(f'{day}.json', 'w') as o:
        json.dump({"Snapshots": snapshots}, o)

# to create daily report
# $ for f in `ls 2019*`; do thyme show -i $f -w stats > $f.html; done