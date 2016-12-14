import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['the-test']

db['staedte'].insert( { 'name': 'Osnabrück', 'inhabitants': 170000,
                        'quarters': [ 'Wüste', 'Hellern', 'Voxtrup'],
                      'sights': [ { 'name': 'Rathaus', 'age': 505 },
                                  { 'name': 'Schloss', 'age': 449 }]})

db['staedte'].insert( { 'name': 'Bramsche', 'inhabitants': 32000,
                        'quarters': [ 'Bramsche', 'Engter', 'Kalkriese'],
                      'sights': [ { 'name': 'Varus-Schlacht', 'age': 2007 }]})

for i in db['staedte'].find({ 'sights.age': {'$gt': 800}}):
    print(i)
