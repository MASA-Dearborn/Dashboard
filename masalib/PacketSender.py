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

    @staticmethod
    def _convert_byte_to_bitlist(byt):
        byt_list = [int(i) for i in bin(byt)[2:].zfill(8)]
        return byt_list

    @staticmethod
    def _convert_bytelist_to_bitlist(bytelist):
        bitlst = []
        for byt in bytelist:
            bitlst += (PacketSender._convert_byte_to_bitlist(byt))
    
        return bitlst
    
    @staticmethod
    def _convert_bitlist_to_bytelist(bitlist):
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
        bitlst = []
        for i in bitstring:
            bitlst.append(int(i))

        return bitlst
    
    @staticmethod
    def _convert_bytelist_to_hexstring(byts):
        msg = ""
        for n in byts:
            msg += str(hex(n)[2:]).zfill(2)
        
        return msg

    @staticmethod
    def _convert_hexstring_to_bytelist(hexstr):
        bytlst = []
        for i in range(int(len(hexstr) / 2)):
            byt = int(hexstr[i*2:i*2+2], 16)
            bytlst.append(byt)
        
        return bytlst
    
    @staticmethod
    def _compute_crc_remainder(bytelist, crc):
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
    
    def send_random_packet(self, length, crc, count=0):
        crc_bytes = (len(crc) - 1) // 8 + 1

        packet = np.append(126, count)
        packet = np.append(packet, np.random.randint(256, size=length))
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

            try:
                data, server = self.sock.recvfrom(1024)
            except KeyboardInterrupt:
                sys.exit(0)
            
            data_list = PacketSender._convert_hexstring_to_bytelist(data)
            
            if PacketSender._compute_crc_remainder(data_list, crc) == [0]:
                break
            
            self.drops += 1
            print("Resending packet")

        receive_time = time.time_ns()

        deltat = receive_time - send_time

        self.latency_list.append(deltat)
        self.drop_rate_list.append(self.drops / self.sends)

    def send_packet(self, data, crc, header=126, count=0):
        pass
    
    def plot_latency_list(self, filename):
        plt.plot(self.latency_list)
        plt.title("Latency per Packet")
        plt.xlabel("Packet")
        plt.ylabel("Latency (ns)")
        plt.ylim(bottom=0)
        plt.savefig(filename)

    def plot_drop_rate_list(self, filename):
        plt.plot(self.drop_rate_list)
        plt.title("Drop Rate Over Time")
        plt.xlabel("Packet")
        plt.ylabel("Drop Rate (%)")
        plt.ylim(bottom=0, top=1)
        plt.savefig(filename)

    def close_socket(self):
        self.sock.close()