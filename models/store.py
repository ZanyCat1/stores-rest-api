#* If we uncomment these lines and comment out the lines below them, then this will happen:
# The store, upon instantiation, will look through the table and build a compendium of all of its items. 
# That operation will take time, but then calling the store's json() method will be free. 
# Using lazy='dynamic' and self.items.all() the store creation is faster, but each time we want to view the
# store's items we will have to enter the table and that will cost more. 
from db import db

class StoreModel(db.Model):
	__tablename__ = 'stores'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	#items = db.relationship('ItemModel') #* 
	items = db.relationship('ItemModel', lazy='dynamic')

	def __init__(self, name):
		self.name = name

	def json(self):
		#return {'name': self.name, 'items': [item.json() for item in self.items]} #*
		return {'store_id': self.id, 'name': self.name, 'items': [item.json() for item in self.items.all()]}

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()

	@classmethod
	def find_by_id(cls, store_id):
		return cls.query.filter_by(id=store_id).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

	def is_number(input):
		try:
			float(input)
			return True
		except:
			return False

