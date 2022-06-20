import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
uri = os.environ.get('DATABASE_URL','sqlite:///data.db')
if uri.startswith("postgres://"):
	uri = uri.replace("://", "ql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

@app.route('/')
def hello():
	return {"Hello": "This is a store!"}

if __name__ == '__main__':
	db.init_app(app)
	app.run(port=5001, debug=True)


																								  