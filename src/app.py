import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello' : 'world'}


api.add_resource(HelloWorld, '/')

@app.route('/<name>')
def hello_name(name):
    return f'Hello {name}!'

if __name__ == '__main__':
    app.run(debug = True)

