import pika
import sys
import os
import json
# home_path = '/home/iamtheuserofthis/Python_Workspace/image_processing_main/iaf_image_process/components/'
# work_path = '/home/iamtheuserofthis/python_workspace/iaf_image_process/components'

# sys.path.append(work_path)
import tensorflow as tf
from tensorflow.python.keras.backend import set_session
import keras
import file_utils.file_tranlator as ft
from model_classes import gender_detect
from dao import db_con_v2


class GenderDetectWorker:

    def __init__(self, receive_queue_name, file_dir, host='localhost'):

        connection = pika.BlockingConnection(
            pika.URLParameters("amqp://test:test@iamtheuserofthis3.pune.cdac.in:5672")
        )
        self.consuming_chan = connection.channel()
        self.file_dir = file_dir

        self.receive_queue_name = receive_queue_name
        self.consuming_chan.queue_declare(queue=self.receive_queue_name, durable=True)
        self.model = gender_detect.GenderDetect(file_dir)

    def call_back_cov(self):

        def cb_gender_detect(ch, method, properties, body):
            try:
                db_op2 = db_con_v2.DBOperations()
                body_ob = json.loads(body.decode('utf-8'))
                applicant_cred_id = body_ob[0]
                f_name = body_ob[1]
                # ch.basic_ack(delivery_tag=method.delivery_tag)

                try:
                    res = self.model.gender_detect_one(os.path.join(self.file_dir, f_name))
                    print('image %s processed successfully res %s' % (f_name, res))
                    db_op2.process_complete(applicant_cred_id, f_name, 'gender_detect', 'gender_detect', res)
                except Exception as e:
                    print('problem with the model :' + e.message)
                    db_op2.process_complete(applicant_cred_id, f_name, 'gender_detect', 'gender_detect', None,
                                            success=False)

            except Exception as e:
                print(e.message)

            finally:
                ch.basic_ack(delivery_tag=method.delivery_tag)

        return cb_gender_detect

    def start_worker(self):
        self.consuming_chan.basic_qos(prefetch_count=1)
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


fdw = GenderDetectWorker('gender_detect_queue', '/image_uploads')
fdw.start_worker()
