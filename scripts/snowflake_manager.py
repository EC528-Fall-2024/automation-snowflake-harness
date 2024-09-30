# File location: scripts/snowflake_manager.py

import logging
from utils.db_utils import get_connection

def create_database(database_name):
    """
    Create a Snowflake database if it does not already exist.
    
    Args:
        database_name (str): The name of the database to create.
    """
    logging.info(f"Attempting to create database: {database_name}")
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name};")
            logging.info(f"Database '{database_name}' created successfully.")
    except Exception as e:
        logging.error(f"Error creating database '{database_name}': {str(e)}")
    finally:
        conn.close()

def create_schema(schema_name):
    """
    Create a Snowflake schema if it does not already exist.
    
    Args:
        schema_name (str): The name of the schema to create.
    """
    logging.info(f"Attempting to create schema: {schema_name}")
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")
            logging.info(f"Schema '{schema_name}' created successfully.")
    except Exception as e:
        logging.error(f"Error creating schema '{schema_name}': {str(e)}")
    finally:
        conn.close()
