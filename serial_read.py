#!/usr/bin/env python
import roslib #roslib.load_manifest('numpy_tutorials') #not sure why I need this
import rospy
from std_msgs.msg import String
import serial
#from crccheck.crc import Crc32Mpeg2
import time

custom_crc_table = {}

def int_to_bytes(i):
    return [(i >> 24) & 0xFF, (i >> 16) & 0xFF, (i >> 8) & 0xFF, i & 0xFF]

def generate_crc32_table(_poly):

    global custom_crc_table

    for i in range(256):
        c = i << 24

        for j in range(8):
            c = (c << 1) ^ _poly if (c & 0x80000000) else c << 1

        custom_crc_table[i] = c & 0xffffffff

def custom_crc32(buf):

    global custom_crc_table
    crc = 0xffffffff

    for integer in buf:
        b = int_to_bytes(integer)

        for byte in b:
            crc = ((crc << 8) & 0xffffffff) ^ custom_crc_table[(
                crc >> 24) ^ byte]

    return crc

# serial config
ser = serial.Serial('/dev/ttyUSB0', 115200)
# string = 'abcdef'
# data = bytearray.fromhex(string)
# crc = str(hex(Crc32Mpeg2.calc(data)))
# print(crc)
poly = 0x04C11DB7
generate_crc32_table(poly)
tx = [1]
tx_encoded = str.encode(str(tx[0]))
#print(custom_crc32(tx))

def node():
    rospy.init_node('serial_port')
    if ser.isOpen():
        print("Serial port initialized")
    else:
        print("Serial port not open")
        quit()
    while not rospy.is_shutdown():
        ser.write(tx_encoded)
        print("Write: " + str(tx_encoded))
        time.sleep(1)
        rev_raw = ser.readline()
        rev = rev_raw.decode()
        print("Get: ", rev, type(rev), type(tx_encoded))

if __name__ == '__main__':
    try:
        node()
    except rospy.ROSInterruptException:
        pass





# try:
#     while True:
#         while ser.in_waiting:
#             data_raw = ser.readline()
#             data = data_raw.decode()
#             print(data)

# except KeyboardInterrupt:
#     ser.close()
#     print("bye")

# def talker():
#  while not rospy.is_shutdown():
#    data= ser.read(2) # I have "hi" coming from the arduino as a test run over the serial port
#    rospy.loginfo(data)
#    pub.publish(String(data))
#    rospy.sleep(1.0)


