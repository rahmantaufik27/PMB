from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import pandas as pd
import json
from typing import Union
import os
from dotenv import load_dotenv
import data_mysql
from starlette.responses import RedirectResponse

app = FastAPI()

# get values from .env file
load_dotenv()
host = os.environ["db_host"]
username = os.environ["db_user"]
password = os.environ["db_password"]
database_name = os.environ["db_database"]
port = os.environ["db_port"]

# connect database with parameters
db = data_mysql.Database(host, username, password, database_name, port)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# show all pengawas
@app.get("/pengawas")
async def load_all_pengawas():
    db.connect()
    res = db.select_all("pengawas")
    return res

# show specific pengawas based on nip
# if the pengawas doesnt have no hp then must be updated
@app.get("/pengawas_nip/{nip}")
async def load_nip_pengawas(nip: str):
    db.connect()
    res = db.select_nip("pengawas", str(nip))
    if not res:
        raise HTTPException(status_code=404, detail="User not found")
    else:
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
        if hp == "":
            return HTMLResponse(content=res_html, status_code=200)
        else:
            return res

# process to update hp pengawas
@app.get("/pengawas_update_hp_proses")
async def update_hp_pengawas_proses(nip: str, hp_new: str):
    return RedirectResponse(f"/pengawas_update_hp/{nip}?hp={hp_new}")

# update to table pengawas and insert the data to log pengawas
@app.get("/pengawas_update_hp/{nip}")
async def update_hp_pengawas(nip: str, hp: Union[str, None] = None):
    try:
        db.connect()
        db.update_nohp("pengawas", str(nip), str(hp))
        db.insert_log_hp_updated("log_pengawas", str(nip), str(hp))
        # return res
        return await load_nip_pengawas(str(nip))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    

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


# if __name__ == '__main__':
#     uvicorn.run(app, port=8000, host='localhost')