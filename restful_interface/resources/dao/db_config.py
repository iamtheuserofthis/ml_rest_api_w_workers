from sqlalchemy import exc, Table, Column, MetaData, String, BigInteger, JSON, TIMESTAMP, Boolean
import resources.config_env as env_conf
"""
Configurations for the database connection
"""
config_obj = {}
config_obj['drivername'] = 'postgres'
config_obj['host'] = env_conf.postgres_hostname
config_obj['username'] = env_conf.postgres_username
config_obj['passwd'] = env_conf.postgres_password
config_obj['port'] = env_conf.postgres_port
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
