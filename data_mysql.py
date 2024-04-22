import mysql.connector
import os
from dotenv import load_dotenv

class Database:
    # initiation
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    # connect to database
    def connect(self):
        try:
            self.db = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database,
                port = self.port
            )
            # print(self.db)
        except mysql.connector.Error as e:
            print(f"Gagal terhubung ke database: {e}")

    # select all
    def select_all(self, table_name):
        try:
            cursor = self.db.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            results = cursor.fetchall()
            # print(results[0])
            # for row in results:
            #     print(row)
            return results

        except mysql.connector.Error as e:
            print(f"Gagal melakukan select all: {e}")

    # select where nip
    def select_nip(self, table_name, nip):
        try:
            cursor = self.db.cursor()
            cursor.execute(f"SELECT * FROM {table_name} WHERE nip = {nip}")
            results = cursor.fetchone()
            if results:
                # print(results)
                return results
            else:
                print("tidak ada data dengan nip tersebut")
                
        except mysql.connector.Error as e:
            print(f"Gagal melakukan select nip: {e}")

    # update no hp where nip
    def update_nohp(self, table_name, nip, nohp):
        try:
            cursor = self.db.cursor()
            query = f"UPDATE {table_name} SET no_hp = {nohp} WHERE nip = {nip}"
            cursor.execute(query)
            self.db.commit()

            if cursor.rowcount == 1:
                return "updated"
            else:
                return "tidak terupdate"

        except mysql.connector.Error as e:
            print(f"Gagal melakukan update nomer hp: {e}")

    # insert log data
    def insert_log_hp_updated(self, table_name, nip, nohp):
        try:
            cursor = self.db.cursor()
            ket = "update no hp"
            query = f"INSERT INTO {table_name} (nip, no_hp, status) VALUES (%s, %s, %s)"
            values = (nip, nohp, ket)
            cursor.execute(query, values)
            self.db.commit()

            if cursor.rowcount == 1:
                return "inserted"
            else:
                return "tidak ter-insert"
            
        except mysql.connector.Error as e:
            print(f"Gagal melakukan insert data log: {e}")


# load_dotenv()
# host = os.environ["db_host"]
# username = os.environ["db_user"]
# password = os.environ["db_password"]
# database_name = os.environ["db_database"]
# port = os.environ["db_port"]

# db = Database(host, username, password, database_name, port)
# db.connect()