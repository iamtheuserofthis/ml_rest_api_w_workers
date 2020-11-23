from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy import inspect
from sqlalchemy import exc, Table, Column, MetaData, String, BigInteger, JSON, TIMESTAMP, Boolean
import json
from datetime import datetime
from resources.dao.db_config import config_obj, table_model
# todo - Place the configuration object in the dbconfig type file



class DBInsertOperations:
    def __init__(self):
        postgres_db = {
            'drivername': config_obj['drivername'],
            'username': config_obj['username'],
            'password': config_obj['passwd'],
            'host': config_obj['host'],
            'port': config_obj['port'],
            'database': config_obj['database']
        }
        self.engine = create_engine(URL(**postgres_db))
        inspector = inspect(self.engine)
        if not 'image_processing_result_v2' in inspector.get_table_names():
            raise exc.NoReferencedTableError("Table could not be found", 'image_processing_result')
        meta = MetaData(self.engine)
        self.table = table_model(meta)

    def init_record(self, applicant_cred_id, image_id, final_task, success=True):
        ins = self.table.insert().values(
            applicant_cred_id=applicant_cred_id,
            image_id=image_id,
            final_task=final_task,
            task='image_submit',
            timestamp=datetime.now(),
            success=success
        )
        conn = self.engine.connect()
        conn.execute(ins)



