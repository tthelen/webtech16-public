from server.webserver import Webserver, App, Cookie
from server.middlewares.session import SessionMiddleware
from server.apps.static import StaticApp
from model_sql import Person, Team
from urllib.parse import unquote


class PersonApp(App):

    def register_routes(self):
        self.add_route("", self.personlist)
        self.add_route("persons", self.personlist)
        self.add_route("teams", self.teamlist)
        self.add_route("ajax/persons", self.persons)
        self.add_route("ajax/person/(?P<id>[a-f0-9]+)", self.persondata)
        self.add_route("ajax/person/new/form", self.new_person_form)
        self.add_route("ajax/person/new", self.new_person)
        self.add_route("ajax/person/delete/(?P<id>[a-f0-9]+)", self.delete_person)
        self.add_route("ajax/person/deletehobby/(?P<id>[a-f0-9]+)/(?P<hobby>.+)", self.delete_hobby)
        self.add_route("ajax/person/addhobby/(?P<id>[a-f0-9]+)/(?P<hobby>.+)", self.add_hobby)
        self.add_route("ajax/person/addteam/(?P<id>[a-f0-9]+)/(?P<teamid>[a-f0-9]+)", self.add_person_team)
        self.add_route("ajax/person/deleteteam/(?P<id>[a-f0-9]+)/(?P<teamid>[a-f0-9]+)", self.delete_person_team)
        self.add_route("ajax/teams", self.teams)
        self.add_route("ajax/team/(?P<id>[a-f0-9]+)", self.teamdata)
        self.add_route("ajax/team/new/form", self.new_team_form)
        self.add_route("ajax/team/new", self.new_team)
        self.add_route("ajax/team/delete/(?P<id>[a-f0-9]+)", self.delete_team)

    def personlist(self, request, response, pathmatch):
        response.send_template("persons.mustache", {})

    def persons(self, request, response, pathmatch):
        persons = Person.find()
        response.send_template("ajax_persons.mustache", {'persons': persons})

    def persondata(self, request, response, pathmatch):
        person = Person(id=pathmatch.group('id'))
        response.send_template("ajax_persondata.mustache", {'person': [person], 'teams': person.get_teams(), 'allteams': Team.find()})

    def new_person_form(self, request, response, pathmatch):
        teams = Team.find()
        response.send_template("ajax_new_person.mustache", locals())

    def new_person(self, request, response, pathmatch):

        d=dict()

        for p in ['firstname', 'lastname', 'email']:
            if p not in request.params or not request.params[p]:
                response.send(code=400, body="<p>Nicht alle notwendigen Felder ausgefüllt. {} fehlt.</p>".format(p))
                return
            d[p]=request.params[p]

        for p in ['hobby', 'team']:
            if p in request.params and request.params[p]:
                if isinstance(request.params[p], list):
                    d[p]=request.params[p]
                else:
                    d[p]=[request.params[p]]
            else:
                d[p]=[]

        person = Person(firstname=d['firstname'], lastname=d['lastname'], email=d['email'], hobbies=d['hobby'])
        person.store()

        for tid in d['team']:
            try:
                team = Team(id=tid)
                team.add_person(person)
                team.store()
            except Exception:
                pass

        response.send(code=200, body="")

    def add_person_team(self, request, response, pathmatch):
        """Add a person to an existing team."""
        person = Person(id=pathmatch.group('id'))
        try:
            team = Team(id=pathmatch.group('teamid'))
            team.add_person(person)
            team.store()
            response.send(code=200, body="")
        except Exception: # TODO: raise better exceptions in team model class
            response.send(code=404, body="Team does not exists.")

    def delete_person_team(self, request, response, pathmatch):
        """Remove a person from an existing team."""
        person = Person(id=pathmatch.group('id'))
        try:
            team = Team(id=pathmatch.group('teamid'))
            team.remove_person(person)
            team.store()
            response.send(code=200, body="")
        except Exception: # TODO: raise better exceptions in team model class
            response.send(code=404, body="Team does not exists.")

    def delete_person(self, request, response, pathmatch):
        person = Person(id=pathmatch.group('id'))
        person.delete()
        response.send(code=200, body='')

    def add_hobby(self, request, response, pathmatch):
        person = Person(id=pathmatch.group('id'))
        hobby = unquote(pathmatch.group('hobby'))  # path parts aren't decoded by server framework
        if hobby not in person.get_hobbies():
            person.hobbies.append(hobby)
            person.store()
        response.send(code=200, body="")

    def delete_hobby(self, request, response, pathmatch):
        person = Person(id=pathmatch.group('id'))
        hobbies = person.get_hobbies()
        try:
            hobby = unquote(pathmatch.group('hobby'))  # path parts aren't decoded by server framework
            hobbies.remove(hobby)
            person.hobbies = hobbies
            person.store()
            response.send(code=200, body="")
        except ValueError:
            response.send(code=404, body="<p>Fehler: Hobby '{}' nicht gefunden.</p>".format(hobby))

    def teamlist(self, request, response, pathmatch):
        teams = Team.find()
        response.send_template("teams.mustache", {})

    def teams(self, request, response, pathmatch):
        teams = Team.find()
        response.send_template("ajax_teams.mustache", {'teams': teams})

    def teamdata(self, request, response, pathmatch):
        team = Team(id=pathmatch.group('id'))
        response.send_template("ajax_teamdata.mustache", {'team': [team], 'persons': team.members(), 'allpersons': Person.find()})

    def new_team_form(self, request, response, pathmatch):
        persons = Person.find()
        response.send_template("ajax_new_team.mustache", locals())

    def new_team(self, request, response, pathmatch):

        if 'name' not in request.params or not request.params['name']:
            response.send(code=400, body="<p>Nicht alle notwendigen Felder ausgefüllt. 'Name' fehlt.</p>")
            return

        persons = []
        if 'person' in request.params and request.params['person']:
            if isinstance(request.params['person'], list):
                persons = request.params['person']
            else:
                persons = [request.params['person']]
        team = Team(name=request.params['name'], persons=persons)

        team.store()

        response.send(code=200, body="")

    def delete_team(self, request, response, pathmatch):
        team = Team(id=pathmatch.group('id'))
        team.delete();
        response.send(code=200, body="")


if __name__ == '__main__':

    s = Webserver()
    s.set_templating("pystache")
    s.set_templating_path("templates.mustache")
    s.add_app(PersonApp())
    s.add_app(StaticApp(prefix='static', path='static'))
    s.serve()

