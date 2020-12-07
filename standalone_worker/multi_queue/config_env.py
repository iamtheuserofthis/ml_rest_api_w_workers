import os

print(os.environ)
rabbitmq_username = os.environ['RABBITMQ_USER']
rabbitmq_passwd = os.environ['RABBITMQ_PASSWD']
rabbitmq_host = os.environ['RABBITMQ_HOST']
rabbitmq_port = os.environ['RABBITMQ_PORT']

postgres_username = os.environ["POSTGRES_USER"]
postgres_password = os.environ["POSTGRES_PASSWORD"]
postgres_hostname = os.environ["POSTGRES_HOSTNAME"]
postgres_port = os.environ["POSTGRES_PORT"]
