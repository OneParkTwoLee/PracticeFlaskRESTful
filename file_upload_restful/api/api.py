from flask import Flask
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
from datetime import datetime
from models import FileModel
import status
from pytz import utc

# for file upload
import werkzeug
from PIL import Image


class FileManager():
    last_id = 0
    def __init__(self):
        self.files = {}

    def insert_file(self, file):
        self.__class__.last_id += 1
        file.id = self.__class__.last_id
        self.files[self.__class__.last_id] = file

    def get_file(self, id):
        return self.files[id]

    def delete_file(self, id):
        del self.files[id]


file_fields = {
    'id': fields.Integer,
    'uri': fields.Url('file_endpoint'),
    'creation_date': fields.DateTime,
    'size': fields.String
}


file_manager = FileManager()


class File(Resource):
    def abort_if_file_doesnt_exist(self, id):
        if id not in file_manager.files:
            abort(status.HTTP_404_NOT_FOUND, message="File {0} doesn't exist".format(id))

    @marshal_with(file_fields)
    def get(self, id):
        self.abort_if_file_doesnt_exist(id)
        return file_manager.get_file(id)

    def delete(self, id):
        self.abort_if_file_doesnt_exist(id)
        file_manager.delete_file(id)
        return '', status.HTTP_204_NO_CONTENT


class FileList(Resource):
    @marshal_with(file_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', required=True, help='File cannot be blank!')
        args = parser.parse_args()
        
        img = Image.open(args['file'])
        
        file = FileModel(
            creation_date=datetime.now(utc),
            size=img.size
            )
        file_manager.insert_file(file) 
        return file, status.HTTP_201_CREATED


app = Flask(__name__)
api = Api(app)
api.add_resource(FileList, '/api/files/')
api.add_resource(File, '/api/files/<int:id>', endpoint='file_endpoint')


if __name__ == '__main__':
    app.run(debug=True)