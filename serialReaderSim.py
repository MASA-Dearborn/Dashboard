
import time #imports time module for handling time-related functions
import serial  #imports pyserial module for handling serial communication
import random #imports random module for pseudo-random number generation
#import struct #imports struct module

def main():

    random.seed() #create a random seed using the current time system

    port = input("What is the serial port?:") #ask the user for a serial port
    #to use
    baud = input("What is the baud?:") #ask the user for the baud rate to use

    ser = serial.Serial(port, int(baud), timeout=1) #create a serial port of the
    #user's selection and a timeout of 1 second

    while True: #infinite loop
        loop(ser) #runs the loop function for the serial port
        time.sleep(0.1) #wait for 0.1 seconds

def loop(serName):
    #the packets to be sent infinitely in a loop, randomized using a switch statement

    n = random.randint(0,3) #create a random number between 0 and 3

    if n==0: #print the first packet
        serName.write(b'TELEM 225310143e06080414072408200927102112131b1e1e24000000c0572d23e94a5f280eb8\r\n')
        #this packet has an incorrect CRC value

    elif n==1: #print the second packet
        serName.write(b'TELEM 225310611005f7da007fe73d193ec83bce15010915321c1a0b170103004e002f007e8915\r\n')
        #this packet is correct, it is a GPS location packet

    elif n==2: #print the third packet
        serName.write(b'TELEM 225310c510042501000117e85d0923c0074b45384e494a0000312e382e370000007e85b4\r\n')
        #this packet is correct, it is a configuration data packet

    else: #print the last packet
        serName.write(b'TELEM 225310291106080421072108230921101512151b1e1e1200000000000000002f007e858e\r\n')
        #this packet is correct, it is a GPS satellite data packet


if __name__ == "__main__":
    main()
