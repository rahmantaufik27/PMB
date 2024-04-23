from flask import Flask, request, redirect, url_for
import os
from dotenv import load_dotenv
import mysql.connector
from starlette.responses import RedirectResponse

app = Flask(__name__)

# create database class to connect, update, insert, etc.
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
            print(self.db)
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

# connect database with parameters
db = Database("103.3.46.185", "simanila", "simanila@2024", "pmb", "3306")

# homepage (display welcome and form input nip)
@app.route('/')
async def index():
    return """
        <html>
            <style>body { display: flex; align-items: center; justify-content: center; height: 100vh; }</style>
            <body>
                <form action="/pengawas_nip" method="POST">
                    <h3>Silahkan Masukan NIP untuk mengetahui penampatan lokasi pengawas </h3>
                    NIP : <input type="text" name="nip" id="nip" required><br>
                    <input type="submit" value="Submit" />
                </form>
            </body>
        </html>
    """

# show specific pengawas based on nip
# if the pengawas doesnt have no hp then must be updated
@app.route("/pengawas_nip", methods=['POST'])
async def load_nip_pengawas():
    db.connect()
    nip = request.form["nip"]
    res = db.select_nip("pengawas", str(nip))
    css = "body { display: flex; align-items: center; justify-content: center; height: 100vh; }"
    # hp = res[-1]
    hp = int(0 if res[-1] is None else res[-1])
    if hp != 0:
        return f"""
            <html>
                <style>{css}</style>
                <body>
                        NIP : {res[5]} <br/>
                        Nama : {res[3]} <br/>
                        No Hp : {res[-1]} <br/>
                        Jadwal : {res[4]} <br/>
                        Nama Lokasi : {res[1]} <br/>
                        Nama Ruangan : {res[2]} <br/>
                </body>
            </html>
        """
    else:
        return f"""
            <html>
                <style>{css}</style>
                <body>
                    <form action="/pengawas_update_hp" method="POST">
                        NIP : <input type="text" name="nip" id="nip" value={res[5]} readonly><br>
                        Nama : <label>{res[3]}</label><br/>
                        Nomer HP : <input type="text" name="hp_new" id="hp_new"><br>
                        <input type="submit" value="Submit" />
                    </form>
                </body>
            </html>
        """
        
    
# show form for updating the hp
@app.route("/pengawas_update_hp", methods=['POST'])
async def load_pengawas_update_hp():
    db.connect()
    nip = request.form["nip"]
    hp = request.form["hp_new"]
    db.update_nohp("pengawas", str(nip), str(hp))
    db.insert_log_hp_updated("log_pengawas", str(nip), str(hp))
    return redirect(url_for('index'))
    
@app.route('/pengawas_all')
def load_all_pengawas():
    db.connect()
    res = db.select_all("pengawas")
    return res

if __name__ == "__main__":
    app.run()
