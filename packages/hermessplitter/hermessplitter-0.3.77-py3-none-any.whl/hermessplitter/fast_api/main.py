from fastapi import FastAPI, Query
from hermessplitter.db import db_funcs
import uvicorn

app = FastAPI()
import contextlib
import time
import threading
import uvicorn


class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


@app.get('/get_hermes_records')
def get_hermes_records():
    return db_funcs.get_records()


@app.get('/get_hermes_record')
def get_hermes_record(record_id: int = Query(...,
                                             description='ID записи из wdb')):
    return db_funcs.get_record(record_id=record_id)


def run_uvicorn():
    config = uvicorn.Config("hermessplitter.fast_api.main:app", host="0.0.0.0",
                            port=8003,
                            log_level="info", loop="asyncio")
    server = Server(config=config)
    server.run()
    with server.run_in_thread():
        while True:
            ...


if __name__ == '__main__':
    run_uvicorn()
