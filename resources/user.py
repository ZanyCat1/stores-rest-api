import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.user import UserModel

class UserLogin(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username',
											type=str,
											required=True,
											help="This field cannot be blank"
											)
	parser.add_argument('email', 
										 type=str, 
										 required=True, 
										 help="This field cannot be blank" 
										 ) 
	parser.add_argument('password',
											type=str,
											required=True,
											help="This field cannot be blank"
											)

	def post(self):		
		data = UserRegister.parser.parse_args()

		if UserModel.find_by_username(data['username']):		
			connection = sqlite3.connect('data.db')
			cursor = connection.cursor()
			query = "SELECT * FROM users"
			for row in cursor.execute(query):
				if row[2] == data['email']:
					connection.commit()
					connection.close()
					return {"message": "User '{}' logged in successfully.".format(data['username'])}, 201
		return {"message": "User not logged in"}



class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username',
											type=str,
											required=True,
											help="This field cannot be blank"
											)
	parser.add_argument('email', 
										 type=str, 
										 required=True, 
										 help="This field cannot be blank" 
										 ) 
	parser.add_argument('password',
											type=str,
											required=True,
											help="This field cannot be blank"
											)

	def post(self):		
		data = UserRegister.parser.parse_args()

		if UserModel.find_by_username(data['username']):		
			return {"message": "A user with that username already exists"}, 400
	
		UserModel(**data).save_to_db()

		return {"message": "User '{}' created successfully.".format(data['username'])}, 201
				

	def delete(self):		
		data = UserRegister.parser.parse_args()
		
		#can probably trim this down a bit

		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		select_query = "SELECT * FROM users"
		for row in cursor.execute(select_query):
			if row[1] == data['username'] and row[2] == data['email'] and row[3] == data['password']:
				select_query = "DELETE FROM users WHERE username=?"
				cursor.execute(select_query, (data['username'],))
				connection.commit()
				connection.close()
				return {"message": "User '{}' deleted!".format(row[1])}, 201

		return {"message": "User '{}' not found.".format(data['username'])}, 400
