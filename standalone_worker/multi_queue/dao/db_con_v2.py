from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy import inspect
from sqlalchemy import exc, Table, Column, MetaData, String, BigInteger, JSON, TIMESTAMP, Boolean
import json
from datetime import datetime

# todo - Place the configuration object in the dbconfig type file
config_obj = {}
config_obj['drivername'] = 'postgres'
config_obj['host'] = 'iamtheuserofthis3.pune.cdac.in'
config_obj['username'] = 'scala_user'
config_obj['passwd'] = 'scala_user'
config_obj['port'] = 5432
config_obj['database'] = 'icg_image_process_sample'

table_model = lambda meta: Table('image_processing_result_v2', meta,
                                 Column('applicant_cred_id', BigInteger),
                                 Column('image_id', String),
                                 Column('task', String),
                                 Column('final_task', String),
                                 Column('result', JSON),
                                 Column('timestamp', TIMESTAMP),
                                 Column('success', Boolean)
                                 )


class DBOperations:
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

    def update_upload(self, applicant_cred_id, final_task, image_id, success=True):
        ins = self.table.insert().values(
            applicant_cred_id=applicant_cred_id,
            image_id=image_id,
            task='image_upload',
            final_task=final_task,
            timestamp=datetime.now(),
            success=success
        )
        conn = self.engine.connect()
        conn.execute(ins)

    def process_complete(self, applicant_cred_id, image_id, task, final_task, result_dict, success=True):
        ins_s = self.table.insert().values(
            applicant_cred_id=applicant_cred_id,
            image_id=image_id,
            task=task,
            final_task=final_task,
            result=json.dumps(result_dict),
            timestamp=datetime.now(),
            success=success
        )

        ins_f = self.table.insert().values(
            applicant_cred_id=applicant_cred_id,
            image_id=image_id,
            task=task,
            final_task=final_task,
            timestamp=datetime.now(),
            success=success
        )
        conn = self.engine.connect()

        conn.execute(ins_s) if success else conn.execute(ins_f)


if __name__=='__main__':
    dbo = DBOperations()
    dbo.init_record(10100, 'thelongandambiguousstringdata', 'face_detect')