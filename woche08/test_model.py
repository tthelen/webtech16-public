import unittest
import os, uuid

DB = 'sqlite'

if DB == 'sqlite':
    import model_sql as model
    DB_NAME = ':memory:'
elif DB == 'mongodb':
    import model_mongodb as model
    DB_NAME = '___TEST___'
else:
    raise "No such db driver: {}".format(DB)


class TestPerson(unittest.TestCase):

    def setUp(self):
        global DB_NAME
        model.db_setup(DB_NAME)  # in-memory db for testing

    def tearDown(self):
        if DB == 'mongodb':
            model.db_remove(DB_NAME)

    def test_createperson(self):
        """Create a person and check if it can be retrieved completely by id lookup."""
        p = model.Person(firstname="Tobias", lastname="Thelen",
                         email="tthelen@uos.de", hobbies=["singen","springen","fröhlichsein"])
        id = p.store()

        p2 = model.Person(id=id)
        self.assertEqual(p.id, p2.id)
        self.assertEqual(p.firstname, p2.firstname)
        self.assertEqual(p.lastname, p2.lastname)
        self.assertEqual(p.email, p2.email)
        self.assertEqual(p.hobbies, p2.hobbies)

    def test_findperson(self):
        """Check if static find method find the correct number of persons."""
        p = model.Person(firstname="Tobias", lastname="Thelen",
                         email="tthelen@uos.de", hobbies=["singen","springen","fröhlichsein"])
        p.store()
        p = model.Person(firstname="Tobias", lastname="Müller",
                         email="tmueller@test.test", hobbies=["rappen", "hüpfen", "lustigsein"])
        p.store()

        persons = model.Person.find(firstname="Tobias")
        self.assertEqual(len(persons), 2)

    def test_changedata(self):
        """Check if changing data works."""
        p = model.Person(firstname="Tobias", lastname="Thelen",
                         email="tthelen@uos.de", hobbies=["singen","springen","fröhlichsein"])
        id = p.store()

        p = model.Person(id=id)
        p['firstname'] = "Walter"
        p.store()

        p2 = model.Person(id=id)
        self.assertEqual(p2.firstname, "Walter")
        self.assertEqual(p2.lastname, "Thelen")

    def test_createteam(self):
        """Check if a created team is retrieved completely after storing and restoring by id."""
        p1, p2, p3 = self.create3persons()
        t = model.Team(name='Tigers', persons=[p1, p2, p3])
        id = t.store()
        t2 = model.Team(id=id)
        self.assertEqual(t.name, t2.name)
        self.assertEqual(t.persons, t2.persons)

    def test_findbymembers(self):
        """Check if team can be found by members."""
        p1, p2, p3 = self.create3persons()
        model.Team(name='Tigers', persons=[p1, p2, p3]).store()
        model.Team(name='Lions', persons=[p1,p2]).store()
        model.Team(name='Snakes', persons=[p2, p3]).store()

        teams = model.Team.find_teams_by_members(p1)  # find all teams with p1 (2)
        self.assertEqual(len(teams), 2)

    def test_removeperson(self):
        """Check if removing a person works."""
        p1, p2, p3 = self.create3persons()
        t = model.Team(name='Tigers', persons=[p1, p2, p3])
        id = t.store()
        t.remove_person(p2)
        t.store()

        t2 = model.Team(id=id)
        self.assertEqual(t2.persons, [p1.id, p3.id])

        with self.assertRaises(ValueError):  # cannot be removed again
            t2.remove_person(p2)

    def create3persons(self):
        """Helper function. Creates three persons."""
        p1 = model.Person(firstname="A1", lastname="B1", email="C1", hobbies=["X"])
        p2 = model.Person(firstname="A2", lastname="B2", email="C2", hobbies=["Y", "X"])
        p3 = model.Person(firstname="A3", lastname="B3", email="C3", hobbies=["Z", "Y"])
        p1.store()
        p2.store()
        p3.store()
        return p1, p2, p3


if __name__=='__main__':
    unittest.main()