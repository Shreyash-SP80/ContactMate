import mysql.connector
from mysql.connector import Error
import streamlit as st


class Database:
    def __init__(self):
        self.connection = None
        self.connect()  # connect immediately

    # -----------------------------------------
    #   CONNECT TO LOCAL MYSQL
    # -----------------------------------------
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",          # change if needed
                password="",          # change if needed
                database="vishal",
                charset='utf8',
                use_unicode=True
            )

            if self.connection.is_connected():
                self.create_database()
                self.create_users_table()

        except Error as e:
            st.error(f"Error connecting to MySQL: {e}")

    # -----------------------------------------
    #   CREATE MAIN DATABASE (IF NOT EXISTS)
    # -----------------------------------------
    def create_database(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS vishal")
            cursor.execute("USE vishal")
        except Error as e:
            st.error(f"Error creating database: {e}")

    # -----------------------------------------
    #   CREATE USERS TABLE
    # -----------------------------------------
    def create_users_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        except Error as e:
            st.error(f"Error creating users table: {e}")

    # -----------------------------------------
    #   CREATE CONTACT TABLE FOR EACH USER
    # -----------------------------------------
    def create_user_contacts_table(self, username):
        try:
            cursor = self.connection.cursor()
            table_name = f"contacts_{username.replace(' ', '_').lower()}"

            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    phone VARCHAR(50) NOT NULL,
                    email VARCHAR(255),
                    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_phone (phone),
                    UNIQUE KEY unique_email (email)
                )
            """)
            return True

        except Error as e:
            st.error(f"Error creating contacts table: {e}")
            return False

    # -----------------------------------------
    #   RETURN MYSQL CONNECTION
    # -----------------------------------------
    def get_connection(self):
        return self.connection
 