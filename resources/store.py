from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel
from models.item import ItemModel
from Validations import MoreValidations, StoreValidations

class Store(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('new_name',
											type=str,
											required=True,
											help="Must provide a store name."
											)

	@jwt_required()
	def post(self, store):
		store = store.strip()
		validated_store = StoreValidations.validate_store_post(store)
		try:
			validated_store.save_to_db()
			return validated_store.json(), 201
		except:
			return validated_store 
	
	def get(self, store):
		store = store.strip()
		validated_store = StoreValidations.validate_store_get(store)
		try:
			return validated_store.json()
		except:
			return validated_store

	@jwt_required()
	def put(self, store):
		data = MoreValidations.strip_from_parser(Store.parser.parse_args())
		store = store.strip()
		validated_store = StoreValidations.validate_store_put(data['new_name'], store)
		try:
			StoreValidations.put_validated_store(validated_store, data['new_name'])
			return "Changed store '{}' to '{}'".format(store, data['new_name']), 201
		except:
			return validated_store

	@jwt_required()
	def delete(self, store):
		store = store.strip()
		validated_store = StoreValidations.validate_store_delete(store)
		try:
			StoreValidations.delete_validated_store(validated_store)
			return {'message': "Store '{}', id '{}' deleted".format(validated_store.name, validated_store.id)}
		except:
			return validated_store


class StoreList(Resource):
	def get(self):
		return {'stores': [store.json() for store in StoreModel.query.all()]}