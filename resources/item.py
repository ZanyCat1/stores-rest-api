from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from resources.store import Store, StoreList, StoreModel
from Validations import MoreValidations, ItemValidations

class Item(Resource):
	#condense these two parsers down a bit, so they at least pull from the same base or however that works
	parser = reqparse.RequestParser()
	parser.add_argument('price',
											type=float,
											required=True,
											help="This field cannot be left blank!"
											)
	parser.add_argument('store',
											type=str,
											required=True,
											help="Every item needs a store identifier (name or id)."
											)

	delete_parser = reqparse.RequestParser()
	delete_parser.add_argument('store',
														type=str,
														required=True,
														help="Every item needs a store identifier (name or id)."
														)


	@jwt_required()
	def post(self, item):
		data = MoreValidations.strip_from_parser(Item.parser.parse_args())
		item = item.strip()
		validated_item = ItemValidations.validate_item_post(item, **data)
		try:
			validated_item.save_to_db()
			return validated_item.json(), 201
		except:
			return validated_item, 500 #Internal Server 

	#@jwt_required()
	def get(self, item):
		item = item.strip()
		results = ItemValidations.validate_item_get(item)
		if results:
			 return results
		return {"message": "Item '{}' not found".format(item)}, 404

	@jwt_required()
	def put(self, item):
		data = MoreValidations.strip_from_parser(Item.parser.parse_args())
		item = item.strip()
		validated_item = ItemValidations.validate_item_put(item, data['store'], data['price'])
		if validated_item:	
			validated_item.save_to_db()
			return validated_item.json(), 201
		return {"message": "No such store '{}' found".format(data['store'])}

	@jwt_required()
	def delete(self, item):
		data = MoreValidations.strip_from_parser(Item.delete_parser.parse_args())
		item = item.strip()
		item_to_delete = ItemValidations.validate_item_delete(data['store'], item)
		if item_to_delete:
			item_to_delete.delete_from_db()
			return {"message": "Item '{}' costing {}, deleted from store {}".format(item, item_to_delete.price, data['store'])}
		return {"message": "Item '{}' not found in store '{}'".format(item, data['store'])}
	

class ItemList(Resource):
	@classmethod
	def get(self):
		return ItemModel.get_all()
		#return {'items': [{"Item name": item.name, "Item price": item.price, "Store id": item.store_id} for item in ItemModel.query.all()]} #List comprehension

	@classmethod
	def delete(self):
		for item in ItemList.get()['items']:
			if item['Store id'] == None:
				ItemModel.find_by_name(item['Item name']).delete_from_db()
		return "Cleaned up all orphan items"
