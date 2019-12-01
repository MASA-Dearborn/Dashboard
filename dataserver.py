# Data server

import argparse
import json

from masalib import PacketReceiver
from masalib import DatabaseWriter

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", type=str, help="Path to configuration file")
    
    args = parser.parse_args()

    receiver = PacketReceiver()
    database = DatabaseWriter()

    while True:
        database.write(receiver)


if __name__ == "__main__":
    main()
