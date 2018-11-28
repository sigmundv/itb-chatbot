import sqlite3


# these functions are storing un/satifactory answers in the embedded SQLite database
# they should be self-explanatory


def store_satisfactory_result(db, query, answer):
    DatabaseManager(db).insert("INSERT INTO queries VALUES (?,?,?)", (query, answer, 1))


def store_unsatisfactory_result(db, query, answer):
    DatabaseManager(db).insert("INSERT INTO queries VALUES (?,?,?)", (query, answer, 0))


def get_previous_results(db, query, satisfied):
    return DatabaseManager(db).query("SELECT answer FROM queries WHERE query=? and satisfied=?", (query, satisfied))


# a class to handle the database transactions

class DatabaseManager:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def create(self, sql):
        self.cur.execute(sql)
        self.conn.commit()

    def query(self, sql, params):
        self.cur.execute(sql, params)
        self.conn.commit()
        return self.cur.fetchall()

    def insert(self, sql, params):
        try:
            self.cur.execute(sql, params)
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass

    def __del__(self):
        self.conn.close()
