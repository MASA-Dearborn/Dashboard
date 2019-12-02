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
        pass
    
    def check_crc(self, data, crc):
        pass

    def close_port(self):
        self.ser.close()
        self.thread.join()

class DataSerialReader(SerialReader):
    def __init__(self, port, speed, start_byte=126, stop_byte=127):
        super().__init__(port, speed, start_byte, stop_byte)
    
    def read(self):
        while True:
            new_byte = int(self.ser.read())

            if new_byte == self.start_byte:
                self.buffer.clear()
            elif new_byte == self.stop_byte:
                self.packet_list.append(self.buffer[:])
            else:
                self.buffer.append(new_byte)

class TeleGPSSerialReader(SerialReader):
    def __init__(self, port, speed, start_byte=126, stop_byte=127):
        self.current_string = ""
        self.header = ["T", "E", "L", "E", "M"]
        self.length = 0
        self.crc_mask = 2 ** 7
        self.packet_length = 64

        super().__init__(port, speed, start_byte, stop_byte)

    @staticmethod
    def convert_hexstring_to_bytelist(hexstr):
        bytlst = []
        for i in range(int(len(hexstr) / 2)):
            byt = int(hexstr[i*2:i*2+2], 16)
            bytlst.append(byt)
        
        return bytlst

    def read(self):
        while True:
            next_char = chr(self.ser.read())

            if next_char in self.header:
                self.current_string == ""
                self.length = 0
            
            self.current_string += next_char
            self.length += 1

            if self.length == 2:
                self.packet_length = int(self.current_string, 16) * 2 + 2

            if self.length == self.packet_length:
                bytelist = TeleGPSSerialReader.convert_hexstring_to_bytelist(self.current_string)
                crc_check = bytelist[-2] & self.crc_mask

                if crc_check == 128:
                    self.packet_list.append(bytelist[1:-4])
                
                self.current_string == ""
                self.length = 0

            
class EggFinderSerialReader(SerialReader):
    def __init__(self, port, speed, start_byte=126, stop_byte=127):
        super().__init__(port, speed, start_byte, stop_byte)
    
    def read(self):
        pass
            
            


