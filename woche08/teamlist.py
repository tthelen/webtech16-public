from server.webserver import Webserver, App, Cookie
from server.middlewares.session import SessionMiddleware
from server.apps.static import StaticApp

DB='sqlite'  # which database driver to use (mongodb, sqlite)

if DB=='mongodb':
    from model_mongodb import db_setup, Person, Team
    db_setup()
elif DB == 'sqlite':
    from model_sql import db_setup, Person, Team
    db_setup()
else:
    raise "No such database driver: {}.".format(DB)


class PersonApp(App):

    def register_routes(self):
        self.add_route("", self.personlist)
        self.add_route("persons", self.personlist)
        self.add_route("teams", self.teamlist)
        self.add_route("ajax/persons", self.persons)
        self.add_route("ajax/person/(?P<id>[a-f0-9]+)", self.persondata)
        self.add_route("ajax/teams", self.teams)
        self.add_route("ajax/team/(?P<id>[a-f0-9]+)", self.teamdata)

    def personlist(self, request, response, pathmatch):
        response.send_template("persons.mustache", {})

    def persons(self, request, response, pathmatch):
        persons = Person.find()
        response.send_template("ajax_persons.mustache", {'persons': persons})

    def persondata(self, request, response, pathmatch):
        person = Person(id=pathmatch.group('id'))
        response.send_template("ajax_persondata.mustache", {'person': [person], 'teams': person.get_teams()})

    def teamlist(self, request, response, pathmatch):
        teams = Team.find()
        response.send_template("teams.mustache", {})

    def teams(self, request, response, pathmatch):
        teams = Team.find()
        response.send_template("ajax_teams.mustache", {'teams': teams})

    def teamdata(self, request, response, pathmatch):
        team = Team(id=pathmatch.group('id'))
        print(team.members()[0])
        response.send_template("ajax_teamdata.mustache", {'team': [team], 'persons': team.members()})



if __name__=='__main__':
    s = Webserver()
    s.set_templating("pystache")
    s.set_templating_path("templates.mustache")
    s.add_app(PersonApp())
    s.add_app(StaticApp(prefix='static', path='static'))
    s.serve()

