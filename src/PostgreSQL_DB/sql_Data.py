from src.PostgreSQL_DB.connection import PostgresDB

# DDL queries for creating tables
employee_table_creation_query = """
CREATE TABLE IF NOT EXISTS employees (
    emp_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    hire_date TEXT NOT NULL,
    salary REAL NOT NULL
);
"""

customers_table_creation_query = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT
);
"""

orders_table_creation_query = """
CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);
"""

# Insert queries
insert_employees_query = """
INSERT INTO employees (emp_id, first_name, last_name, email, hire_date, salary)
VALUES (%s,%s,%s,%s,%s,%s);
"""

insert_customers_query = """
INSERT INTO customers (customer_id, first_name, last_name, email, phone)
VALUES (%s,%s,%s,%s,%s);
"""

insert_orders_query = """
INSERT INTO orders (order_id, customer_id, order_date, amount)
VALUES (%s,%s,%s,%s);
"""

# Sample data
employee_data = [
    (1, "Sunny", "Savita", "sunny.sv@abc.com", "2023-06-01", 50000.00),
    (2, "Arhun", "Meheta", "arhun.m@gmail.com", "2022-04-15", 60000.00),
    (3, "Alice", "Johnson", "alice.johnson@jpg.com", "2021-09-30", 55000.00),
    (4, "Bob", "Brown", "bob.brown@uio.com", "2020-01-20", 45000.00),
]

customers_data = [
    (1, "John", "Doe", "john.doe@example.com", "1234567890"),
    (2, "Jane", "Smith", "jane.smith@example.com", "9876543210"),
    (3, "Emily", "Davis", "emily.davis@example.com", "4567891230"),
    (4, "Michael", "Brown", "michael.brown@example.com", "7894561230"),
]

orders_data = [
    (1, 1, "2023-12-01", 250.75),
    (2, 2, "2023-11-20", 150.50),
    (3, 3, "2023-11-25", 300.00),
    (4, 4, "2023-12-02", 450.00),
]

# Class for creating tables and inserting data
class CreateDatabase:
    def __init__(self, db_name, user, password=None):
        self.cursor = PostgresDB(db_name=db_name, user=user, password=password)

    def create_tables(self):
        """
        Creating tables inside the database
        """
        try:
            # Execute table creation queries
            self.cursor.execute_ddl(employee_table_creation_query)
            self.cursor.execute_ddl(customers_table_creation_query)
            self.cursor.execute_ddl(orders_table_creation_query)
            print("Tables created successfully\n")
        except Exception as e:
            print(f"Failed to create tables: {e}\n")

    def insert_data(self):
        """
        Insert data into the tables
        """
        try:
            # Insert data into each table
            self.cursor.insert_data(insert_employees_query, employee_data)
            self.cursor.insert_data(insert_customers_query, customers_data)
            self.cursor.insert_data(insert_orders_query, orders_data)
            print("Data inserted successfully\n")
        except Exception as e:
            print(f"Failed to insert data: {e}\n")
        self.cursor.close_connection()