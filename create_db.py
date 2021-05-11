import mysql.connector

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	passwd = r"%Xu&C+5>WAC,6at?+7p{",
	)

my_cursor = mydb.cursor()

#my_cursor.execute("CREATE DATABASE users")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
	print(db)