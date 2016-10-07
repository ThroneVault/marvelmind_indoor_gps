#!/usr/bin/env python

# Adapted from code written by Boris Zinin (b.zinin@gmail.com)
# To prevent errors when installing crcmod module used in this script, use the following sequence of commands:
#   sudo apt-get install python-pip
#   sudo apt-get update
#   sudo apt-get install python-dev
#   sudo pip install crcmod

import rospy
import sys
from time import sleep
import serial
import struct
import time
from numpy import pi
from geometry_msgs.msg import Vector3
#import crcmod
import traceback

def indoor_gps_init(serial_device, baudrate):
    # open port
    try:
        ser = serial.Serial(serial_device, baudrate, timeout=3 )
    except serial.serialutil.SerialException:
        print 'Can not open serial port(%s)'%(serial_device)
        traceback.print_exc()
        return None
 
    # return serial port
    ser.flushInput()
    return ser

def indoor_gps_data_acq():
    # start node
    rospy.init_node('indoor_gps', anonymous=True)
    pub 	= rospy.Publisher('indoor_gps', Vector3, queue_size = 10)
    
    # open port
    port        = rospy.get_param("indoor_gps/port")
    baud        = rospy.get_param("indoor_gps/baud")
    ser 	    = indoor_gps_init(port, baud)

    pktSize = 23
    meta_data_size = 5;
    
    while not rospy.is_shutdown():
        ser = serial.Serial(port, baud, timeout=3 )
        ser.flushInput()
        len_buf = pktSize*3 - 1
        buf = ser.read(len_buf)
        buf = ''

        while buf is not None:
            buf += ser.read(len_buf)
            pktHdrOffset = buf.find('\xff\x47\x01\x00')
   
            while pktHdrOffset == -1:
                ser.flushInput()
                buf = ser.read(len_buf)
                pktHdrOffset = buf.find('\xff\x47\x01\x00')

            if len_buf - pktHdrOffset - meta_data_size >= 18:
                usnTimestamp, usnX, usnY, usnCRC16 = struct.unpack_from ( '<LhhxxxxxxxxH', buf, pktHdrOffset + meta_data_size )
                pub.publish( Vector3( usnX, usnY, 0) )
     
            len_tail = len( buf ) - (pktHdrOffset + pktSize)
            len_buf = pktSize - len_tail
            if len_buf == 0:
                len_buf = pktSize
                buf = ''
            elif len_buf < 0:
                ser.flushInput()
                len_buf = pktSize*2 - 1
                buf = ''
            else:
                buf = buf[ pktHdrOffset + pktSize : ]

    ser.close()

if __name__ == '__main__':
    try:
        indoor_gps_data_acq()
    except rospy.ROSInterruptException:
        pass
