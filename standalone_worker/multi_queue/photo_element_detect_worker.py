import pika
import sys
import os
import json

from dao.db_con_v2 import DBOperations
from model_classes.photo_element_mrcnn import ElementDetectionMrcnn
import config_env as env_vars

class PhotoElementDetectWorker():
    def __init__(self, receive_queue_name, file_dir, log_dir, model_dir, host='localhost'):
        url = "amqp://%s:%s@%s:%s" % (
        env_vars.rabbitmq_username, env_vars.rabbitmq_passwd, env_vars.rabbitmq_host, env_vars.rabbitmq_port)
        print('connection link: %s' % url)
        connection = pika.BlockingConnection(
            pika.URLParameters(url)
        )
        self.consuming_chan = connection.channel()
        self.file_dir = file_dir
        self.receive_queue_name = receive_queue_name
        self.consuming_chan.queue_declare(queue=self.receive_queue_name, durable=True)
        self.model = ElementDetectionMrcnn(log_dir, model_dir)

    def call_back_cov(self):
        def cb_element_detect(ch, method, properties, body):
            try:
                db_op = DBOperations()
                body_ob = json.loads(body.decode('utf-8'))
                applicant_cred_id = body_ob[0]
                f_name = body_ob[1]

                try:
                    file_loc = os.path.join(self.file_dir, f_name)
                    print('body_ob', body_ob)
                    print('file_log', file_loc)
                    res = self.model.detect_image(file_loc)
                    print(res)
                    db_op.process_complete(applicant_cred_id, f_name, 'photo_element_detect', 'photo_element_detect',res)

                except Exception as e:
                    db_op.process_complete(applicant_cred_id,
                                           f_name,
                                           'photo_element_detect',
                                           'photo_element_detect',
                                           None,
                                           success=False)

            except Exception as E:
                print('Could not process the message @ %s' % PhotoElementDetectWorker.__name__)

            finally:
                ch.basic_ack(delivery_tag=method.delivery_tag)

        return cb_element_detect

    def start_worker(self):
        self.consuming_chan.basic_qos(prefetch_count=3)
        self.consuming_chan.basic_consume(
            queue=self.receive_queue_name,
            on_message_callback=self.call_back_cov(),
            auto_ack=False
        )
        try:
            self.consuming_chan.start_consuming()

        except KeyboardInterrupt:
            self.consuming_chan.stop_consuming()
            self.consuming_chan.close()
            print('Closing the consumer connection.....')


phote_elem_detect = PhotoElementDetectWorker(
    'photo_element_detect_queue',
    '/image_uploads',
    '/log_files',
    '/models/weights_for_fin_v3.h5')

phote_elem_detect.start_worker()
