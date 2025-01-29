import mysql.connector
from config import DB_CONFIG


def get_connection():
    """Establish a connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)
