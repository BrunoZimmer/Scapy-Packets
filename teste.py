# from scapy.all import *

# pcap_file = "string.pcap"

# def read_pcap(pcap_file):
#     packets = rdpcap(pcap_file)
#     for packet in packets:
#         print (packet.id)



# read_pcap(pcap_file)


# a = 12 *10*30
# print(a)


    # packets = rdpcap(pcap_file)
    # for packet in packets:
    #     print (packet.show)   
import csv

import os
    
with open("string.csv", "r") as file:
    csvreader = csv.reader(file)  # reads all csv
    for i in range(8):
        try:
            a = next(csvreader)
        except:
            print("EEND")
        else:
            print(a)
        #test if the csv file is bigger than pcap file
        # if(next(csvreader)):
        #     test1 = False


    