import mysql.connector

from sqlalchemy import create_engine

# e = create_engine("mysql://Sql1239980:71f6778t4x@89.46.111.70", )

engine = create_engine("mysql+pymysql://Sql1239980:71f6778t4x@89.46.111.70:3306/Sql1239980_2", echo=True)
print(engine.table_names())


# db = mysql.connector.connector(
#     host="89.46.111.70",
#     user="Sql1239980",
#     password="71f6778t4x"
# Sql1239980_2
# )

h = 4