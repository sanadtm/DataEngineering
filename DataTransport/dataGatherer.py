from urllib import request, error
from urllib import request, error
import csv, json

BASE = "https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id="
INPUT = "allIds.csv"
OUTPUT = "glitch_all_data.json"

def get_ids(file):
    with open(file) as f:
        return [i for row in csv.reader(f) for i in row if i.strip().isdigit()]

def fetch(vid):
    try:
        with request.urlopen(BASE + vid) as r:
            return json.loads(r.read().decode())
    except error.HTTPError as e:
        print(f"{vid} error: {e.code}")
    except Exception as e:
        print(f"{vid} error: {e}")
    return []

data = []
for vid in get_ids(INPUT):
    print(f"Getting {vid}")
    data.extend(fetch(vid))

with open(OUTPUT, 'w') as out:
    json.dump(data, out)
    print(f"Saved {len(data)} records to {OUTPUT}")
