# MASA Dashboard Data Client
# By Dean Lawrence

import argparse
import json

from masalib import DataSerialReader, TeleGPSSerialReader, EggFinderSerialReader
from masalib import PacketSender

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", type=str, help="Path to configuration file")
    
    args = parser.parse_args()

    with open(args.config, "r") as fp:
        config = json.loads(fp.read())["client"]    # Read in the client section from the json config

    # Initialize the SerialReaders. Each listens for the processes data from a serial in within its own thread
    receiver_list = []

    receiver_list.append(DataSerialReader(config["readers"]["Data"]["port"], 
                                          config["readers"]["Data"]["speed"], 
                                          header_byte=config["readers"]["Data"]["header"], 
                                          start_byte=config["readers"]["Data"]["start_byte"], 
                                          stop_byte=config["readers"]["Data"]["stop_byte"]))

    receiver_list.append(TeleGPSSerialReader(config["readers"]["TeleGPS"]["port"], 
                                             config["readers"]["TeleGPS"]["speed"], 
                                             header_byte=config["readers"]["TeleGPS"]["header"]))

    receiver_list.append(EggFinderSerialReader(config["readers"]["EggFinder"]["port"], 
                                               config["readers"]["EggFinder"]["speed"], 
                                               header_byte=config["readers"]["EggFinder"]["header"]))

    sender = PacketSender(config["server_ip"], config["server_port"])   # Create the packet sender with the specified ip and port

    while True: # Infinite loop
        for receiver in receiver_list:
            sender.send_next_serial_packet(receiver, config["crc"]) # Iterate the list of receivers and send the next packet if it exists
    
    sender.close_socket()

    sender.plot_latency_list(args.latency)
    sender.plot_drop_rate_list(args.droprate)


if __name__ == "__main__":
    main()

