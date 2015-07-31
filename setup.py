
from pymongo import MongoClient
import glob
import json
from pprint import pprint

client = MongoClient()
db = client.database
card_db = db.card_db

# Clean db
#card_db.remove()

for f in glob.glob('json/*.json'):
	with open(f) as data_file:
		locale = f.split('/')[-1].split('.')[0]
		data = json.load(data_file)

	# Repopulate db
	for value in data['data'].values():
		card_db.update({'id' : value['id'], 'locale' : locale}, value, upsert=True)

