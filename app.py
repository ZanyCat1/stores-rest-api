import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
#try:
#	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
#except:
#	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')

try:
	if os.environ.get('DATABASE_URL').startswith("postgres://"):
		app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
	else:
		print("else:")
		app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
except:
	print("Did something break? not connected to any databases")
	
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<store>')
#api.add_resource(Store, '/store/<string:name>', '/store/<int:id>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<item>')
api.add_resource(ItemList, '/items')

api.add_resource(UserRegister, '/register')

@app.route('/')
def hello():
	return {"Hello": "Did this update?"}

if __name__ == '__main__':
	from run import *
	db.init_app(app)
	app.run(port=5001, debug=True)


																								  