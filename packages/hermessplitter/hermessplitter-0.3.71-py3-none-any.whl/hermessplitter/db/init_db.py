import sqlalchemy.exc
from sqlalchemy import create_engine
from hermessplitter.db import tables
import os

dbpath = os.environ.get('HDBPATH')
dbpath = f"sqlite:///{dbpath}"
#dbpath = 'sqlite:///C:\\Users\\faizi\\PycharmProjects\\Splitters\\hermesspillter\\hermessplitter\\hdb.db'
if not os.path.exists(dbpath):
    engine = create_engine(dbpath)
    engine.connect()
    tables.metadata.create_all(engine)

try:
    ins = tables.settings.insert().values(
        key='active',
        value=True
    )
    engine.execute(ins)
except sqlalchemy.exc.IntegrityError:
    pass

try:
    ins = tables.settings.insert().values(
        key='test_mode',
        value=True
    )
    engine.execute(ins)
except sqlalchemy.exc.IntegrityError:
    pass

