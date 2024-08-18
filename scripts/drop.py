import sqlite3

connection = sqlite3.connect("data.db")

# Create a cursor object to interact with the database
cursor = connection.cursor()

# SQL command to drop a table
drop_table_sql = "DROP TABLE IF EXISTS carProblems;"

# Execute the SQL command
cursor.execute(drop_table_sql)

# Commit the changes to the database
connection.commit()

# Close the connection
connection.close()
