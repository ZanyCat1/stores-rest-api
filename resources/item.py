from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
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

	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {'message': 'Item not found'}, 404

	@jwt_required()
	def post(self, name):
		if ItemModel.find_by_name(name):
			return {'message': "An item with name '{}' already exists.".format(name)}, 400
		  # You cannot put the same item in two different stores with this implementation. Needs to check
			# if this item exists in the given store_id

		data = Item.parser.parse_args()

		#item = ItemModel(name, data['price'], data['store_id'])
		item = ItemModel(name, **data)
		
		try:
			item.save_to_db()
		except:	
			return {"message": "An error occurred inserting the item."}, 500 #Internal Server Error

		return item.json(), 201

	@jwt_required()
	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()
		
		return {"message": "Item '{}' deleted.".format(name)}
	
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
