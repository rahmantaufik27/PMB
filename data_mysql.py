import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        try:
            self.db = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database,
                port = "3306"
            )
            # print(self.db)
        except mysql.connector.Error as e:
            print(f"Gagal terhubung ke database: {e}")

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

    def select_nip(self, table_name, nip):
        try:
            cursor = self.db.cursor()
            cursor.execute(f"SELECT * FROM {table_name} WHERE NIP = {nip}")
            results = cursor.fetchone()
            if results:
                # print(results)
                return results
            else:
                print("tidak ada data dengan nip tersebut")
                
        except mysql.connector.Error as e:
            print(f"Gagal melakukan select nip: {e}")

    def update_nohp(self, table_name, nip, nohp):
        try:
            cursor = self.db.cursor()
            query = f"UPDATE {table_name} SET `No HP` = {nohp} WHERE nip = {nip}"
            cursor.execute(query)
            self.db.commit()

            if cursor.rowcount == 1:
                return "updated"
            else:
                return "tidak terupdate"

        except mysql.connector.Error as e:
            print(f"Gagal melakukan update nomer hp: {e}")

# load_dotenv()
# host = os.environ["db_host"]
# username = os.environ["db_user"]
# password = os.environ["db_password"]
# database_name = os.environ["db_database"]

# db = Database(host, username, password, database_name)
# db.connect()