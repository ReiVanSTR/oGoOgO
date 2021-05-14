from flask import Flask
import mysql.connector
import config
from mysql.connector import errorcode


app = Flask(__name__)


class SQLConnector():
	def __init__(self):
		try:
			self.connection = mysql.connector.connect(**config.sql)
			self.cursor = self.connection.cursor()
			print('Succesfilly connected to ' + config.sql['database'] + 'database')
		except mysql.connector.Error as error:
			if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with your user name or password")
			elif error.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(error)
		else:
			self.connection.close()
			self.cursor.close()

	def addUser(self, user='None'):
		try:
			query = "INSERT INTO users VALUES (?, ?)", (user, 0)
			print(self.cursor.execute(query))
			self.cursor.commit()
			return True
		except:
			error_id, error = 101, f"Couldn't create user: {user}"
			return error_id, error



db = SQLConnector()
print(db.addUser('Admin'))
@app.route('/')
def hello_world():
	return 'Hello from Flask!'


"""DOCUMENTATION:"""

"""Error 101: Couldn't create user Class: SQLConnector, function addUser"""

