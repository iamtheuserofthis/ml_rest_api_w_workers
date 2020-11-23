from sqlalchemy import exc, Table, Column, MetaData, String, BigInteger, JSON, TIMESTAMP, Boolean

"""
Configurations for the database connection
"""
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
