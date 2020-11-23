from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy import inspect
from sqlalchemy import exc, Table, Column, MetaData, String, BigInteger, JSON, TIMESTAMP, Boolean, select
import json
from datetime import datetime
from resources.dao.db_config import config_obj, table_model


class DBSelectOperations:

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

    @staticmethod
    def list_to_dict(list_values):
        """
        :param list_values: result_tuple/list
        :type list_values: list/tuple
        :return: Key/Value pair of info passed
        :rtype: Dict
        """
        fin_dict = {
            'applicant_cred_id': list_values[0],
            'image_id': list_values[1],
            'task': list_values[2],
            'final_task': list_values[3],
            'result': list_values[4],
            'tstamp': list_values[5],
            'success': list_values[6]

        }
        return fin_dict

    def get_from_db(self, **kwargs):
        """
        :param kwargs: applicant_cred_id, image_id, final_task
        :type kwargs:  long/int, str, str
        :return: Records of the applicant_cred_id or/and image_id or/and final_task
        :rtype: List[Dict]
        """
        valid_kwargs_keys = ['image_id', 'applicant_cred_id', 'task_name']
        conn = self.engine.connect()
        sel_by_app_cred = select([
            self.table.c.applicant_cred_id,
            self.table.c.image_id,
            self.table.c.task,
            self.table.c.final_task,
            self.table.c.result,
            self.table.c.timestamp,
            self.table.c.success])

        for k, v in kwargs.items():
            if not k in valid_kwargs_keys:
                raise KeyError('%s is unknown use:%s' % (k, str(valid_kwargs_keys)))
            if k == 'applicant_cred_id':
                sel_by_app_cred = sel_by_app_cred.where(self.table.c.applicant_cred_id == v)

            if k == 'image_id':
                sel_by_app_cred = sel_by_app_cred.where(self.table.c.image_id == v)

            if k == 'task_name':
                sel_by_app_cred = sel_by_app_cred.where(self.table.c.final_task == v)

        return list(map(self.list_to_dict, conn.execute(sel_by_app_cred)))

    def get_image_res(self, applicant_cred_id, image_id, final_task):
        query_res = {}
        res = self.get_from_db(applicant_cred_id=applicant_cred_id, image_id=image_id, task_name=final_task)
        # print(res)
        sorted_res = sorted(res, key=lambda x: x['tstamp'], reverse=True)
        latest_event = sorted_res[0]
        if latest_event['task'] == latest_event['final_task']:
            query_res = {'status': 'successful' if latest_event['success'] else 'failed',
                         'result': latest_event['result'],
                         'total_time': str(sorted_res[0]['tstamp']-sorted_res[-1]['tstamp'])}
        else:
            query_res = {'status': 'pending' if latest_event['success'] else 'failed',
                         'last_task': latest_event['task'],
                         'total_time': str(sorted_res[0]['tstamp']-sorted_res[-1]['tstamp'])}

        return query_res

    def status_per_image_app_cred(self, applicant_cred_id, image_id):
        pass

    def status_cred_id(self, applicant_cred_id):
        """
        Status and the images uploaded by individual user
        :param applicant_cred_id:
        :type applicant_cred_id:
        :return:
        :rtype:
        """
        pass


if __name__ == '__main__':
    dbOp = DBSelectOperations()
    print(dbOp.get_image_res(applicant_cred_id=12102, image_id='656c3258-7309-4e35-b460-5400e08f9882',
                             final_task='photo_element_detect'))
    # for i in
