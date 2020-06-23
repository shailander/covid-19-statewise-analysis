import mysql.connector

class DbConnector:
    my_db = None
    cursor = None

    def __init__(self):
        """
        Initializes DbConnector instance.

        """
        # create a db handle
        self.my_db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="123Nineleap",
            database="test"
        )
        self.cursor = self.my_db.cursor(buffered=True)

    def save(self):
        # commit database operation
        self.my_db.commit()

    def table_creation(self):
        query = """CREATE TABLE IF NOT EXISTS covid_data (
        active INT,
        confirmed INT,
        deaths INT,
        recovered INT,
        state VARCHAR(20),
        date DATE
        )"""
        self.cursor.execute(query)