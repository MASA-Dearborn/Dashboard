# Packet Receiver 

import socket
import numpy as np 
import time
import sys
import threading
import queue

class PacketReceiver():
    def __init__(self, port, crc):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = (socket.gethostbyname(socket.gethostname()), port)
        #self.address = ("127.0.0.1", 9990)
        self.sock.bind(self.address)

        self.data = {}

        self.crc = crc

        self.thread = threading.Thread(target=self.receive)
        self.thread.daemon = True
        self.thread.start()
    
    def init_data_item(self, header):
        if header not in self.data:
            self.data[header] = queue.Queue(0)
    
    @staticmethod
    def _convert_byte_to_bitlist(byt):
        """
        Converts a byte to a list of bits

        Parameters:
        byt (int): A integer valued between 0 and 255

        Returns:
        list: A list of integers with values 0 and 1
        """

        byt_list = [int(i) for i in bin(byt)[2:].zfill(8)]
        return byt_list

    @staticmethod
    def _convert_bytelist_to_bitlist(bytelist):
        """
        Converts a list of bytes to a list of bits

        Parameters:
        bytelist (list): A list of integers with values 0 to 255

        Returns:
        list: A list of integers with values 0 and 1
        """

        bitlst = []
        for byt in bytelist:
            bitlst += (PacketReceiver._convert_byte_to_bitlist(byt))
    
        return bitlst
    
    @staticmethod
    def _convert_bitlist_to_bytelist(bitlist):
        """
        Converts a list of bits to a list of bytes.

        Parameters:
        bitlist (list): List of integers with values 0 and 1

        Returns:
        list: List of integers with values between 0 and 255
        """

        bytlist = []
        byte_count = (len(bitlist) // 8)

        for byte_num in range(byte_count):
            byt = 0
            for i in range(byte_num * 8, (byte_num + 1) * 8):
                byt += bitlist[i] << (len(bitlist) - i - 1)
        
            bytlist.append(byt)
    
        return bytlist
    
    @staticmethod
    def _convert_bitstring_to_bitlist(bitstring):
        """
        Converts a string to bits to list of bits.

        Parameters:
        bitstring (str): A string containing only 0 and 1

        Returns:
        list: List of integers in the of 0 and 1
        """

        bitlst = []
        for i in bitstring:
            bitlst.append(int(i))

        return bitlst
    
    @staticmethod
    def _convert_hexstring_to_bytelist(hexstr):
        """
        Converts a hexstring to a list of bytes.

        Parameters:
        hexstr (str): Even length string containing characters 0 to F

        Returns:
        list: List of integers between 0 and 255
        """

        bytlst = []
        for i in range(int(len(hexstr) / 2)):
            byt = int(hexstr[i*2:i*2+2], 16)
            bytlst.append(byt)
        
        return bytlst
    
    @staticmethod
    def compute_crc_remainder(bytelist, crc):
        """
        Computes the crc remainder of a CRC on a list of bytes.

        Parameters:
        bytelist (list): A list of bytes 
        crc (str): A string of 0's and 1's representing a crc

        Returns:
        list: List of remainder bytes to be appended to end of new list
        """

        crc_list = PacketReceiver._convert_bitstring_to_bitlist(crc)
        crc_len = len(crc_list)
        full_crc_len = (((crc_len - 1) // 8) + 1) * 8
        index = 0
    
        bitlist = PacketReceiver._convert_bytelist_to_bitlist(bytelist)
    
        while True:
            while(bitlist[index] != 1 and index < len(bitlist) - 1):
                index += 1
        
            if index >= len(bitlist) - crc_len:
                break
        
            xorlist = []
            for (i, j) in zip(bitlist[index:], crc_list):
                xorlist.append(i ^ j)
            
            bitlist[index:index+crc_len] = xorlist
    
        return PacketReceiver._convert_bitlist_to_bytelist(bitlist[-full_crc_len:])

    def receive(self):
        """The main packet receiving loop for the PacketReceiver."""
        
        while True:
            data, server = self.sock.recvfrom(1024)

            data_list = PacketReceiver._convert_hexstring_to_bytelist(data)

            if PacketReceiver.compute_crc_remainder(data_list, self.crc) != [0]:
                self.sock.sendto("7E".encode(), server)
                continue
            
            self.sock.sendto("00".encode(), server)

            self.data[data_list[0]].put(data_list[2:-1])


