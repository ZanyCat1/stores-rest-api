from models.store import StoreModel
from models.item import ItemModel
#from resources.store import StoreModel

class MoreValidations():
	def strip_from_parser(data):
		for element in data:
			try:
				data[element] = data[element].strip()
			except:
				pass
		return data


class StoreValidations():
	def validate_store_post(store):
		if store:
			error_message = ""
			if StoreModel.find_by_name(store):
				error_message = "Store '{}' already exists.".format(store)
			elif StoreModel.is_number(store):
				error_message = "Store name cannot be a number."
			if error_message:
				return {"message" : error_message}, 400
			return StoreModel(store)
		return {"message": "An error occurred finding the store."}, 500

	def validate_store_get(store):
		if store:
			store_to_return = None
			if StoreModel.is_number(store):
				if StoreModel.find_by_id(store):
					store_to_return = StoreModel.find_by_id(store)
			elif StoreModel.find_by_name(store):
				store_to_return = StoreModel.find_by_name(store)
			if store_to_return:
				return store_to_return
		return {"message": "Could not find store '{}'.".format(store)}, 404

	def validate_store_put(data, store):
		error_message = ""
		if StoreModel.is_number(data):
			error_message = "Cannot change store name to a number."
		elif StoreModel.find_by_name(data):
			error_message = "Cannot change store to existing name '{}'.".format(data)
		if error_message:
			return {"message": error_message}, 400
		if StoreModel.find_by_name(store):
			return StoreModel.find_by_name(store)
		if StoreModel.find_by_id(store):
			return StoreModel.find_by_id(store)
		return {"message": "Could not find store '{}'.".format(store)}, 404
		#return {"message": "An error occurred finding the store."}, 500 

	def put_validated_store(store, new_name):
		if store:
			for item in store.items:
				item.store_name = new_name
				item.save_to_db()
			store.name = new_name
			store.save_to_db()
		return "store was null"

	def validate_store_delete(store):							 
		if store:
			if StoreModel.find_by_name(store):
				return StoreModel.find_by_name(store)
			if StoreModel.find_by_id(store):
				return StoreModel.find_by_id(store)
			return {'message': "Store '{}' not found".format(store)}, 404
		return {'message': "There was an error deleting store '{}'.".format(store)}, 500

	def delete_validated_store(store):
		if store:
			for item in store.items:
				item.store_name = None
				item.store_id = None
				item.save_to_db()
			store.delete_from_db()
		return {"message": "Store was null"}, 404


class ItemValidations():
	def validate_item_post(item, **data): 
		if item:
			check_store = ""
			if StoreModel.find_by_name(data['store']):
				check_store = StoreModel.find_by_name(data['store'])
			if StoreModel.find_by_id(data['store']):
				check_store = StoreModel.find_by_id(data['store'])
			if check_store:
				if ItemModel.item_exists_in_store(item, check_store):
					return {"message": "'{}' already exists in store '{}'.".format(item, data['store'])}, 400
				return ItemModel(item, **data)
			return {"message": "There is no such store '{}'.".format(data['store'])}, 404
		return {"message": "An error occurred inserting the item."}, 500

	def validate_item_get(item):
		results = []
		for each_item in ItemModel.get_all()['items']:
			if each_item['Item name'] == item:
				results.append({"Item name": each_item['Item name'], "Item price": each_item['Item price'], "Store name": each_item['Store name'], "Store id": each_item['Store id']})
		if results:
			return results
		return {"message": "Item '{}' not found.".format(item)}, 404 
	
	def validate_item_put(item, store, price):
		if item:
			if StoreModel.find_by_name(store):
				check_store = StoreModel.find_by_name(store)
			elif StoreModel.find_by_id(store):
				check_store = StoreModel.find_by_id(store)
			if check_store:
				if ItemModel.item_exists_in_store(item, check_store):
					item_to_add = ItemModel.find_by_store_name(check_store.name, item)
					item_to_add.price = price
				else:
					item_to_add = ItemModel(item, price, store)
				return item_to_add
			return {"message": "No such store '{}' found.".format(store)}, 404
		return {"message": "An error occurred inserting the item."}, 500 

	def validate_item_delete(store, item):
		if ItemModel.find_by_store_name(store, item):
			item_to_delete = ItemModel.find_by_store_name(store, item)
		#I think making next item elif will keep code from trying to evaluate it with a name when it wants a number
		elif ItemModel.find_by_store_id(store, item):
			item_to_delete = ItemModel.find_by_store_id(store, item)
		try:
			return item_to_delete
		except:
			pass
		return {"message": "Item '{}' not found in store '{}'.".format(item, store)}, 404

	