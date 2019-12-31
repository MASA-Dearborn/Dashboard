# MASA Dashboard Data Server
# By Dean Lawrence

import argparse
import json
import struct

from masalib import PacketReceiver
from masalib import SQLiteInterface

def convert_bytelist_to_int(bytlst):
    """
    Converts a list of four bytes to a single int

    Parameters:
    bytlst (list): List containing ints from 0 to 255

    Returns:
    int: Int value equal to bytes inputted
    """

    s = 0
    for byt in bytlst:
        s = (s << 8) + byt
    
    return s

def convert_bytelist_to_float(bytlst):
    """
    Converts a list of four bytes to a single float.
        
    Parameters:
    bytlst (list): List containing ints from 0 to 255

    Returns:
    float: Float value equal to bytes inputted
    """
    
    return struct.unpack('>f', bytes(bytlst))[0]

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", type=str, help="Path to configuration file")
    
    args = parser.parse_args()

    with open(args.config, "r") as fp:
        config = json.loads(fp.read())["server"] # Grab the config information for the server
    
    receiver = PacketReceiver(config["port"], config["crc"]) # Create the packet receiver
    database = SQLiteInterface(config["database"])           # Create the SQL database interface

    # If a table in the config doesn't exist in the database, create it
    for table in config["tables"]:
        receiver.init_data_item(config["tables"][table]["header"]) # Initialize the PacketReceiver dictionary

        if not database.does_table_exist(table):
            columns = [(col_name, config["tables"][table]["columns"][col_name]) for col_name in config["tables"][table]["columns"]]
            database.create_table(table, columns)
            print("Created new table:", table)

    # Main processing loop
    while True:
        for table in config["tables"]:
            if receiver.data[config["tables"][table]["header"]].qsize() == 0:
                continue    # If this data queue is empty, move onto next queue

            data = receiver.data[config["tables"][table]["header"]].get() # Get next received packet from receiver

            columns = config["tables"][table]["columns"] # Extract the column metadata

            # Process bytelist data into ints and floats and put into right format
            processed_columns = {}
            data_index = 0
            for column in columns:
                if columns[column] == "int":        # If the config marks column as int, convert to int
                    value = convert_bytelist_to_int(data[data_index:data_index+4])
                elif columns[column] == "float":    # If the config marks column as float, convert to float
                    value = convert_bytelist_to_float(data[data_index:data_index+4])
                
                data_index += 4                     # Increment to next full value
                processed_columns[column] = value   # Store the processed value in the data dictionary

            database.insert(table, processed_columns) # Insert the data into the database table
            print("Writing new entry in table:", table)


if __name__ == "__main__":
    main()
