# Packet Sender

import numpy as np
import socket
import time
import sys
import matplotlib.pyplot as plt

class PacketSender():
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (ip, port)
        self.latency_list = []
        self.drop_rate_list = []

        self.sock.settimeout(5.0)

        self.drops = 0
        self.sends = 0

        self.counter = 0

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
            bitlst += (PacketSender._convert_byte_to_bitlist(byt))
    
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
    def _convert_bytelist_to_hexstring(byts):
        """
        Converts a list of bytes to a hexstring.

        Parameters:
        byts (list): List of integers between 0 and 255

        Returns:
        str: Even length string containing character 0 to F
        """

        msg = ""
        for n in byts:
            msg += str(hex(n)[2:]).zfill(2)
        
        return msg

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
    def _compute_crc_remainder(bytelist, crc):
        """
        Computes the crc remainder of a CRC on a list of bytes.

        Parameters:
        bytelist (list): A list of bytes 
        crc (str): A string of 0's and 1's representing a crc

        Returns:
        list: List of remainder bytes to be appended to end of new list
        """

        crc_list = PacketSender._convert_bitstring_to_bitlist(crc)
        crc_len = len(crc_list)
        full_crc_len = (((crc_len - 1) // 8) + 1) * 8
        index = 0
    
        bitlist = PacketSender._convert_bytelist_to_bitlist(bytelist)
    
        while True:
            while(bitlist[index] != 1 and index < len(bitlist) - 1):
                index += 1
        
            if index >= len(bitlist) - crc_len:
                break
        
            xorlist = []
            for (i, j) in zip(bitlist[index:], crc_list):
                xorlist.append(i ^ j)
            
            bitlist[index:index+crc_len] = xorlist
    
        return PacketSender._convert_bitlist_to_bytelist(bitlist[-full_crc_len:])
    
    def increment_counter(self):
        self.counter += 1
        self.counter %= 256

    def send_packet(self, data, crc, header=126, count=0):
        """
        Sends a single packet of data.

        Parameters:
        data (list): A list of integers from 0 to 255 to send
        crc (str): A string of 0's and 1's meant to represent a CRC
        header (int): An integer between 0 and 255 to act as a single byte header
        count (int): An integer between 0 and 255 to act as a single byte counter
        """

        pass

    def send_next_serial_packet(self, serial_reader):
        """
        Sends the next packet in the queue of a SerialReader.
        
        Parameters:
        serial_reader (SerialReader): The SerialReader to send a packet from
        """

        if len(serial_reader.packet_queue.qsize()) == 0:
            return 0
        
        crc_bytes = (len(crc) - 1) // 8 + 1

        next_packet = serial_reader.packet_queue.get()

        packet = np.append(serial_reader.header_byte, self.counter)
        packet = np.append(packet, next_packet)
        packet = np.append(packet, [0 for i in range(crc_bytes)])

        checksum = PacketSender._compute_crc_remainder(packet, crc)
        packet[-crc_bytes:] = checksum

        msg = PacketSender._convert_bytelist_to_hexstring(packet)
        new_packet = PacketSender._convert_hexstring_to_bytelist(msg)

        send_time = time.time_ns()

        while True:
            print(msg)
            self.sock.sendto(msg.encode(), self.server_address)

            self.sends += 1

            data, _ = self.sock.recvfrom(1024)
            
            if data == "00":
                break
            
            self.drops += 1
            print("Resending packet")

        receive_time = time.time_ns()

        deltat = receive_time - send_time

        self.latency_list.append(deltat)
        self.drop_rate_list.append(self.drops / self.sends)
    
    def plot_latency_list(self, filename):
        """
        Plots the latency information to a file

        Parameters:
        filename (str): Local filename to save the plot to
        """

        plt.plot(self.latency_list)
        plt.title("Latency per Packet")
        plt.xlabel("Packet")
        plt.ylabel("Latency (ns)")
        plt.ylim(bottom=0)
        plt.savefig(filename)

    def plot_drop_rate_list(self, filename):
        """
        Plots the drop rate information to a file

        Parameters:
        filename (str): Local filename to save the plot to
        """

        plt.plot(self.drop_rate_list)
        plt.title("Drop Rate Over Time")
        plt.xlabel("Packet")
        plt.ylabel("Drop Rate (%)")
        plt.ylim(bottom=0, top=1)
        plt.savefig(filename)

    def close_socket(self):
        """Close the PacketSender's socket."""

        self.sock.close()