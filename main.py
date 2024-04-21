from fastapi import FastAPI
import pandas as pd
import json
from typing import Union
import os
from dotenv import load_dotenv
import data_mysql

app = FastAPI()

load_dotenv()
host = os.environ["db_host"]
username = os.environ["db_user"]
password = os.environ["db_password"]
database_name = os.environ["db_database"]

db = data_mysql.Database(host, username, password, database_name)

@app.get("/pengawas")
async def load_all_pengawas():
    db.connect()
    res = db.select_all("pengawas")
    return res

@app.get("/pengawas_nip/{nip}")
async def load_nip_pengawas(nip: int):
    db.connect()
    res = db.select_nip("pengawas", str(nip))
    return res
    
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