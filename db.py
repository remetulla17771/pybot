import sqlite3
from xmlrpc.client import boolean

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def get_user(self, iin):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `electorate` WHERE `iin` = ?", (iin,)).fetchone()
        return result

    def user_exists(self, iin):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `electorate` WHERE `iin` = ?", (iin,)).fetchone()
            if result:
                return True
            else:
                return False

    def get_region(self, idRegion):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `area` WHERE `nomer` = ?", (idRegion,)).fetchone()
        return result
    
    def get_city(self, idCity):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `regions` WHERE `id` = ?", (idCity,)).fetchone()
        return result
    