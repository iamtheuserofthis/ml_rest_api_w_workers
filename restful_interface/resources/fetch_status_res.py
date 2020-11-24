from flask_restful import Resource, reqparse
from flask import jsonify, make_response

from resources.dao import db_fetch_res


class StatusResultFetcher(Resource):
    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument(
            'applicant_cred_id',
            dest='applicant_cred_id',
            required=True, type=int
        )

    def get(self):
        print('reached here')
        args = self.get_parser.parse_args()
        print(args.applicant_cred_id)
        db_reader = db_fetch_res.DBSelectOperations()
        result = db_reader.status_cred_id(args.applicant_cred_id)
        print(make_response(jsonify(result)))
        return make_response(jsonify(result))
