from flask import Flask
from flask_restful import Api
from resources.enqueue_task import PhotoElementDetection

app = Flask(__name__)
api = Api(app)

api.add_resource(PhotoElementDetection, '/test_photo')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3004,debug=True)