import threading #imports multithreading for the queue and saving data functions

def TeleGPStranslation(input):
    # the main function of the program, turns the TeleGPS strings into comma
    #seperated lists that expand out all the data
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

    def signedConversion(number):
        #converts the unsigned 32 bit HEX into signed 2's compliment for the coordinates
        if number >= 2147483648:
            return int(f'{number:08b}'[1:], 2) - 2147483648
        else:
            return number

    #takes an input of raw TeleGPS data and returns an array of readable data
    output = []

    if input == []: #if the input is empty, don't bother trying to decode it
        #print('error, no data inputted')
        #return None
        output = ['error, no data inputted']
        return output[0:]


    if 'TELEM' == input[:5]: #checks to make sure the data starts with the correct
    #start code from the TeleDongle

        if checkSum(input) == True: #checks the checksum value to ensure no lost
        # data

            if int(f'{int(input[len(input)-4:len(input)-2], 16):08b}'[:1]) == 1:
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

                    #approximate altitude (output 10)
                    output.append(int(input[22:24] + input[20:22], 16))

                    #latitude (output 11)
                    output.append(signedConversion(int(input[30:32] + input[28:30] + input[26:28] + input[24:26], 16)) * 1/10000000)

                    #longitude (output 12)
                    output.append(signedConversion(int(input[38:40] + input[36:38] + input[34:36] + input[32:34], 16)) * 1/10000000)

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
                        output.append(int(input[20+4*transIter:22+4*transIter], 16)) #space vehicle identifier
                        output.append(int(input[22+4*transIter:24+4*transIter], 16)) #C/N1 signal quality indicator
                        transIter += 1

                else: #packet has bad packet type, discard
                    #print('error, incorrect packet type')
                    #return None

                    output = ['error, incorrect packet type']

                return output[0:]

            else: #packet does not have a valid CRC value
                #print('error, improper CRC')
                #return None
                output = ['error, improper CRC']
                return output[0:]

        else: #packet does not have the correct checksum so data has been lost
            #print('error, wrong checksum, data lost')
            #return None
            output = ['error, wrong checksum, data lost']
            return output[0:]

    else: #packet lacks the TELEM start string
        #print('error, improper string, no start code')
        #return None
        output = ['error, improper string, no start code']
        return output[0:]

def CSVsave(fileName, data):
    #takes the translated data and saves it to a CSV file with the file name given

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

def queueData(processingLine, translatedQueueName, translationFunction):
    #queue's data from the serial line to allow for fast incoming data, designed for
    #multithreading use

    if translationFunction(processingLine[:1]) != None: #only puts in data if there's
    #data
        translatedQueueName.append(translationFunction(processingLine[:len(processingLine)-1]))

if __name__ == '__main__':

    fileToProcess = input('what is the text file being processed called?:')
    #ask the user for the file being processed

    fileToSaveTo = input('what is the file being saved to called?:')
    #ask the user for the file being saved to

    rawFile = open(fileToProcess + '.txt', 'r') #open the file being processed

    translatedQueue = [] #creates a queue for the translated data

    currentLine = rawFile.readline() #get a line to processed

    while currentLine != '':
        #loop through all the lines of the file

        queueThread = threading.Thread(target=queueData, args=(currentLine, translatedQueue,
        TeleGPStranslation)) #the thread which fills the translated queue with translated data

        #run the thread for the translation
        queueThread.start()
        queueThread.join()

        if len(translatedQueue) != 0:
            #if there is data in the translatedQueue, save it to a csv file
            csvThread = threading.Thread(target=CSVsave, args=(fileToSaveTo, translatedQueue.pop(0)))

            #run the thread for the saving to a file
            csvThread.start()
            csvThread.join()


        currentLine = rawFile.readline() #get the next line to processed


    rawFile.close() #close the file being read
