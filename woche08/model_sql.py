"""Persons and Teams model using SQLite.

Tobias Thelen, 2016
Public Domain, no rights reserved, CC-0

The model defines two classes: Persons and Teams.

Usage:

# initialize databse
db_setup()
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

import sqlite3

conn = None  # the databse connection


def db_setup(dbname='teamlist.db'):
    """Initialize databse.

    :param: dbname string the name of the sqlite database file.
    """
    global conn

    sql_create_person_table = """ CREATE TABLE IF NOT EXISTS person (
                                          id integer PRIMARY KEY,
                                          firstname text NOT NULL,
                                          lastname text NOT NULL,
                                          email text NOT NULL
                                      ); """

    sql_create_hobby_table = """CREATE TABLE IF NOT EXISTS hobby (
                                      id integer PRIMARY KEY,
                                      person_id integer NOT NULL,
                                      name text NOT NULL,
                                      FOREIGN KEY (person_id) REFERENCES person (id)
                                  );"""

    sql_create_team_table = """CREATE TABLE IF NOT EXISTS team (
                                      id integer PRIMARY KEY,
                                      name text NOT NULL
                                  );"""

    sql_create_team_member_table = """CREATE TABLE IF NOT EXISTS team_member (
                                      id integer PRIMARY KEY,
                                      person_id integer NOT NULL,
                                      team_id integer NOT NULL,
                                      FOREIGN KEY (team_id) REFERENCES team (id),
                                      FOREIGN KEY (person_id) REFERENCES person (id)
                                  );"""

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    conn = sqlite3.connect(dbname)
    conn.row_factory = dict_factory
    conn.execute(sql_create_person_table)
    conn.execute(sql_create_team_table)
    conn.execute(sql_create_hobby_table)
    conn.execute(sql_create_team_member_table)
    conn.commit()


def db_shutdown():
    global conn
    conn.close()


class Person():
    """A Person object collects information about a person. (Name, E-Mail, Hobbies)"""

    @classmethod
    def find(cls, **kwargs):
        """Retrieves a list of Persons from db that match given criteria.

        :param firstname string If given, firstname must match.
        :param lastname string If given, lastname must match.
        :param email string If given, email must match.
        """

        sql = "SELECT * FROM person WHERE 1 "
        params = []
        for k,v in kwargs.items():
            sql += "AND {} = ? ".format(k)  # save because python kwargs cannot contain malicious sql
            params.append(v)

        persons = [Person(dbobj=row) for row in conn.execute(sql, params)]
        conn.commit()
        return persons

    def __init__(self, dbobj=None, id=None, firstname=None, lastname=None, email=None, hobbies=None):
        """A Person.

        firstname string The first name
        lastname string  The last name
        email string E-Mail-Address
        hobbies list of strings Hobbies
        """
        self.data = {'firstname': '', 'lastname': '', 'email': '', 'hobbies': []}

        if dbobj and isinstance(dbobj, dict):
            self.data = dbobj
            self.get_hobbies()
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
        if 'id' in self.data and self.data['id']:
            self.data['id'] = int(self.data['id'])  # make sure id is an integer
            sql = "UPDATE person SET firstname=:firstname, lastname=:lastname, email=:email WHERE id=:id"
            conn.execute(sql, self.data)
            conn.commit()
            self.write_hobbies()
        else:
            sql = "INSERT INTO person (firstname, lastname, email) VALUES (:firstname, :lastname, :email)"
            cursor = conn.cursor()
            cursor.execute(sql, self.data)
            conn.commit()
            self.data['id'] = cursor.lastrowid  # get autoincremenet id of last insert
            self.write_hobbies()

        return self.data['id']

    def restore(self, id):
        """Read a person object from database given its ID."""
        id = int(id)  # make sure id is an integer
        sql = "SELECT * FROM person WHERE id=?"
        self.data = conn.execute(sql, [id]).fetchone()  # a row
        self.get_hobbies()

    def get_teams(self):
        """Find all teams this person is member of.

        :return List of Team objects."""

        return Team.find_teams_by_members(self)

    def get_hobbies(self):
        """Retrieve list of hobbies for a person from db."""
        sql="SELECT * FROM hobby WHERE person_id=?"
        self.data['hobbies'] = []
        for row in conn.execute(sql, [int(self.data['id'])]):
            self.data['hobbies'].append(row['name'])
        return self.data['hobbies']

    def write_hobbies(self):
        """Write list of hobbies for a person First delete all hobbies, then rewrite list."""
        sql="DELETE FROM hobby WHERE person_id=?"
        conn.execute(sql, [int(self.data['id'])])
        for h in self.data['hobbies']:
            sql = "INSERT INTO hobby (person_id, name) VALUES (?,?)"
            conn.execute(sql, (int(self.data['id']), h))
        conn.commit()

    def __getitem__(self, item):
        """Direct access to data properties.

        Enables name = p['firstname']
        """
        return self.data.get(item, None)

    def __getattr__(self, item):
        """Direct access to data properties.

           Enables name = p.firstname
        """
        if item == 'data':
            return self.data
        return self.data.get(item, None)

    def __setitem__(self, key, value):
        """Direct access to data properties.

        Enables p['firstname'] = 'Tobias'
        """
        self.data[key] = value

    def __contains__(self, item):
        """Direct access to data properties.

        Enables if 'firstname' in p: ..."""
        return item in self.data

    def __str__(self):
        out = "Person {} {}, {}".format(self['firstname'], self['lastname'], self['email'])
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
    def find_teams_by_members(cls, persons):
        """Find all teams that contain all persons (1 or more) given.

        :param persons Person or List of Persons
        :return List of Team objects
        """
        if isinstance(persons, Person): # either a single Person object
            personlist=[persons['id']]
        else:
            personlist=[p['id'] for p in persons]  # or a list of Person object
        first = True
        sql = ""
        params = []
        for p in personlist:
            if first:
                sql = "SELECT team_id as tid FROM team_member WHERE person_id=? "
                first = False
            else:
                sql += "LEFT JOIN team_member ON (team_id = tid) WHERE person_id=? "
            params.append(int(p))
        teamlist = []
        for row in conn.execute(sql, params):
            teamlist.append(Team(id=row['tid']))
        return teamlist

    @classmethod
    def find(cls, **kwargs):
        """Retrieves a list of Teams from db that match given criteria.

        :param name string If given, name must match.
        """

        sql = "SELECT * FROM team WHERE 1 "
        params = []
        for k,v in kwargs.items():
            sql += "AND {} = ? ".format(k)  # save because python kwargs cannot contain malicious sql
            params.append(v)

        teams = [Team(dbobj=row) for row in conn.execute(sql, params)]
        conn.commit()
        return teams


    def __init__(self, dbobj=None, id=None, name=None, persons=None):
        self.data = dict()

        if dbobj:  # initialise object from db query result
            self.data = dbobj
            self.get_persons()
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
                    self.data['persons'] = [p['id'] for p in persons]
                else:
                    # we assume that list contains ids... TODO: real check
                    self.data['persons'] = persons

    def restore(self, db_id):
        """Read team object from database.

        DB data is stored in data member variable. Team members are included
        as list of person-IDs.
        """
        db_id=int(db_id)  # make sure it's an integer
        sql = "SELECT * FROM team WHERE id=?"
        self.data = None
        for row in conn.execute(sql, [db_id]):
            self.data = row
        if not self.data:
            raise Exception("No such team id.")
        self.get_persons()

    def store(self):
        """Write team object to database."""

        if 'id' in self.data and self.data['id']:
            self.data['id'] = int(self.data['id'])  # make sure id is an integer
            sql = "UPDATE team SET name=:name WHERE id=:id"
            conn.execute(sql, self.data)
            conn.commit()
            self.write_persons()
        else:
            sql = "INSERT INTO team (name) VALUES (:name)"
            cursor = conn.cursor()
            cursor.execute(sql, self.data)
            conn.commit()
            self.data['id'] = cursor.lastrowid  # get autoincremenet id of last insert
            self.write_persons()

        return self.data['id']

    def add_person(self, person):
        """Add a person to a team.

        :param person Person object, ObjectId or string  The person (or person ID) to add.
        """
        if isinstance(person, Person):
            p_id = person['id']
        else:
            p_id = person
        self.data['persons'].append(p_id)

    def remove_person(self, person):
        """Remove a person from a team.

        :param person Person object, ObjectId or string  The person (or person ID) to add.
        """
        if isinstance(person, Person):
            p_id = person['id']
        else:
            p_id = person
        self.data['persons'].remove(p_id)

    def get_persons(self):
        """Retrieve list of person ids from db."""

        # TODO: This is inefficient - now members() performs unnecessary queries
        self.data['persons'] = []
        sql = "SELECT person_id FROM team_member WHERE team_id=?"
        for row in conn.execute(sql, [int(self.data['id'])]):
            self.data['persons'].append(int(row['person_id']))
        conn.commit()
        return self.data['persons']

    def write_persons(self):
        sql="DELETE FROM team_member WHERE team_id=?"
        conn.execute(sql, [int(self.data['id'])])
        for p_id in self.data['persons']:
            sql = "INSERT INTO team_member (team_id, person_id) VALUES (?,?)"
            conn.execute(sql, (int(self.data['id']), p_id))
        conn.commit()

    def members(self):
        """Get list of Persons.

        :return List of Persons"""

        return [Person(id=p) for p in self.data['persons']]

    def __str__(self):
        """Printable representation"""
        return "Team '{}' with members: {}".format(self.data['name'], ", ".join([p['firstname']+" "+p['lastname'] for p in self.members()]))

    def __getattr__(self, item):
        """Direct access to data properties.

           Enables name = p.firstname
        """
        if item == 'data':
            return self.data
        return self.data.get(item, None)


if __name__== '__main__':
    db_setup()
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
    lions = Team(name="lions", persons=[walter, walter])
    lions.store()


    print("Teams mit Tobias:\n=================")
    for i in Team.find_teams_by_members(tobias):
        print(i)

    print("Tobias' Teams:\n==============")
    for i in Person(id = tobias['id']).get_teams():
        print(i)

    print("Alle Personen mit Vorname Tobias:\n===============================")
    for i in Person.find(firstname="Tobias"):
        print(i)
