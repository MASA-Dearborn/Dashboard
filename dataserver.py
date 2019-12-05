# Data server

import argparse
import json

from masalib import PacketReceiver
from masalib import SQLInterface

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", type=str, help="Path to configuration file")
    
    args = parser.parse_args()

    with open(args.config, "r") as fp:
        config = json.reads(fp.read())

    receiver = PacketReceiver(9990, "11001")
    database = SQLInterface("dean", "password", "main")

    while True:
        pass


if __name__ == "__main__":
    main()
