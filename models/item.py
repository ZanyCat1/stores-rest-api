from db import db
from models.store import StoreModel
#from models.item import ItemList

class ItemModel(db.Model):
	__tablename__ = 'items'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	price = db.Column(db.Float(precision=2))
	store_name = db.Column(db.String(80))

	store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
	store = db.relationship('StoreModel')

	def __init__(self, name, price, store):#, store_id, store_name = ""):
		self.name = name
		self.price = price
		try:
			self.store_id = store
			self.store_name = StoreModel.find_by_id(store).name
		except:
			try:
				self.store_id = StoreModel.find_by_name(store).id
				self.store_name = store
			except:
				self.store_id = None
				self.store_name = None
		#self.store_id = store_id
		#self.store_name = StoreModel.find_by_id(store_id)

	def json(self):
		return {'name': self.name, 'price': self.price}

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()

	@classmethod
	def find_by_store_id(cls, this_store_id, this_item_name = ""):
		if this_item_name:
			return cls.query.filter_by(store_id=this_store_id).filter_by(name=this_item_name).first()
		return cls.query.filter_by(store_id=this_store_id).first()

	@classmethod
	def find_by_store_name(cls, this_store_name, this_item_name = ""):
		if this_item_name:
			return cls.query.filter_by(store_name=this_store_name).filter_by(name=this_item_name).first()
		return cls.query.filter_by(store_name=this_store_name).first()

	@classmethod
	def item_exists_in_store(cls, item_to_check, store_to_check):
		for item in store_to_check.items:
			if item.name == item_to_check:
				return True
		return False

	@classmethod
	def get_all(cls):
		return {'items': [{"Item name": item.name, "Item price": item.price, "Store name": item.store_name, "Store id": item.store_id} for item in ItemModel.query.all()]} #List comprehension

	def organize(self, store_object):
		return [({"Item name": item.name, "Item price": item.price, "Item store id": item.store_id}) for item in store_object.items] 

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()


