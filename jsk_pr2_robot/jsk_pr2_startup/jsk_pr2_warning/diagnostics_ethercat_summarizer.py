#!/usr/bin/env python

import rospy

from diagnostic_msgs.msg import DiagnosticArray


def callback(data):
    flag = False
    dp_value = None
    rlp_value = None
    for e in data.status:
        #EtherCAT Device
        for v in e.values:
            if v.key =='Drops':
                flag = True
                print(e.name + " Drops: {}".format(v.value))
        #EtherCAT Master
        if e.name == 'EtherCAT Master':
            for v in e.values:
                if v.key =='Dropped Packets':
                    print(e.name + " Dropped Packets: {}".format(v.value))
                    dp_value = int(v.value)
                if v.key =='RX Late Packet':
                    print(e.name + " RX Late Packet: {}".format(v.value))
                    rlp_value = int(v.value)
                if dp_value != None and rlp_value != None:
                    print("EtherCAT Master CRC Errors (Dropped Packets - RX Late Packet): {}".format(dp_value - rlp_value))
                    dp_value = None
                    rlp_value = None

    if flag:
        print("--------------------------------------------")


def listener():
    rospy.init_node('diagnostics_ethercat_summarizer', anonymous=True)
    rospy.Subscriber('/diagnostics', DiagnosticArray, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
