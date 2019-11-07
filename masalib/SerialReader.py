# Serial Reader 

import serial
import threading

class SerialReader():
    def __init__(self, port, speed, start_byte=126, stop_byte=127):
        self.ser = serial.Serial(port, speed)
        self.buffer = []
        self.packet_list = []

        self.start_byte = start_byte
        self.stop_byte = stop_byte

        self.thread = threading.Thread(target=self.read)
        self.thread.start()
    
    def read(self):
        while True:
            new_byte = int(self.ser.read())

            if new_byte == self.start_byte:
                self.buffer.clear()
            elif new_byte == self.stop_byte:
                self.packet_list.append(self.buffer[:])
            else:
                self.buffer.append(new_byte)

    def close_port(self):
        self.ser.close()
        self.thread.join()