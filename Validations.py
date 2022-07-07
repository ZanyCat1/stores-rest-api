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
			if StoreModel.find_by_name(store):
				return "Store '{}' already exists".format(store)
			if StoreModel.is_number(store):
				return "Store name cannot be a number"
			return StoreModel(store)
		return False

	def validate_store_get(store):
		if store:
			if StoreModel.find_by_name(store):
				return StoreModel.find_by_name(store)
			if StoreModel.find_by_id(store):
				return StoreModel.find_by_id(store)
			return "Could not find store '{}'".format(store)
		return False

	def validate_store_put(data, store):
		if StoreModel.is_number(data):
			return "Cannot change store name to a number"
		if StoreModel.find_by_name(data):
			return "Cannot change store to existing name '{}'".format(data)
		if StoreModel.is_number(store):
			if StoreModel.find_by_id(store):
				return StoreModel.find_by_id(store)
			else:
				return "Could not find store id '{}'".format(store)
		if StoreModel.find_by_name(store):
			return StoreModel.find_by_name(store)
		else:
			return "Could not find store '{}'".format(store)

	def validate_store_delete(store):
		if store:
			if StoreModel.is_number(store):
				if StoreModel.is_number(store):
					return StoreModel.find_by_id(store)
			if StoreModel.find_by_name(store):
				return StoreModel.find_by_name(store)
			return False
		return False

	def delete_validated_store(store):
		if store:
			for item in store.items:
				item.store_name = None
				item.store_id = None
				item.save_to_db()
			store.delete_from_db()



class ItemValidations():
	def validate_item_post(item, **data):
		check_store = StoreModel.find_by_id(data['store']) or StoreModel.find_by_name(data['store'])
		if check_store:
			if ItemModel.item_exists_in_store(item, check_store):
				return {"message": "'{}' already exists in store '{}'.".format(item, data['store'])}
			return ItemModel(item, **data)
		return {"message": "There is no such store '{}'.".format(data['store'])}

	def validate_item_get(item):
		results = []
		for each_item in ItemModel.get_all()['items']:
			if each_item['Item name'] == item:
				results.append({"Item name": each_item['Item name'], "Item price": each_item['Item price'], "Store name": each_item['Store name'], "Store id": each_item['Store id']})
		return results
		
	def validate_item_put(item, store, price):
		check_store = StoreModel.find_by_id(store) or StoreModel.find_by_name(store)
		if check_store:
			if ItemModel.item_exists_in_store(item, check_store):
				item_to_add = ItemModel.find_by_store_id(store, item) or ItemModel.find_by_store_name(store, item)
				item_to_add.price = price
				return item_to_add
			else:
				item_to_add = ItemModel(item, price, store)
				return item_to_add
		return False

	def validate_item_delete(store, item):
		item_to_delete = ItemModel.find_by_store_id(store, item) or ItemModel.find_by_store_name(store, item)
		if item_to_delete:
			return item_to_delete
		return False

	