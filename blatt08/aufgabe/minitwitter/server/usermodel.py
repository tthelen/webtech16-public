from server.log import log
import sqlite3 as sqlite
import re

class UserError(Exception):
    """Error handling user data."""

    def __init__(self, msg=''):
        self.msg = msg


class Users:
    """The User collection."""

    def __init__(self, db_connection=None):

        self.username_regex = r"^[\w-]+$"  # only word chars for usernames
        self.passwd_regex = r"^[^\s:]+$"  # no whitespace and : for passwords
        self.roles = ['nobody', 'user', 'admin']

        if not db_connection:
            self.con = sqlite.connect('user.db')
        else:
            self.con = db_connection

        with self.con:
            cur = self.con.cursor()
            cur.executescript("""
              CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT, role TEXT, fullname TEXT);
              INSERT OR IGNORE INTO users VALUES ('admin','admin','admin','Armin Administrator');
              INSERT OR IGNORE INTO users VALUES ('user1','user1','user','Ulf User');
              INSERT OR IGNORE INTO users VALUES ('user2','user2','user','Ute User');
              """)

    def login(self, username, password):
        """Checks credentials and return user object if they are correct."""

        u = self.findByUsername(username)
        if u and u.password == password:
            return u
        else:
            return None

    def createUser(self, username, password, role, fullname):
        """Create a new user in db. Returns 1 if inserted, 0 if not."""

        if self.findByUsername(username):
            raise UserError("Username already exists.")
        if not username:
            raise UserError("Invalid empty username.")
        if not password or not re.match(self.passwd_regex, password):
            raise UserError("Invalid password '%s'. Don't use whitespace and :" % password)
        if not role in self.roles:
            raise UserError("Illegal role.")

        with self.con:
            cur = self.con.cursor()
            cur.executescript("INSERT INTO users VALUES('%s', '%s', '%s', '%s')" % (username, password, role, fullname))
            return cur.rowcount

    def deleteUser(self, username):
        with self.con:
            cur = self.con.cursor()
            cur.executescript("DELETE FROM users WHERE username='%s'" % (username))
            return cur.rowcount

    def findByUsername(self, username):
        with self.con:
            cur = self.con.cursor()
            query = "SELECT * FROM users WHERE username='%s'" % (username)
            cur.execute(query)
            row = cur.fetchone()
            log(2, "findByUsername(%s)=%s" % (username, row if row else "[empty result]"))

        if row:
            return User(row)
        else:
            None  # None if no user found

    def findUsers(self):
        with self.con:
            cur = self.con.cursor()
            query = "SELECT * FROM users"
            cur.execute(query)
            rows = cur.fetchall()
        return [User(row) for row in rows]


class User:
    """An authenticated user."""

    def __init__(self, row):
        """Constructs a user with username and arbitratry additional attributes."""
        self.username = row['username']
        self.is_authenticated = True
        for key in row.keys():  # set all other parameters as object attributes
            setattr(self, key, row[key])
        self.is_admin = (self.role == 'admin')


class AnonymousUser(User):
    """A special unauthenticated user named 'Anonymous' with role 'nobody' ."""

    def __init__(self):
        self.username = 'Anonymous'
        self.fullname = 'Anonymous'
        self.role = 'nobody'
        self.is_authenticated = False
        self.is_admin = False
