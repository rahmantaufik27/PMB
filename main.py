from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import pandas as pd
import json
from typing import Union
import os
from dotenv import load_dotenv
import data_mysql
from starlette.responses import RedirectResponse

app = FastAPI()

load_dotenv()
host = os.environ["db_host"]
username = os.environ["db_user"]
password = os.environ["db_password"]
database_name = os.environ["db_database"]

db = data_mysql.Database(host, username, password, database_name)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/pengawas")
async def load_all_pengawas():
    db.connect()
    res = db.select_all("pengawas")
    return res

@app.get("/pengawas_nip/{nip}")
async def load_nip_pengawas(nip: int):
    db.connect()
    res = db.select_nip("pengawas", str(nip))
    hp = res[-1]
    nama = res[3]
    # print(res[-1])
    res_html = f"""
            <html>
                <body>
                    <form action="/pengawas_update_hp_proses" method="GET">
                        NIP : <input type="text" name="nip" id="nip" value={nip} readonly><br>
                        Nama : <label>{nama}</label><br/>
                        Nomer HP : <input type="text" name="hp_new" id="hp_new"><br>
                        <input type="submit" value="Submit" />
                    </form>
                </body>
            </html>
        """
    if res[-1] == "":
        return HTMLResponse(content=res_html, status_code=200)
    else:
        return res

@app.get("/pengawas_update_hp_proses")
async def update_hp_pengawas_proses(nip: str, hp_new: str):
    return RedirectResponse(f"/pengawas_update_hp/{nip}?hp={hp_new}")

@app.get("/pengawas_update_hp/{nip}")
async def update_hp_pengawas(nip: int, hp: Union[str, None] = None):
    db.connect()
    res = db.update_nohp("pengawas", str(nip), str(hp))
    # return res
    return await load_nip_pengawas(str(nip))
    
# df = pd.read_csv("data/output-3.csv")

# @app.get("/pengawas")
# async def load_questions():
#     res = df.to_json(orient="records")
#     parsed = json.loads(res)
#     return parsed

# @app.get("/pengawas_nip/{nip}")
# async def read_item(nip: int):
#     res = df.loc[df.loc[:,'NIP']==nip]
#     res = res.to_json(orient="records")
#     parsed = json.loads(res)
#     return parsed


# if __name__ == "__main__":
#     main()

# pikirin gimana cara akses data nya lewat dataframe/csv/gsheet/mysql
# pikirin gimana caranya select value only based on nip
## pikirin gimana caranya write nomer telepon where nip in json+api (belum)