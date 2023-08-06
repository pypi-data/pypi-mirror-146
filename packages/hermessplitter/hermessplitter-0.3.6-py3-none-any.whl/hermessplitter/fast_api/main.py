from fastapi import FastAPI, Query
from hermessplitter.db import db_funcs
from hermessplitter.fast_api import functions
import uvicorn

app = FastAPI()


@app.get('/get_hermes_records')
def get_hermes_records():
    return db_funcs.get_records()


@app.get('/get_hermes_record')
def get_hermes_record(record_id: int = Query(...,
                                             description='ID записи из wdb')):
    return db_funcs.get_record(record_id=record_id)

def run_uvicorn():
    uvicorn.run("hermessplitter.fast_api.main:app", host="0.0.0.0", port=8001)


if __name__ == '__main__':
    run_uvicorn()