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
            query = f"UPDATE {table_name} SET no_hp = '{nohp}' WHERE nip = {nip}"
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
    content_html = """
        <!doctype html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>PMB</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
            </head>
            <body>
                <div class="container mt-5">
                    <div class="row justify-content-center">
                        <div class="col-xl-6 col-lg-6 col-md-6">
                            <div class="card shadow-lg">
                                <div class="card-header py-3">
                                    <h6 class="m-0 font-weight-bold text-dark text-center">Penempatan Lokasi Pengawasi</h6>
                                </div>
                                <form action="/pengawas_nip" method="POST">
                                    <div class="card-body pt-4 pb-4 text-center">
                                        <div class="mb-3">
                                            <p class="card-text mb-0">Silahkan Masukan NIP untuk mengetahui penampatan lokasi pengawas</p><br>
                                            <div class="form-floating mb-3">
                                                <input type="text" class="form-control" placeholder="Nomor Identitas Pegawai" name="nip" id="nip" required>
                                                <label for="floatingInput">Nomor Identitas Pegawai</label>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="card-footer d-flex justify-content-end">
                                        <button type="submit" class="btn btn-dark">Submit</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
            </body>
            </html>

    """
    return content_html

# show specific pengawas based on nip
# if the pengawas doesnt have no hp then must be updated
@app.route("/pengawas_nip", methods=['POST'])
async def load_nip_pengawas():
    db.connect()
    nip = request.form["nip"]
    res = db.select_nip("pengawas", str(nip))

    content_html_data = f"""
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>PMB</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        </head>
        <body>
            <div class="container mt-5">
                <div class="row justify-content-center">
                    <div class="col-xl-6 col-lg-6 col-md-6">
                        <div class="card shadow-lg">
                            <div class="card-header py-3">
                                <h6 class="m-0 font-weight-bold text-dark text-center">Penempatan Lokasi Pengawas</h6>
                            </div>
                            <div class="card-body">
                                <div class="mb-3">
                                    <table class="table table-borderless">
                                        <tbody>
                                            <tr>
                                                <td>NIP</td>
                                                <td>:</td>
                                                <td>{res[5]}</td>
                                            </tr>
                                            <tr>
                                                <td>Nama</td>
                                                <td>:</td>
                                                <td>{res[3]}</td>
                                            </tr>
                                            <tr>
                                                <td>No. Hp</td>
                                                <td>:</td>
                                                <td>{res[-1]}</td>
                                            </tr>
                                            <tr>
                                                <td>Jadwal</td>
                                                <td>:</td>
                                                <td>{res[4]}</td>
                                            </tr>
                                            <tr>
                                                <td>Nama Lokasi</td>
                                                <td>:</td>
                                                <td>{res[1]}</td>
                                            </tr>
                                            <tr>
                                                <td>Nama Ruangan</td>
                                                <td>:</td>
                                                <td>{res[2]}</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
        </body>
        </html>
    """
    input_hp = """
        <div class="form-floating mb-3">
            <input type="text" inputmode="numeric" pattern="[0-9]{1,20}" class="form-control" placeholder="Nomer HP" name="hp_new" id="hp_new" required>
            <label for="floatingInput">Nomer HP</label>
        </div>
    """
    content_html_update = f"""
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>PMB</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        </head>
        <body>
            <div class="container mt-5">
                <div class="row d-flex align-item-center justify-content-center" style="height:100%;">
                    <div class="col-xl-6 col-lg-6 col-md-6">
                        <div class="card shadow-lg">
                            <div class="card-header py-3">
                                <h6 class="m-0 font-weight-bold text-dark text-center">Sistem Penerimaan Mahasiswa Baru</h6>
                            </div>
                            <form action="/pengawas_update_hp" method="POST">
                                <div class="card-body">
                                    <div class="mb-3">
                                        <p class="card-text mb-0 text-center">Silahkan Masukan Nomor HP untuk melengkapi data pengawas</p><br>
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="{res[5]}" name="nip" id="nip" readonly>
                                            <label for="floatingInput">Nomor Identitas Pegawai</label>
                                        </div>
                                        <div class="form-floating mb-3">
                                            <input type="text" class="form-control" id="floatingInput" value="{res[3]}"readonly>
                                            <label for="floatingInput">Nama</label>
                                        </div>
                                        {input_hp}
                                    </div>
                                </div>
                                <div class="card-footer d-flex justify-content-end">
                                    <button type="submit" class="btn btn-dark">Submit</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
        </body>
        </html>
    """
    
    hp = int(0 if res[-1] is None or res[-1] == "" else res[-1])
    if hp != 0:
        return content_html_data
    else:
        return content_html_update
        
    
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
