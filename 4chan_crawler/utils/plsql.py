import os

import psycopg2
from pathlib import Path
from dotenv import load_dotenv
from utils.logger import Logger
from constants.constants import CHAN_CRAWLER
from psycopg2.extras import execute_values

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

logger = Logger(CHAN_CRAWLER).get_logger()


class PLSQL:
    def __init__(self):
        logger.info("Connecting to PostgreSQL database...")
        DATABASE_URL = os.environ.get("DATABASE_URL")
        logger.debug(f"DATABASE_URL: {DATABASE_URL}")
        self.conn = psycopg2.connect(dsn=DATABASE_URL)
        self.cur = self.conn.cursor()
    
    def execute_query(self, query: str, params=None):
        """
        Execute a query and return the results.
        
        Args:
            query (str): The SQL query to execute
            params (tuple, optional): Parameters for the query
            
        Returns:
            list: List of tuples containing the query results, or empty list on error
        """
        try:
            logger.info("Executing query on PostgreSQL database...")
            logger.debug(f"Query: {query}")
            if params:
                logger.debug(f"Parameters: {params}")
            
            self.cur.execute(query, params)
            
            # Check if the query returns data (SELECT, RETURNING, etc.)
            if self.cur.description:
                records = self.cur.fetchall()
                logger.info(f"Query executed successfully. Fetched {len(records)} record(s).")
                return records
            else:
                # For queries that don't return data (INSERT, UPDATE, DELETE without RETURNING)
                self.conn.commit()
                logger.info(f"Query executed successfully. Rows affected: {self.cur.rowcount}")
                return []
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            self.conn.rollback()
            return []

    def insert_into_db(self, query: str, fields: tuple):
        try:
            if not fields:
                logger.info("No records provided; skipping insert.")
                return
            logger.info("Inserting data into PostgreSQL database...")
            self.cur.execute(query, fields)
            self.conn.commit()
            logger.info("Data inserted successfully.")
        except Exception as e:
            logger.error(f"Error inserting data into PostgreSQL database: {e}")
            self.conn.rollback()

    def get_data_from(self, query, params=None):
        try:
            logger.info("Fetching data from PostgreSQL database...")
            logger.debug(f"Select query: {query}")
            self.cur.execute(query, params)
            records = self.cur.fetchall()
            logger.info("Successfully fetched data from PostgreSQL database...")
            return records
        except Exception as e:
            logger.error(f"Error fetching data from PostgreSQL database: {e}")
            return []

    def insert_bulk_data_into_db(self, query: str, fields: list):
        try:
            if not fields:
                logger.info("No bulk records provided; skipping insert.")
                return
            logger.info("Inserting bulk data into PostgreSQL database...")
            logger.debug(f"Bulk insert query: {query}")
            execute_values(self.cur, query, fields)
            self.conn.commit()
            logger.info("Bulk data inserted successfully.")
        except Exception as e:
            logger.error(f"Error inserting bulk data into PostgreSQL database: {e}")
            self.conn.rollback()

    def close_connection(self):
        self.cur.close()
        self.conn.close()
        logger.info("PostgreSQL connection closed.")
