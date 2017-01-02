"""Persons and Teams model using MongoDB.

Tobias Thelen, 2016
Public Domain, no rights reserved, CC-0

The model defines two classes: Persons and Teams.

Usage:

# create a new person
p = Person(firstname="Tobias", lastname="Thelen", email="tthelen@uos.de", hobbies=["singen", "tanzen", "fröhlichsein"])
# change an attribute
p['email'] = "tobias.thelen@uni-osnabrueck.de"
# save that person to database
p.store()
# print it
print(p)
> Person Tobias Thelen, tobias.thelen@uni-osnabrueck.de, hobbies: singen, tanzen, fröhlichsein

# Find persons
p2 = Person.find(firstname="Tobias")
> [<__main__.Person object at 0x00000196C1AD9080>, <__main__.Person object at 0x00000196C1ADD208>, ...]

# create a new team calles the tigers
t = team(name="The Tigers")
# add a person
t.add_person(p)
# never forget to save
t.store()
# print it:
print(t)
> Team 'The Tigers' with members: Tobias Thelen


"""

import pymongo
from bson.objectid import ObjectId

db = None


def db_setup(dbname='teamlist'):
    global db
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client[dbname]


def db_remove(dbname='teamlist'):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    client.drop_database(dbname)


class Person():
    """A Person object collects information about a person. (Name, E-Mail, Hobbies)"""

    @classmethod
    def find(cls, **kwargs):
        """Retrieves a list of Persons from db that match given criteria.

        :param firstname string If given, firstname must match.
        :param lastname string If given, lastname must match.
        :param email string If given, email must match.
        :param hobbies string or list of strings If given, hobbies must include at least one of the given hobbies."""

        return [Person(dbobj=p) for p in db['persons'].find(kwargs)]

    def __init__(self, dbobj=None, id=None, firstname=None, lastname=None, email=None, hobbies=None):
        """A Person.

        firstname string The first name
        lastname string  The last name
        email string E-Mail-Address
        hobbies list of strings Hobbies
        """
        self.data = {'firstname':'', 'lastname':'', 'email':'', 'hobbies':[]}

        if dbobj and isinstance(dbobj, dict):  # TODO: check type!
            self.data = dbobj
            return

        if id:
            self.restore(id)
        if firstname:
            self.data['firstname'] = firstname
        if lastname:
            self.data['lastname'] = lastname
        if email:
            self.data['email'] = email
        if hobbies and isinstance(hobbies, list):
            self.data['hobbies'] = hobbies

    def store(self):
        """Save a person object to database."""
        persons = db['persons']
        if '_id' in self.data and self.data['_id']:
            persons.update({'_id':self.data['_id']}, self.data)
        else:
            self.data['_id'] = persons.insert_one(self.data).inserted_id
        return self.data['_id']

    def restore(self, id):
        """Read a person object from database given its ID."""
        persons = db['persons']
        p = persons.find_one({'_id':ObjectId(id)})
        if not p:
            print("No person found!")
        else:
            self.data = p

    def get_teams(self):
        """Find all teams this person is member of.

        :return List of Team objects."""

        return Team.find_teams_by_members(self)

    def __getitem__(self, item):
        """Direct access to data properties.

        Enables name = p['firstname']
        """
        if item == 'id':
            return self.data.get('_id', None)
        return self.data.get(item, None)

    def __getattr__(self, item):
        """Direct access to data properties.

           Enables name = p.firstname
        """
        if item == 'data':
            return self.data
        if item == 'id':
            return self.data.get('_id', None)
        return self.data.get(item, None)

    def __setitem__(self, key, value):
        """Direct access to data properties.

        Enables p['firstname'] = 'Tobias'
        """
        if key == 'id':
            key = '_id'
        self.data[key] = value

    def __contains__(self, item):
        """Direct access to data properties.

        Enables if 'firstname' in p: ..."""
        if item=='id':
            return '_id' in self.data
        return item in self.data

    def __str__(self):
        out = "Person {} {}, {}".format(self.data['firstname'], self.data['lastname'], self.data['email'])
        if 'hobbies' in self.data:
            out += ", hobbies: "
            out += ", ".join(self.data['hobbies'])
        return out


class Team:
    """A Team is a named collection of persons. A team has a name.

    :param dbobj Database query result used to initialise object
    :param id  the Team's ID, either String or ObjectId. If given, object will be read from DB
    :param name  string  The team name for new objects
    :param persons  list of Person objects or ObjectIds
    """

    @classmethod
    def find(cls, **kwargs):
        """Retrieves a list of Persons from db that match given criteria.

        :param name string If given, name must match."""

        return [Team(dbobj=t) for t in db['teams'].find(kwargs)]

    @classmethod
    def find_teams_by_members(cls, persons):
        """Find all teams that contain all persons (1 or more) given.

        :param persons Person or List of Persons
        :return List of Team objects
        """
        teams = db['teams']
        if isinstance(persons, Person):
            personlist = [persons['_id']]
        else:
            personlist = [p['_id'] for p in persons]
        return [Team(dbobj=t) for t in teams.find({'persons': {'$all': personlist}})]

    def __init__(self, dbobj=None, id=None, name=None, persons=None):
        self.data = dict()

        if dbobj:  # initialise object from db query result
            self.data=dbobj
            return

        if id:  # read from Database, id is given
            self.restore(id)
        else:  # new object, initialize with given arguments
            if name:
                # set team name
                self.data['name'] = name
            if persons and isinstance(persons, list):
                # set persons list (either Person objects or ObjectIds
                if persons == []:
                    self.data['persons'] = []
                elif isinstance(persons[0], Person):
                    # if list contains person objects: Only take their IDs
                    self.data['persons'] = [p['_id'] for p in persons]
                else:
                    # we assume that list contains ObjectIds... TODO: real check
                    self.data['persons'] = persons

    def restore(self, db_id):
        """Read team object from database.

        DB data is stored in data member variable. Team members are included
        as list of person-IDs.
        """
        teams = db['teams']

        if isinstance(db_id, ObjectId):
            id = db_id  # id given as ObjectId
        else:
            id = ObjectId(db_id)  # id given as string

        t = teams.find_one({'_id': id})
        if not t:
            print("No team found!") # TODO: raise exception
        else:
            self.data = t

    def store(self):
        """Write team object to database."""
        teams = db['teams']
        if '_id' in self.data and self.data['_id']:
            teams.update({'_id':self.data['_id']}, self.data)
        else:
            self.data['_id'] = teams.insert_one(self.data).inserted_id
        return self.data['_id']

    def add_person(self, person):
        """Add a person to a team.

        :param person Person object, ObjectId or string  The person (or person ID) to add.
        """
        if isinstance(person, Person):
            p_id = person['_id']
        elif isinstance(person, ObjectId):
            p_id = person
        else:
            p_id = ObjectId(person)
        self.data['persons'].append(p_id)

    def remove_person(self, person):
        """Remove a person from a team.

        :param person Person object, ObjectId or string  The person (or person ID) to add.
        """
        if isinstance(person, Person):
            p_id = person['_id']
        elif isinstance(person, ObjectId):
            p_id = person
        else:
            p_id = ObjectId(person)
        self.data['persons'].remove(p_id)

    def members(self):
        """Get list of Persons.

        :return List of Persons"""

        return [Person(id=p) for p in self.data['persons']]

    def __str__(self):
        return "Team '{}' with members: {}".format(self.data['name'], ", ".join([p['firstname']+" "+p['lastname'] for p in self.members()]))

    def __getattr__(self, item):
        """Direct access to data properties.

           Enables name = p.firstname
        """
        if item == 'data':
            return self.data
        if item == 'id':
            return self.data.get('_id', None)
        return self.data.get(item, None)

    def __setitem__(self, key, value):
        """Direct access to data properties.

        Enables p['firstname'] = 'Tobias'
        """
        if key == 'id':
            key = '_id'
        self.data[key] = value

    def __contains__(self, item):
        """Direct access to data properties.

        Enables if 'firstname' in p: ..."""
        if item=='id':
            return '_id' in self.data
        return item in self.data


if __name__== '__main__':
    tobias = Person(firstname='Tobias', lastname='Thelen', email='tobias.thelen@uni-osnabrueck.de')
    tobias['hobbies'] = ['Briefmarken sammeln', 'Brieftauben züchten', 'Briefumschläge falten']
    tobias.store()
    walter = Person(firstname='Walter', lastname='Sparbier', email='walter.sparbier@uni-meppen.de')
    walter['hobbies'] = ['Singen', 'Springen']
    walter.store()
    hans = Person(firstname='Hans', lastname='Wurst', email='hans.wurst@uni-meppen.de')
    hans['hobbies'] = ['Brieftauben züchten', 'Singen']
    hans.store()

    tigers = Team(name="tigers", persons=[tobias, hans, walter])
    tigers.store()
    lions = Team(name="lions", persons=[walter, hans])
    lions.store()

    for i in Team.find_teams_by_members(tobias):
        print(i.data)

    for i in Person(id = str(tobias.data['_id'])).get_teams():
        print(i)

    for i in Person.find(firstname="Tobias"):
        print(i)
        print(i.get_teams())

    print(Person.find(firstname="Tobias"))
