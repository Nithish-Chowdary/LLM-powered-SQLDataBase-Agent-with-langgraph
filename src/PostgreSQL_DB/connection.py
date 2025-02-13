import psycopg2

class PostgresDB:

    def __init__(self,db_name:str, user:str, password=None, host:str="localhost", port:int=5432):
        """
        Initialize the connection to the PostgreSQL Database
        :param db_name:
        :param user:
        :param password:
        :param host:
        :param port:
        """
        self.db_name = db_name
        try:
            if password:
                self.connection = psycopg2.connect(
                    dbname=db_name,
                    user=user,
                    password=password,
                    host=host,
                    port=port
                )
            else:
                self.connection = psycopg2.connect(
                    dbname=db_name,
                    user=user,
                    host=host,
                    port=port
                )

            self.cursor = self.connection.cursor()
            print(f"Database connection established successfully with database:{db_name}.\n")
        except Exception as e:
            print(f"Error connecting to the database:{db_name} with error: {e}\n")

    def execute_ddl(self, ddl_query):
        """
        Executes a DDL query (like CREATE TABLE, ALTER TABLE, etc.) that modifies the database schema.
        """
        try:
            # Execute the DDL query
            self.cursor.execute(ddl_query)
            self.connection.commit()  # Commit the transaction (for DDL queries)
            print(f"DDL query executed successfully for database: {self.db_name}.")
        except Exception as e:
            print(f"Failed to execute ddl query for database: {self.db_name} with following error:{e}")
            self.connection.rollback()  # Rollback if error occurs

    def insert_data(self, insert_query, data):
        """
        Inserts data into database tables
        :param insert_query:
        :param data:
        :return:
        """
        try:
            self.cursor.executemany(insert_query, data)
            self.connection.commit()
            print(f"Data inserted successfully inot database: {self.db_name}!")
        except Exception as e:
            print(f"Failed to insert data into database:{self.db_name} with following error: {e}")

    def close_connection(self):
        """
        close the database connection
        """

        try:
            self.cursor.close()
            self.connection.close()
            print(f"Connection to databsse {self.db_name} closed\n")
        except Exception as e:
            print(f"Failed to close connection to database:{self.db_name} with following error:{e}\n")


