# seed.py
import os
import csv
import uuid
import mysql.connector
from mysql.connector import Error

# Read DB creds from environment or use defaults
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PWD = os.getenv("MYSQL_PWD", os.getenv("MYSQL_PASSWORD", ""))
DB_PORT = int(os.getenv("MYSQL_PORT", "3306"))

DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"


def connect_db():
    """
    Connect to MySQL server (no specific database).
    Returns connection or None.
    """
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PWD,
            port=DB_PORT,
            autocommit=True,
        )
        return conn
    except Error as e:
        print("Error connecting to MySQL server:", e)
        return None


def create_database(connection):
    """
    Create ALX_prodev database if it does not exist.
    """
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        cursor.close()
    except Error as e:
        print("Error creating database:", e)
        raise


def connect_to_prodev():
    """
    Connect to the ALX_prodev database.
    """
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PWD,
            database=DB_NAME,
            port=DB_PORT,
            autocommit=True,
        )
        return conn
    except Error as e:
        print("Error connecting to ALX_prodev:", e)
        return None


def create_table(connection):
    """
    Create user_data table if not exists with schema:
    user_id CHAR(36) PRIMARY KEY (UUID), name, email, age (DECIMAL)
    Also creates an index on user_id and email.
    """
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        age DECIMAL(3,0) NOT NULL,
        INDEX idx_user_id (user_id),
        INDEX idx_email (email)
    ) ENGINE=InnoDB;
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_sql)
        cursor.close()
        print(f"Table {TABLE_NAME} created successfully")
    except Error as e:
        print("Error creating table:", e)
        raise


def insert_data(connection, csv_path):
    """
    Insert rows from csv_path into user_data table.
    Avoid inserting rows where email already exists.
    csv format expected: "name","email","age" header row included
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"{csv_path} not found")

    insert_sql = f"""
    INSERT INTO {TABLE_NAME} (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """

    # We'll check existing emails to prevent duplicates
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT email FROM {TABLE_NAME};")
        existing = {row[0] for row in cursor.fetchall()}

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            to_insert = []
            for row in reader:
                name = row.get("name") or row.get("full_name") or ""
                email = row.get("email") or ""
                age_str = row.get("age") or "0"
                # Validate/cast age
                try:
                    age = int(float(age_str))
                except Exception:
                    age = 0
                if not email:
                    continue
                if email in existing:
                    continue
                uid = str(uuid.uuid4())
                to_insert.append((uid, name, email, age))
                existing.add(email)

            if to_insert:
                cursor.executemany(insert_sql, to_insert)
                print(f"Inserted {cursor.rowcount} rows into {TABLE_NAME}")
            else:
                print("No new rows to insert")
        cursor.close()
    except Error as e:
        print("Error inserting data:", e)
        raise
