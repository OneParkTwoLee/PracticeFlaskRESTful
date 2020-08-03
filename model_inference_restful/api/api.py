from flask import Flask
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
from picture import PictureModel
import status

# for file upload
import werkzeug
from PIL import Image

# for image classification
import aiohttp, asyncio
import time
from io import BytesIO
from fastai import *
from fastai.vision import *


class PictureManager():
    last_id = 0
    def __init__(self):
        self.pictures = {}

    def insert_picture(self, picture):
        self.__class__.last_id += 1
        picture.id = self.__class__.last_id
        self.pictures[self.__class__.last_id] = picture

    def get_picture(self, id):
        return self.pictures[id]

    def delete_picture(self, id):
        del self.pictures[id]


picture_fields = {
    'id': fields.Integer,
    'uri': fields.Url('picture_endpoint'),
    'size': fields.String,
    'reasoning_time': fields.String,
    'predicted_label': fields.String
}


picture_manager = PictureManager()

# Download model from URL
model_file_url = 'https://www.dropbox.com/s/njd726x4h7fgy60/big_cat.pth?raw=1'
model_file_name = 'model'
classes = ['lion', 'tiger']
path = Path(__file__).parent

async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f: f.write(data)

async def setup_learner():
    await download_file(model_file_url, path/'models'/f'{model_file_name}.pth')
    data_bunch = ImageDataBunch.single_from_classes(path, classes,
        ds_tfms=get_transforms(), size=224).normalize(imagenet_stats)
    learn = cnn_learner(data_bunch, models.resnet34, pretrained=False)
    learn.load(model_file_name)
    return learn

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()


class Picture(Resource):
    def abort_if_picture_doesnt_exist(self, id):
        if id not in picture_manager.pictures:
            abort(status.HTTP_404_NOT_FOUND, message="Picture {0} doesn't exist".format(id))

    @marshal_with(picture_fields)
    def get(self, id):
        self.abort_if_picture_doesnt_exist(id)
        return picture_manager.get_picture(id)

    def delete(self, id):
        self.abort_if_picture_doesnt_exist(id)
        picture_manager.delete_picture(id)
        return '', status.HTTP_204_NO_CONTENT


class PictureList(Resource):
    @marshal_with(picture_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files', required=True, help='Picture cannot be blank!')
        args = parser.parse_args()
        
        img_bytes = args['picture'].read()
        img = open_image(BytesIO(img_bytes))
        
        start = time.time()
        label = learn.predict(img)[0]
        end = time.time()

        picture = PictureModel(
            size=img.size,
            reasoning_time=end-start,
            predicted_label=label
            )
        picture_manager.insert_picture(picture) 
        return picture, status.HTTP_201_CREATED


app = Flask(__name__)
api = Api(app)
api.add_resource(PictureList, '/api/pictures/')
api.add_resource(Picture, '/api/pictures/<int:id>', endpoint='picture_endpoint')


if __name__ == '__main__':
    app.run(debug=True)