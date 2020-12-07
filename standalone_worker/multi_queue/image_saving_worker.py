import pika
import sys
import os
import time
import json

print(sys.path)
# home_path = '/home/iamauser/python_workspace/iaf_image_process/components/'
# work_path = '/home/iamtheuserofthis/python_workspace/iaf_image_process/components'
#
# sys.path.append(work_path)

import file_utils.file_tranlator as ft

from dao import db_con_v2
import config_env as env_vars


class ImageSaveWorker:
    def __init__(self, receive_queue_name, file_dir, host='localhost'):
        url = "amqp://%s:%s@%s:%s" % (
        env_vars.rabbitmq_username, env_vars.rabbitmq_passwd, env_vars.rabbitmq_host, env_vars.rabbitmq_port)
        print('connection link: %s' % url)
        connection = pika.BlockingConnection(
            pika.URLParameters(url)
        )
        self.consuming_chan = connection.channel()
        self.consuming_chan.queue_declare(queue=receive_queue_name, durable=True)
        self.next_task_chan = connection.channel()
        # self.next_task_chan.exchange_declare(exchange='EVENTS', exchange_type='direct')
        self.next_task_chan.queue_declare(queue='face_detect_queue', durable=True)
        self.next_task_chan.queue_declare(queue='gender_detect_queue', durable=True)
        self.next_task_chan.queue_declare(queue='photo_element_detect_queue', durable=True)
        self.file_dir = file_dir
        self.receive_queue_name = receive_queue_name
        # self.send_publish_routing_key = send_publish_routing_key

    def call_back_cov(self):
        def cb_file_store(ch, method, properties, body):
            print('current path', os.getcwd())

            db_op2 = db_con_v2.DBOperations()
            try:
                dec_body = ft.decode_img_tag_json(body)
                applicant_cred_id = dec_body[0]
                fin_task = dec_body[1]
                f_name = dec_body[2]
                print(applicant_cred_id, fin_task, f_name)

                try:
                    with open(os.path.join(self.file_dir, str(f_name)), 'wb') as f:
                        f.write(dec_body[3])

                    db_op2.update_upload(applicant_cred_id, fin_task, f_name)

                    if fin_task == 'photo_element_detect':
                        self.next_task_chan.basic_publish(
                            exchange='',
                            routing_key='photo_element_detect_queue',
                            body=json.dumps([applicant_cred_id, f_name]),
                            properties=pika.BasicProperties(delivery_mode=2)
                        )
                    elif fin_task == 'face_detect':
                        print('publishing at face_detect')
                        self.next_task_chan.basic_publish(
                            exchange='',
                            routing_key='face_detect_queue',
                            body=json.dumps([applicant_cred_id, f_name]),
                            properties=pika.BasicProperties(delivery_mode=2)
                        )
                    elif fin_task == 'gender_detect':
                        self.next_task_chan.basic_publish(
                            exchange='',
                            routing_key='gender_detect_queue',
                            body=json.dumps([applicant_cred_id, f_name]),
                            properties=pika.BasicProperties(delivery_mode=2)
                        )

                except Exception as e1:
                    print(e1.message)
                    db_op2.update_upload(applicant_cred_id, fin_task, f_name, success=False)
            except Exception as e:
                print(e.message)
            finally:
                ch.basic_ack(delivery_tag=method.delivery_tag)

        # self.next_task_chan.basic_publish(
        #     exchange='events', routing_key=self.send_publish_routing_key, body=str(f_name)
        # )
        return cb_file_store

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


# work_path = '/home/iamtheuserofthis/Music/image_queue'
im_save_worker = ImageSaveWorker('image_store', '/image_uploads')
im_save_worker.start_worker()
