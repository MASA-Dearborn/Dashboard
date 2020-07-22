input = "TELEM 220710a6d40520efff0000000000000000ec010b172214e7e7e7010000000000ff4285bf"
#a line from the recorded data from the GPS testing, will be replaced by the
#serial input in the final
output = []
#the output of the code which for now is simply translating the packet into
#readable data-- so it should return everything as a CSV
#   output[0] - length of packet
#   output[1] - serial number of transmitter

if 'TELEM' == input[:5]: #checks to make sure the data starts with the correct
#start code from the TeleDongle
    if int(bin(int(input[len(input)-4:len(input)-2], 16))[9:]) == 1:
        #checks the second to last byte of the string's 7th binary digit to
        #ensure a proper CRC value (this comes from the encoding scheme of the
        #TeleGPS, see https://altusmetrum.org/AltOS/doc/telemetry.html)
        output = [input[6:8], input[10:12] + input[8:10]]
        print(output[0])
    else:
        print('error, improper CRC')
else:
    print("improper string, no start code")
