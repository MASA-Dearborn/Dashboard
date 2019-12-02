# Packet Receiver 

import socket
import numpy as np 
import time
import sys
import threading

from masalib import PacketSender

class PacketReceiver():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.data = {}

        self.crc = "11001"

        self.thread = threading.Thread(target=self.receive)

    def receive(self):
        """The main packet receiving loop for the PacketReceiver."""
        
        while True:
            data, server = self.sock.recvfrom(1024)

            data_list = PacketSender._convert_hexstring_to_bytelist(data)

            if PacketSender._compute_crc_remainder(data_list, self.crc) != [0]:
                self.sock.sendto("7E".encode(), server)
                continue
            
            self.sock.sendto("00".encode(), server)

            if data_list[0] not in self.data:
                self.data[data_list[0]] = []

            self.data[data_list[0]].append(data_list[1:-1])


