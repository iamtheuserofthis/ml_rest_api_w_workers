import pika
import sys
import os
import json

from model_classes import face_detect
from dao.db_con_v2 import DBOperations


class FaceDetectWorker:

    def __init__(self, receive_queue_name, file_dir, host='localhost'):

        connection = pika.BlockingConnection(
            pika.URLParameters("amqp://test:test@iamtheuserofthis3.pune.cdac.in:5672")
        )
        self.consuming_chan = connection.channel()
        self.file_dir = file_dir
        self.receive_queue_name = receive_queue_name
        self.consuming_chan.queue_declare(queue=self.receive_queue_name, durable=True)
        self.model = face_detect.FaceDetectModel()

    def call_back_cov(self):

        def cb_face_detect(ch, method, properties, body):
            try:
                db_op = DBOperations()
                body_ob = json.loads(body.decode('utf-8'))
                applicant_cred_id = body_ob[0]
                f_name = body_ob[1]
                # ch.basic_ack(delivery_tag=method.delivery_tag)
                try:
                    res = self.model.face_detect(os.path.join(self.file_dir, f_name))
                    print('image %s processed successfully res %s' % (f_name, res))
                    db_op.process_complete(applicant_cred_id, f_name, 'face_detect', 'face_detect', res)
                except Exception as e:
                    db_op.process_complete(applicant_cred_id, f_name, 'face_detect', 'face_detect', None, False)
                    print('task failed for applicant_cred_id=%s, file_name=%s' % (applicant_cred_id, f_name))

            except Exception as e:
                print(e.message)
            finally:
                ch.basic_ack(delivery_tag=method.delivery_tag)

        return cb_face_detect

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


fdw = FaceDetectWorker('face_detect_queue', '/image_uploads')
fdw.start_worker()
