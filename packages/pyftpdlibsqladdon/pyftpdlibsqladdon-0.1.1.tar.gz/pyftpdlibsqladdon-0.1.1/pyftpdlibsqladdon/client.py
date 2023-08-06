import mysql.connector
from mysql.connector import Error

class SqlClient():

    def sqlUser(user,sql_server_config,sql_query_config):
        SELECT_USER_QUERY = f"SELECT `{sql_query_config['user']}`,`{sql_query_config['password']}`,`{sql_query_config['home']}`,`{sql_query_config['permissions']}` FROM `{sql_query_config['table']}` WHERE `{sql_query_config['user']}`='{user}'"
        try:
            connection = mysql.connector.connect(**sql_server_config)
            if connection.is_connected():
                db_Info = connection.get_server_info()
                #print("Conectado a  MySQL Server version ", db_Info)
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                #print("Estas conectado a la base de datos: ", record)
                cursor.execute(SELECT_USER_QUERY)
                result = cursor.fetchall()
                #print(result)
            #revisamos si la lista esta vacia 
            if not result:
                print("User doesn't exist")
        except Error as e:
            print("Error MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Sql users service end")
            if not result:
                resultVoid = []
                return resultVoid
            else:
                return result
                