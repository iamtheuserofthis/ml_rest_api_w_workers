from flask_restful import Resource, fields, reqparse
from flask import jsonify, make_response
import pika
import werkzeug
from resources.file_translator import file_tranlator
from resources.dao import db_operation_insert

class PhotoElementDetection(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(
            'applicant_cred_id',
            dest='applicant_cred_id',
            location='form',
            required=True, type=str
        )

        self.post_parser.add_argument(
            'final_task',
            dest='final_task',
            location='form',
            required=True, type=str,
            choices=('photo_element_detect', 'face_detect', 'gender_detect')
        )

        self.post_parser.add_argument(
            'photoUpload',
            type=werkzeug.datastructures.FileStorage,
            dest='photoUpload',
            location='files',
            required=True
        )
        connection = pika.BlockingConnection(
            pika.URLParameters("amqp://test:test@iamtheuserofthis3.pune.cdac.in:5672")
        )
        self.q_channel = connection.channel()
        self.q_channel.queue_declare(queue='image_store', durable=True)

    def post(self):
        args = self.post_parser.parse_args()
        print(args.applicant_cred_id, args.photoUpload, args.final_task)
        img_id, img_data_b64 = file_tranlator.image_to_json(args.applicant_cred_id, args.photoUpload.read(),
                                                            args.final_task)
        db = db_operation_insert.DBInsertOperations()
        self.q_channel.basic_publish(
            exchange='',
            routing_key='image_store',
            body=img_data_b64,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        self.q_channel.close()
        db.init_record(args.applicant_cred_id, img_id, args.final_task)
        return make_response(jsonify(image_id=img_id, status='successful'))
