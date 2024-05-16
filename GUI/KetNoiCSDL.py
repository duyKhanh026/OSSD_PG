import mysql.connector

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gamepython"
        )
        print("Connected to MySQL")
        return connection
    except mysql.connector.Error as error:
        print("Error connecting to MySQL:", error)
        return None

def get_account_list():
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM account")
            account_list = cursor.fetchall()
            return account_list
        except mysql.connector.Error as error:
            print("Error fetching data from MySQL:", error)
        finally:
            connection.close()

# Thử nghiệm hàm
if __name__ == "__main__":
    accounts = get_account_list()
    if accounts:
        print("List of accounts:")
        for account in accounts:
            print(account)
