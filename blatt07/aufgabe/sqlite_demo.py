import sqlite3

sql = """
CREATE TABLE IF NOT EXISTS person (
  id integer PRIMARY KEY,
  firstname text NOT NULL,
  lastname text NOT NULL,
  email text NOT NULL
);"""

conn = sqlite3.connect('sqlite_demo.db')
curs = conn.cursor()
curs.execute(sql)
conn.commit()

sql = "INSERT INTO person (firstname, lastname, email) VALUES ('Tobias', 'Thelen', 'tthelen@uos.de')"
conn.execute(sql)
conn.commit()

fn="Tobias"
for row in conn.execute("SELECT * FROM person WHERE firstname=?;", [fn]):
    print(row)
