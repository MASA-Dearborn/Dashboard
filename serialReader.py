exe = "TELEM 220710a6d40520efff0000000000000000ec010b172214e7e7e7010000000000ff4285bf"
#a line from the recorded data from the GPS testing, will be replaced by the
#serial input in the final


def TeleGPStranslation(input):
    #takes an input of raw TeleGPS data and returns a CSV of readable data
    output = []
    #the readable data which will be returned if possible
    #   output[0] - length of packet
    #   output[1] - serial number of transmitter
    #   output[2] - device time in 100ths of a second
    #   output[3] - packet type

    if 'TELEM' == input[:5]: #checks to make sure the data starts with the correct
    #start code from the TeleDongle
        if int(bin(int(input[len(input)-4:len(input)-2], 16))[9:]) == 1:
            #checks the second to last byte of the string's 7th binary digit to
            #ensure a proper CRC value (this comes from the encoding scheme of the
            #TeleGPS, see https://altusmetrum.org/AltOS/doc/telemetry.html)

            output = [int(input[6:8], 16), int(input[10:12] + input[8:10], 16),
            int(input[14:16] + input[12:14],16), int(input[16:18], 16)]
            #enters the first bit of packet data which is in all packets

            return output[0:]
        else:
            print('error, improper CRC')
    else:
        print("improper string, no start code")

if __name__ == '__main__':
    print(TeleGPStranslation(exe))
