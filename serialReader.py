exe = "TELEM 220710a6d40520efff0000000000000000ec010b172214e7e7e7010000000000ff4285bf"
#a line from the recorded data from the GPS testing, will be replaced by the
#serial input in the final

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

                if output[3] == 5: #if true, the packet is a GPS location packet
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

                    #approximate altitude, latitude, longitude (output 10 throuh 12)
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
                    print('GPS Satellite packet')

                elif output[3] == 4: #if true, the packet is configuration data
                    print('Configuration data')

                else: #packet has bad packet type, discard
                    print('error, incorrect packet type')
                    return None

                return output[0:]

            else:
                print('error, improper CRC')
                return None

        else:
            print('error, wrong checksum, data lost')
            return None

    else:
        print("improper string, no start code")
        return None

if __name__ == '__main__':
    print(TeleGPStranslation(exe))
