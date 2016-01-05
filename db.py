import sqlite3 as sql

class Things:
    """ A class to keep all the database related things """

    def __init__(self):
        # Connects to the database of things.
        # Will create it if it does not exists.
        self.db = sql.connect('things.db')

        # Checks if the "Things" table is already present in the database.
        # If not, create it
        if (u'Things',) not in self.getTables() :
            print "[+] Creating the Things table"
            self.createThingsTable()

    # Get a list of tables in the db
    def getTables(self):
        with self.db:
            cur = self.db.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return cur.fetchall()

    # Creates a table to store Things
    def createThingsTable(self):
        with self.db:
            cur = self.db.cursor()
            cur.execute("CREATE TABLE Things(Id INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT, Author TEXT, ThingId INT, License TEXT, Time TEXT , SearchWord Text, Folder TEXT)")

    # Insert new Thing in the DB, with data as a Tuple like this:
    # (Title, Author, ThingId, License, Time, SearchWord, Folder)
    def insertThing(self, data):
        with self.db:
            cur = self.db.cursor()
            cur.execute("INSERT INTO Things(Title, Author, ThingId, License, Time, SearchWord, Folder) VALUES(?, ?, ?, ?, ?, ?, ?);", data)
