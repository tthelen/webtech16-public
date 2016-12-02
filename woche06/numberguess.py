'''
Created on May 16, 2011

@author: tobias
'''

from server.webserver import Webserver, App, Cookie
from server.middlewares.session import SessionMiddleware
from server.apps.static import StaticApp
import os


class GuessNumberModel:
    """Chooses a random number to guess, maintains counter and
       compares guesses to random number."""
    
    def __init__(self, num=0, count=0):
        """Constructs Model from scratch or from known values."""
        
        if num == 0: # find new random number, reset counter
            from random import randint
            self.num = randint(1,100)
            self.count = 0
        else: # fill from given values
            self.num = int(num) # TODO: error handling
            self.count = int(count) # TODO: error handling
            
    def guess(self, guess):
        """Compares guess and stored number to guess. Increases counter.
           Returns tuple of (Found?, Message to display)."""
        if guess < 1 or guess > 100:
            return (False, '')
        
        self.count +=1
        if self.num < guess:
            return (False, "Die gesuchte Zahl ist kleiner als %d." % (guess))
        elif self.num > guess:
            return (False, "Die gesuchte Zahl ist größer als %d." % (guess))
        else:
            self.count=0
            return (True, "Herzlichen Glückwunsch! %d war richtig geraten!" % (guess))
        

class WelcomeApp(App):

    def register_routes(self):
        self.add_route("", self.start)

    def start(self, request, response, pathmatch):
        response.send_template('start.tmpl',{})


theGuesser = None

class GlobalGuessApp(App):
    """Transport state using a global server object."""

    def register_routes(self):
        self.add_route("", self.globalGuess)

    def globalGuess(self, request, response, pathmatch):
        """Controller for number guesser using cookies."""

        global theGuesser
        if not theGuesser: # no global model object
            theGuesser = GuessNumberModel() # generate new number
            newmsg = 'Neue Nummer generiert!'
        else:
            newmsg=''

        try: # access guessed number from form
            guess = int(request.params['guess'])
        except KeyError:
            guess = -1

        # evaluate guess
        (found, msg) = theGuesser.guess(guess)

        if found: # correct guess
            theGuesser=GuessNumberModel() # new number

        d = {'msg':msg, 'newmsg':newmsg, 'cnt':theGuesser.count+1,
             'variant':'globales Serverobjekt', 'hidden':''}
        response.send_template('show.tmpl',d)


class GetGuesserApp(App):

    def register_routes(self):
        self.add_route("", self.getGuess)

    def getGuess(self, request, response, pathmatch):
        """Controller for number guesser using hidden GET form fields."""

        try: # access guessed number from form
            guess = int(request.params['guess'])
        except KeyError:
            guess = -1

        try: # retrieve state variables from form
            num = int(request.params['number'])
            count = int(request.params['count'])
        except KeyError: # can't retrieve: new number to guess
            num = 0
            count = 0

        g = GuessNumberModel(num, count) # make model object
        newmsg = 'Neue Nummer generiert!' if num == 0 else ''

        # evaluate guess
        (found, msg) = g.guess(guess)

        if found: # correct guess: create new number
            g = GuessNumberModel()

        # always generate hidden fields for state values
        hidden = "<input type='hidden' name='number' value=%d>\n" % g.num
        hidden += "<input type='hidden' name='count' value=%d>\n" % g.count

        d = {'msg':msg, 'newmsg':newmsg, 'cnt':g.count+1,
             'variant':'GET-Parameter', 'hidden':hidden}
        response.send_template('show.tmpl',d)


class CookieGuesserApp(App):

    def register_routes(self):
        self.add_route("", self.cookiesGuess)

    def cookiesGuess(self, request, response, pathmatch):
        """Controller for number guesser using cookies."""

        try: # access guessed number from form
            guess = int(request.params['guess'])
        except (KeyError, ValueError):
            guess = -1

        try: # access state values from cookie
            num = int(request.cookies['number'])
            count = int(request.cookies['count'])
        except KeyError: # no cookie
            num = 0
            count = 0

        # make model object (new or from cookie values)
        g = GuessNumberModel(num, count)
        newmsg = 'Neue Nummer generiert!' if num == 0 else ''

        # evaluate guess
        (found, msg) = g.guess(guess)
        if found: # correct guess. Destroy cookies
            cookie_num = Cookie("number", g.num, expires=Cookie.expiry_date(-1))
            cookie_count = Cookie("count", 0, expires = Cookie.expiry_date(-1))
        else: # create new cookies
            cookie_num = Cookie("number", g.num)
            cookie_count = Cookie("count", g.count)

        # send cookies
        response.add_cookie(cookie_num)
        response.add_cookie(cookie_count)
        d = {'msg':msg, 'newmsg':newmsg, 'cnt':g.count+1,
             'variant':'Cookies', 'hidden':''}
        response.send_template('show.tmpl',d)


class SessionGuesserApp(App):

    def register_routes(self):
        self.add_route("", self.sessionGuess)

    def sessionGuess(self,request, response, pathmatch):
        """Controller for number guesser using cookies."""

        try: # access guessed number from form
            guess = int(request.params['guess'])
        except KeyError:
            guess = -1

        try:
            g = request.session['guesser']
        except KeyError:
            request.session.renew()
            g = GuessNumberModel()
            request.session['guesser'] = g
            newmsg = 'Neue Nummer generiert!'
        else:
            newmsg = ''

        (found, msg) = g.guess(guess)
        if found: # destroy session
            # new session and number will be generated next time
            request.session.renew()
            count = 1
        else:
            # pass sessid id to hidden input field
            count = g.count + 1

        d = {'msg':msg, 'newmsg':newmsg, 'cnt':count,
             'variant':'Session per Cookie', 'hidden':''}
        response.send_template('show.tmpl',d)


        
if __name__ == '__main__':
    s = Webserver()
    s.set_templating("jinja2")
    s.set_templating_path("templates.jinja2")
    s.add_app(WelcomeApp())
    s.add_app(GlobalGuessApp(prefix='global/?'))
    s.add_app(CookieGuesserApp(prefix='cookies/?'))
    s.add_app(GetGuesserApp(prefix='get/?'))
    s.add_app(SessionGuesserApp(prefix='session/?'))
    s.add_app(StaticApp(prefix='', path='static'))
    s.add_middleware(SessionMiddleware()) # let's have sessions

    s.serve()

