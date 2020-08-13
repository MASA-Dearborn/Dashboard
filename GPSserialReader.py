import serial #imports pyserial for use in the program

serialOne = serial.Serial('COM3', 9600, timeout=1) #opens up a serial line at COM3
# with a timeout of 1 second and a baud of 9600

def checkSum(input):
    #takes an input of raw teleGPS data and calculates what the value of the
    #checksum should be given the data, then returns whether or not the
    #checksum matches
    checkedData = input[8:len(input)-2] #data the checksum checks
    i = 0 #iteration number
    sum = 0 #sum of the bytes

    while i < len(checkedData): #sums the hex bytes
        sum = sum + int(checkedData[i:i+2], 16)
        i = i + 2

    if (sum + 90) % 256 == int(input[len(input)-2:], 16): #checks the checksum's
    #value given the formula from the TeleGPS modulation scheme
        return True
    else:
        return False

def TeleGPStranslation(input):
    #takes an input of raw TeleGPS data and returns an array of readable data
    output = []

    if 'TELEM' == input[:5]: #checks to make sure the data starts with the correct
    #start code from the TeleDongle

        if checkSum(input) == True: #checks the checksum value to ensure no lost
        # data

            if int(f'{int(input[len(input)-4:len(input)-2], 16):08b}'[7:]) == 1:
                #checks the second to last byte of the string's 7th binary digit to
                #ensure a proper CRC value (this comes from the encoding scheme of the
                #TeleGPS, see https://altusmetrum.org/AltOS/doc/telemetry.html)

                output = [int(input[6:8], 16), int(input[10:12] + input[8:10], 16),
                int(input[14:16] + input[12:14],16), int(input[16:18], 16),
                int(input[len(input)-6:len(input)-4], 16)/2 - 74]
                #enters the first bit of packet data which is in all packets
                #   output[0] - length of packet
                #   output[1] - serial number of transmitter
                #   output[2] - device time in 100ths of a second
                #   output[3] - packet type
                #   output[4] - recieved signal stregth indicator

                if output[3] == 4: #if true, the packet is configuration data
                    #   output[5] - device type
                    #   output[6] - flight number
                    #   output[7:8] - config major version, config minor version
                    #   output[9] - maximum flight log size in kB
                    #   output[10] - HAM callsign
                    #   output[11] - software version idenifier

                    #device type (37 from testing), flight number (output 5 and 6)
                    output.append(int(input[18:20], 16))
                    output.append(int(input[22:24] + input[20:22], 16))

                    #config major version, config minor version (output 7 and 8)
                    output.append(int(input[24:26], 16))
                    output.append(int(input[26:28], 16))

                    #maximum flight log size in kB (output 9)
                    output.append(int(input[38:40] + input[36:38], 16))

                    #HAM callsign and software version identifier (output 10 and 11)
                    output.append(str(bytes.fromhex(input[40:56]).decode('utf-8')).replace("\x00", ""))
                    output.append(str(bytes.fromhex(input[56:72]).decode('utf-8')).replace("\x00", ""))

                elif output[3] == 5: #if true, the packet is a GPS location packet
                    #   output[5:9] - GPS Flags
                    #   output[10] - approx. altitutde in m
                    #   output[11] - latitude
                    #   output[12] - longitude
                    #   output[13:19] - date and time
                    #   output[20:22] - pdop, hdop, vdop (dilutions of precision)
                    #   output[23] - GPS Mode
                    #   output[24] - Ground Speed in cm/s
                    #   output[25] - Climb Rate in cm/s
                    #   output[26] - Course/2

                    #GPS Flags (output 5 through 9)
                    output.append(int(f'{int(input[18:20],16):08b}'[:4], 2))
                    output.append(int(f'{int(input[18:20],16):08b}'[4:5]))
                    output.append(int(f'{int(input[18:20],16):08b}'[5:6]))
                    output.append(int(f'{int(input[18:20],16):08b}'[6:7]))
                    output.append(int(f'{int(input[18:20],16):08b}'[7:]))

                    #approximate altitude, latitude, longitude (output 10 through 12)
                    output.append(int(input[22:24] + input[20:22], 16))
                    output.append(input[24:32])
                    output.append(input[32:40])

                    #date and time (output 13 through 19)
                    output.append(int(input[40:42], 16))
                    output.append(int(input[42:44], 16))
                    output.append(int(input[44:46], 16))
                    output.append(int(input[46:48], 16))
                    output.append(int(input[48:50], 16))
                    output.append(int(input[50:52], 16))

                    #pdop, hdop, vdop (outputs 20 through 22)
                    output.append(int(input[52:54], 16))
                    output.append(int(input[54:56], 16))
                    output.append(int(input[56:58], 16))

                    #GPS Mode, ground speed, climb rate, course (output 23 through 26)
                    output.append(int(input[58:60], 16))
                    output.append(int(input[62:64] + input[60:62], 16))
                    output.append(int(input[66:68] + input[64:66], 16))
                    output.append(int(input[68:70], 16))

                elif output[3] == 6: #if true, the packet is a GPS Satellite packet
                    #   output[5] - number of reported satellite info
                    #   output[6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28] - space vehicle identifier
                    #   output[7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29] - C/N1 signal quality indicator

                    #number of reported satellite info (output 5)
                    output.append(int(input[18:20], 16))

                    #space vehicle identifiers and C/N1 signal quality inidcators (output[6:29])
                    transIter = 0 #creates an iteration value for the satellite data loop
                    while transIter < 12:
                        output.append(int(input[20+2*transIter:22+2*transIter], 16)) #space vehicle identifier
                        output.append(int(input[22+2*transIter:24+2*transIter], 16)) #C/N1 signal quality indicator
                        transIter += 1

                else: #packet has bad packet type, discard
                    print('error, incorrect packet type')
                    return None

                return output[0:]

            else: #packet does not have a valid CRC value
                print('error, improper CRC')
                return None

        else: #packet does not have the correct checksum so data has been lost
            print('error, wrong checksum, data lost')
            return None

    else: #packet lacks the TELEM start string
        print("improper string, no start code")
        return None

def testTranslation(input):
    #translates the test code from the arduino

    output = []

    transIter = 1 #creates an iteration to break up the numbers
    while transIter < 23:
        output.append(input[transIter:transIter+2])
        transIter += 2

    return output[0:]

def CSVsave(fileName, data):
    #takes the data (given in a python array) and saves it to a CSV file with the
    #file name given

    file = open(fileName + ".csv", "a") #open and write to a file the data

    CSVIter = 1 #creates an iteration value for the data

    while CSVIter <= len(data): #iterate through the data and add it to a line of the
    #CSV file
        file.write(str(data[CSVIter - 1]))
        if CSVIter < len(data): #makes sure that the last data is not followed by a ','
            file.write(",")
        CSVIter += 1

    file.write("\n") #add a new line to the CSV file
    file.close() #close the file

if __name__ == '__main__': #the main loop -> cancel the script with ctrl + C

    print(serialOne.readline()) #primes the readline to work-- for some reason
    #the readline always starts with a junk line but this simply prints that line

    queue = [] #creates a test queue for the incoming data

    serialIter = 0 #creates a loop value for the serial data
    while serialIter < 15:

        #translates the data and addes it to the queue
        recieved = str(serialOne.readline()).replace("\\r\\n", "").replace("b", "")
        queue.append(testTranslation(recieved))

        #saves the data to the test.csv file
        CSVsave("test", queue.pop(0))
        
        serialIter += 1
