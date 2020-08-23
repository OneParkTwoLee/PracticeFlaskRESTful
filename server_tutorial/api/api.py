from flask import Flask
from flask_restful import Api, fields, marshal_with, reqparse, Resource
from cat import CatModel
import status

# for file upload
import werkzeug

# for image classification
import aiohttp, asyncio
from io import BytesIO
from fastai import *
from fastai.vision import *

cat_fields = {
    'predicted_label': fields.String
}

# Download model from URL
model_file_url = 'https://www.dropbox.com/s/3ru2uzva9g8f5ll/cat.pth?raw=1'
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
    learn.path = path
    learn.load(model_file_name)
    return learn

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()


class CatList(Resource):
    @marshal_with(cat_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cat', type=werkzeug.datastructures.FileStorage, location='files', required=True, action='append', help='Cat cannot be blank!')
        args = parser.parse_args()
        
        label = ''

        for i, req_img in enumerate(args['cat']):
            img_bytes = req_img.read()
            img = open_image(BytesIO(img_bytes))    

            if i+1 != len(args['cat']):
                label = label + str(learn.predict(img)[0]) + ','
            else:
                label += str(learn.predict(img)[0])

        cat = CatModel(predicted_label=label)
        return cat, status.HTTP_201_CREATED


app = Flask(__name__)
api = Api(app)
api.add_resource(CatList, '/api/cats')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')