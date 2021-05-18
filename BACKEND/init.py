from flask import Flask, request, jsonify
import mysql.connector
import config
from mysql.connector import errorcode


app = Flask(__name__)


class SQLConnector():
	def __init__(self):
		try:
			connection = mysql.connector.connect(**config.sql)
			if connection:
				print('Succesfilly connected to ' + config.sql['database'] + 'database')
			else:
				error_id, error = 100, f"Couldn't connect to database: {config.sql['database']}"
				return error_id, error
			connection.close()
		except mysql.connector.Error as error:
			if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with your user name or password")
			elif error.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(error)

	def addUser(self, user=str):
		try:
			connection =  mysql.connector.connect(**config.sql)
			cursor = connection.cursor()

			cursor.execute("SELECT * FROM users WHERE user =%s", (user,))
			if not cursor.fetchall():
				query = "INSERT INTO  users (user) SELECT %s FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM users WHERE user = %s)"
				cursor.execute(query, (user,user))
				connection.commit()
				cursor.close()
				connection.close()
				return True, f"Succesfilly added user {user}"
			else:
				return False, "User already exists"
		except:
			error_id, error = 101, f"Couldn't create user: {user}"
			return error_id, error
			
	def getUser(self, user):
		try:
			connection =  mysql.connector.connect(**config.sql)
			cursor = connection.cursor()
	
			cursor.execute("SELECT * FROM users WHERE user =%s", (user,))
			response = cursor.fetchall()
			if not response:
				self.addUser(user)
				return self.getUser(user)
			else:
				return response
			cursor.close()
			connection.close()
		except:
			error_id, error = 102, f"Couldn't get user: {user}"
			return error_id, error


	def updateStatus(self, user, status):
		try:
			if not self.getUser(user):
				return f"User not found, {user}"
			else:
				connection =  mysql.connector.connect(**config.sql)
				cursor = connection.cursor()

				cursor.execute("UPDATE users SET status = %s WHERE user = %s", (status, user))
				connection.commit()

				cursor.close()
				connection.close()
				return True, f"Succesfilly updated {user}'s status to {status}"
			return False
		except:
			error_id, error = 103, f"Couldn't change user's status : {user}, {status}"
			return error_id, error

	def removeUser(self, user, reason="Why not?"):
		try:
			connection =  mysql.connector.connect(**config.sql)
			cursor = connection.cursor()

			cursor.execute("DELETE FROM users WHERE user =%s", (user,))
			connection.commit()

			cursor.close()
			connection.close()
			return True, f"User {user} succesfilly removed with reason: {reason}"
		except:
			error_id, error = 104, f"Couldn't remove user: {user}, {reason}"
			# return error_id, error


db = SQLConnector()

@app.route('/')
def hello_world():
	return "ReiVan's privacy website"

@app.route('/addUser')
def ApiAddUser():
	if 'user' in request.args:
		user = request.args['user']
	else:
		return jsonify('Give a user')
	return jsonify(db.addUser(user))

@app.route('/getUser')
def ApiGetUser():
	if 'user' in request.args:
		user = request.args['user']
	else:
		return jsonify('Give a user')
	return jsonify(db.getUser(user))

@app.route('/updateStatus')
def ApiUpdateStatus():
	if 'user' and 'status' in request.args:
		user = request.args['user']
		status = request.args['status']
	else:
		return jsonify('Give a user and status')
	return jsonify(db.updateStatus(user, status))

@app.route('/removeUser')
def ApiRemoveUser():
	if 'user' and 'reason' in request.args:
		user = request.args['user']
		reason = request.args['reason']
	else:
		return jsonify('Give a user and reason')
	return jsonify(db.removeUser(user, reason))

"""DOCUMENTATION:"""

"""Error 100 Couldn't connect to database Class: SQLConnector, function __init__ """
"""Error 101: Couldn't create user Class: SQLConnector, function addUser """
"""Error 102: Couldn't get user Class: SQLConnector, function getUser """
"""Error 103: Couldn't cange user's status class: SQLConnector, function updateStatus """
"""Error 104: Couldn't remove user Class: SQLConnector, function removeUser """