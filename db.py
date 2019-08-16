import mysql.connector
import conndets
#Details for db login
q_username = conndets.user
q_password = conndets.pswd
q_host = conndets.host
q_database = conndets.db

def query(sql):
	try:
		conn = mysql.connector.connect(user=q_username, password=q_password, host=q_host, database=q_database)
		cur = conn.cursor()
		cur.execute(sql)
		return cur.fetchall()
	except mysql.connector.Error as error :
		conn.rollback() #rollback if any exception occured
		print("Failed calling record. {}".format(error))
	
def insert(sql, val):
	try:
		conn = mysql.connector.connect(user=q_username, password=q_password, host=q_host, database=q_database)
		cur = conn.cursor()
		cur.execute(sql, val)
		conn.commit()
	except mysql.connector.Error as error :
		conn.rollback() #rollback if any exception occured
		print("Failed inserting record. {}".format(error))
		
def delete(sql):
	try:
		conn = mysql.connector.connect(user=q_username, password=q_password, host=q_host, database=q_database)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
	except mysql.connector.Error as error :
		conn.rollback() #rollback if any exception occured
		print("Failed deleting record. {}".format(error))

def update(sql):
	try:
		conn = mysql.connector.connect(user=q_username, password=q_password, host=q_host, database=q_database)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
	except mysql.connector.Error as error :
		conn.rollback() #rollback if any exception occured
		print("Failed updating record. {}".format(error))
