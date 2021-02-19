# Serial Reader

import serial
import threading
import struct
import queue
import crcmod

class SerialReader():
    def __init__(self, port, speed, header_byte):
        self.ser = serial.Serial(port, speed)
        self.packet_queue = queue.Queue(0)  # Create a FIFO queue for storing data

        self.header_byte = header_byte  # Initialize the header that will be associated with this data until it is stored server-side

        self.thread = threading.Thread(target=self.read)    # Create the listening thread
        self.thread.daemon = True
        self.thread.start()

    def read(self):
        pass

    def check_crc(self, data, crc):
        pass

    def close_port(self):
        """Close the serial port and join the thread."""

        self.ser.close()
        self.thread.join()

class DataSerialReader(SerialReader):
    def __init__(self, port, speed, header_byte, start_byte=126, stop_byte=127):
        self.buffer = []

        self.start_byte = start_byte
        self.stop_byte = stop_byte

        super().__init__(port, speed, header_byte)

    def read(self):
        """The main data processing loop for the DataSerialReader."""

        while True:
            new_byte = int(self.ser.read())

            if new_byte == self.start_byte:
                self.buffer.clear()
            elif new_byte == self.stop_byte:
                self.packet_queue.put(self.buffer[:])
            else:
                self.buffer.append(new_byte)

class TeleGPSSerialReader(SerialReader):
    def __init__(self, port, speed, header_byte):
        self.current_string = ""    # String to log current incoming stuff
        self.header = ["T", "E", "L", "E", "M"] # List to isolate the header
        self.length = 0
        self.crc_mask = 2 ** 7  # Mask for the CRC bit
        self.packet_length = 64

        super().__init__(port, speed)

    @staticmethod
    def convert_hexstring_to_bytelist(hexstr):
        """
        Converts a hexstring to a list of integers between 0 and 255.

        Parameters:
        hexstr (str): Even length string containing characters from 0 to F

        Returns:
        list: List of ints with values from 0 to 255
        """

        bytlst = []
        for i in range(int(len(hexstr) / 2)):
            byt = int(hexstr[i*2:i*2+2], 16)
            bytlst.append(byt)

        return bytlst

    def read(self):
        """The main data processing loop for the TeleGPSSerialReader."""

        while True:
            next_char = chr(self.ser.read())    # Read the next character from serial

            if next_char in self.header:    # Don't worry about the character if its in the header
                self.current_string == ""
                self.length = 0

            self.current_string += next_char    # Add the next character onto the string
            self.length += 1

            if self.length == 2:
                self.packet_length = int(self.current_string, 16) * 2 + 2

            if self.length == self.packet_length:
                bytelist = TeleGPSSerialReader.convert_hexstring_to_bytelist(self.current_string)
                crc_check = bytelist[-2] & self.crc_mask

                if crc_check == 128:
                    self.packet_queue.put(bytelist[1:-4])

                self.current_string == ""
                self.length = 0


class EggFinderSerialReader(SerialReader):
    def __init__(self, port, speed, header_byte):
        self.current_string = ""
        super().__init__(port, speed, header_byte)

    @staticmethod
    def _convert_float_to_bytelist(self, flo):
        """
        Converts a float to a list of integers between 0 and 255.

        Parameters:
        flo (float): Floating-point number to convert

        Returns:
        list: List of numbers between 0 and 255 equivalent to the inputted float
        """

        ba = bytearray(struct.pack("f", flo))
        return [int("%02x" % b, 16) for b in ba]

    def read(self):
        """The main data processing loop for the EggFinderSerialReader."""
        while True:
            next_char = chr(self.ser.read())

            if next_char == '$' and self.current_string[0] == '$':  # If the next packet is about to start, process the current packet
                data = self.current_string.split(',')

                if data[0] == "$GPGGA":
                    pass # process positional data
                elif data[0] == "$GPGSA":
                    pass # process accuracy data
                elif data[0] == "$GPGSV":
                    pass # process satellite data

                self.current_string = ""

            self.current_string += next_char


class VideoSerialReader(SerialReader):
    def __init__(self, port, speed, header_byte):
        self.current_list = []
        self.previous_list = []
        self.length = 0

        super().__init__(self, port, speed, header_byte)

    def read(self):
        """The main processing loop for the VideoSerialReader."""
        while True:
            current_byte = int(self.ser.read())

            if current_byte == 127 and len(self.current_list) >= self.length:
                self.previous_list = self.current_list[:]
                self.current_list = []

                if len(self.previous_list) == self.length:
                    # Compute crc

                    self.packet_queue.append(np.array([np.array([i]) for i in self.previous_list[5:-4]]))

                length = self.ser.read(size=4)
                self.length = struct.unpack(">I", length)

                self.current_list.append(current_byte)
                self.current_list += list(length)

            #self.current_list.append(current_byte)
            #self.current_list.append(self.ser.read())
