
import time #imports time module for handling time-related functions
import serial  #imports pyserial module for handling serial communication

import struct #

def main():

    port = input("What is the serial port?:") #ask the user for a serial port
    #to use
    baud = input("What is the baud?:") #ask the user for the baud rate to use

    ser = serial.Serial(port, int(baud), timeout=1) #create a serial port of the
    #user's selection and a timeout of 1 second

    while True: #infinite loop
        loop(ser) #runs the loop function for the serial port
        time.sleep(0.1) #wait for 0.1 seconds

def loop(serName):
    #the packets to be sent infinitely in a loop

    serName.write(b'TELEM 225310143e06080414072408200927102112131b1e1e24000000c0572d23e94a5f280eb8\n')
    #this packet has an incorrect CRC value

    serName.write(b'TELEM 225310611005f7da007fe73d193ec83bce15010915321c1a0b170103004e002f007e8915\n')
    #this packet is correct, it is a GPS location packet

    serName.write(b'TELEM 225310c510042501000117e85d0923c0074b45384e494a0000312e382e370000007e85b4\n')
    #this packet is correct, it is a configuration data packet

    serName.write(b'TELEM 225310291106080421072108230921101512151b1e1e1200000000000000002f007e858e\n')
    #this packet is correct, it is a GPS satellite data packet

if __name__ == "__main__":
    main()
