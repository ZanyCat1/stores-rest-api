from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from resources.store import StoreList

class Item(Resource):
	#condense these two parsers down a bit, so they at least pull from the same base or however that works
	parser = reqparse.RequestParser()
	parser.add_argument('price',
											type=float,
											required=True,
											help="This field cannot be left blank!"
											)
	parser.add_argument('store_id',
											type=int,
											required=True,
											help="Every item needs a store id."
											)

	delete_parser = reqparse.RequestParser()
	delete_parser.add_argument('store_id',
														type=int,
														required=True,
														help="Every item needs a store id."
														)


	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {'message': 'Item not found'}, 404

	@jwt_required()
	def post(self, name):
		data = Item.parser.parse_args()
		rval = []
		if ItemModel.find_by_name(name):
			for store in StoreList.get(self)['stores']:
				if store['store_id'] == data['store_id']:
					for item in store['items']:
						if item['name'] == name:
							return {'message': "An item with name '{}' already exists in store '{}'.".format(name, data['store_id'])}, 400
#	
		item = ItemModel(name, **data)
		
		try:
			item.save_to_db()
		except:	
			return {"message": "An error occurred inserting the item."}, 500 #Internal Server Error

		return item.json(), 201

	@jwt_required()
	def delete(self, name):
		item_to_delete = ""
		data = Item.delete_parser.parse_args()
		if ItemModel.find_by_name(name):
			for store in StoreList.get(self)['stores']:
				if store['store_id'] == data['store_id']:
					for item in store['items']:
						if item['name'] == name:
							item_to_delete = ItemModel.find_by_name(name)
		if item_to_delete:
			item_to_delete.delete_from_db()
			return {"message": "Item '{}' deleted.".format(name)}
		return {"message": "Item '{}' not found".format(name)}
	
	@jwt_required()
	def put(self, name):
		data = Item.parser.parse_args()

		item = ItemModel.find_by_name(name)

		if item is None:
			#item = ItemModel(name, data['price'], data['store_id'])
			item = ItemModel(name, **data)
		else:
			item.price = data['price']

		item.save_to_db()

		return item.json(), 201


class ItemList(Resource):
	@classmethod
	def get(self):
		return {'items': [item.json() for item in ItemModel.query.all()]} #List comprehension
		#return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))} #Lambda
