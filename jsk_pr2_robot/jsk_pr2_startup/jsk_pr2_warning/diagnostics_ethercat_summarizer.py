#!/usr/bin/env python

import rospy

from diagnostic_msgs.msg import DiagnosticArray


def callback(data):
    flag = False
    dp_value = None
    rlp_value = None
    thre_val = 0
    s_name_list = []
    key_list = []
    value_list = []
    for s in data.status:
        #EtherCAT Device
        for v in s.values:
            if v.key =='Drops':
                flag = True
                print(s.name + " Drops: {}".format(v.value))
                if int(v.value) > thre_val:
                    s_name_list.append(s.name)
                    value_list.append(v.value)
                    key_list.append(v.key)

        #EtherCAT Master
        if s.name == 'EtherCAT Master':
            for v in s.values:
                if v.key =='Dropped Packets':
                    print(s.name + " Dropped Packets: {}".format(v.value))
                    dp_value = int(v.value)
                if v.key =='RX Late Packet':
                    print(s.name + " RX Late Packet: {}".format(v.value))
                    rlp_value = int(v.value)
                if dp_value != None and rlp_value != None:
                    print("EtherCAT Master CRC Errors (Dropped Packets - RX Late Packet): {}".format(dp_value - rlp_value))
                    dp_value = None
                    rlp_value = None

    if flag:
        if len(s_name_list) > 0:
            print("[Devices with errors]")
            for s_name, key, value in zip(s_name_list, key_list, value_list):
                print(s_name + " " + key + ": {}".format(value))
        print("--------------------------------------------")


def listener():
    rospy.init_node('diagnostics_ethercat_summarizer', anonymous=True)
    rospy.Subscriber('/diagnostics', DiagnosticArray, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
