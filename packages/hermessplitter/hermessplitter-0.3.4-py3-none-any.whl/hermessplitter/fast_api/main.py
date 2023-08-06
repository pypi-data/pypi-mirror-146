from fastapi import FastAPI, Query
from hermessplitter.db import db_funcs
from hermessplitter.fast_api import functions

app = FastAPI()


class HermesAPI:
    def __init__(self, hermes_core):
        self.wdb_sqlshell = hermes_core.wdb_sqlshell

    @app.get('/get_hermes_records')
    def get_hermes_records(self):
        return db_funcs.get_records()

    @app.get('/get_hermes_record')
    def get_hermes_record(self, record_id: int = Query(...,
                                                       description='ID записи из wdb')):
        return db_funcs.get_record(record_id=record_id)

    def get_wdb_records(self):
        return functions.get_wdb_records(self.wdb_sqlshell)