
import time
import struct

from masalib import PacketSender


def main():
    sender = PacketSender("127.0.0.1", 9991)

    counter = 0

    while True:
        counter += 1
        counter %= 250

        sender.send_spoof_packet([0, 0, 0, counter, 0, 0, 0, 0], "10001001", header=0)
        sender.send_spoof_packet([0, 0, 0, counter, 0, 0, 0, 0], "10001001", header=1)
        time.sleep(0.1)

if __name__ == "__main__":
    main()