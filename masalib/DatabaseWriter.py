# Database writer

import sqlite3
import sqlalchemy as db
import os

class SQLiteInterface():
    datatypes = {"int": db.Integer(),
                 "str": db.String(255),
                 "float": db.Float()}   # Dictionary that maps datatype names to datatype variables

    def __init__(self, database):
        if not os.path.exists(database):
            sqlite3.connect(database)   # Create database if it does not already exist
        
        self.engine = db.create_engine("sqlite:///{}".format(database)) # Create SQLAlchemy engine
        self.meta = db.MetaData()                                       # Create database metadata
        self.meta.reflect(bind=self.engine)                             # Bind metadata to database engine
        self.conn = self.engine.connect()                               # Create a database engine

    def create_table(self, name, columns):
        """
        Creates a new SQL table

        Parameters:
        name (str): Name of the table to be created
        columns (list): List of tuples in the format of (column_name, datatype_name) as strings
        """

        try:
            col = (db.Column(name, self.datatypes[typ]) for name, typ in columns)   # Construct a tuple of Column variables
        except KeyError:                                                            # Catch a KeyError if a datatype name doesn't exist
            return None

        table = db.Table(name, self.meta, *col) # Decompress the column list and create the table variable
        self.meta.create_all(self.engine)       # Create the table
    
    def insert(self, table_name, data):
        """
        Inserts a new set of data to a table

        Parameters:
        table_name (str): Name of table to insert data into
        data (dict): Dictionary of data to insert into table
        """

        table = self.meta.tables[table_name]            # Fetch the table variable from the database metadata
        query = db.insert(table)                        # Create an insert query
        values = [data]                                 # Put data into a list
        ResultProxy = self.conn.execute(query, values)  # Execute the query

        return ResultProxy

    def fetch_all(self, table_name):
        """
        Fetches all data in a given table

        Parameters:
        table_name (str): Name of table to fetch data from

        Returns:
        list: List of tuples of data contained in the table
        """
        
        table = db.Table(table_name, self.meta, autoload=True, autoload_with=self.engine)
        query = db.select([table])              # Select all data from the table
        ResultProxy = self.conn.execute(query)  # Execute the query
        ResultSet = ResultProxy.fetchall()      # Fetch data

        return ResultSet    # Return data
