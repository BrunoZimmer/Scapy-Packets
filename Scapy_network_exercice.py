# Although dealing with networks, our software does not see in most cases the actual packets, but only metadata, 
# such as source and destination IP addresses, UDP or TCP ports, packet-size, etc. To view the packets or to replay
#  them, a possibility is to craft the packets using a library like Scapy (see https://scapy.readthedocs.io/en/latest/).
#   That way, we can store the generated packets in a pcap file. Such file can be opened with a network protocol 
#   analysis tools (Wireshark is a very popular one, with a GUI, and tshark is its terminal-based variant). Note 
#   that usually such metadata only contains information about the IP header and above. But packets transmitted 
#   in IP networks typically contain an ethernet header below the IP header.

# Given a CSV file that contains metadata of real IP packets:
#      ---- write a function `build_pcap` that generates packets based on that data
#     saves it into a pcap file
#     returns the number of packets it generated.

# Write a test that checks the generated pcap file, by reading the pcap file and do a few checks, such as:
#     does it contain the expected number of packets ?
#     are the packets in the right order ?
#     do their properties match the content of the CSV ?

# Try to think of other positive or negative test cases that could extend the test coverage 
# (implementation is not required)


# For this exercise, we'll make the following assumptions:
#     a generated packet must contain a source and a destination IP address, a transport protocol header (TCP or UDP) with
#         source and destination ports, based on the content of the metadata,
#     the size of the packet should match what is specified in the metadata, and for that, one can append dummy bytes at 
#         the end of the packet,
#     no importance will be given to the time information of each packet in the pcap file, but the packet flow ordering 
#         from the CSV file must be kept,
#     both IPv4 and IPv6 versions should be handled,
#     use fixed values for ethernet source and destination addresses, such as "00:00:00:00:00:01", "00:00:00:00:00:02".
#     there is no constraint on how the code is structured or divided, except for the build_pcap function.

# Here is an example of CSV string:
# """id,src-ip,dst-ip,proto,sport,dport,length
# 1,10.0.0.1,20.0.0.2,6,20500,53,120"""

# And the resulting scapy structure:
# <Ether  dst=00:00:00:00:00:02 src=00:00:00:00:00:01 type=IPv4 |<IP  frag=0 proto=tcp src=10.0.0.1 dst=20.0.0.2 |
# <TCP  sport=20500 dport=domain |<Raw  load='AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' |>>>>



################################################### BEGIN ###################################################


# csv_file: path to the input csv file
# pcap_file: path to where the resulting pcap file should be stored
# returns: the number of packets that were put in the pcap file
def build_pcap(csv_file, pcap_file):
    # write code here
    return nb_packets


import csv
from scapy.all import *

# csv_file: path to the input csv file
# pcap_file: path to where the resulting pcap file should be stored
# returns: the number of packets that were put in the pcap file
csv_file = "string.csv"
pcap_file = "string.pcap"
csv_badfile = "stringBadTest.csv"
pcap_badfile = "stringBad.pcap"


def ReadCSV(csv_file):  # returns the list with all rows of the csv file
    # its better to have this function into build-pcap to reduce the memory usage
    rows = []

    with open(csv_file, "r") as file:
        csvreader = csv.reader(file)  # reads all
        header = next(csvreader)  # saves the header
        for row in csvreader:  # saves each row
            rows.append(row)

    return [header, rows]

def build_pcap(csv_file, pcap_file):
    rows = ReadCSV(csv_file)
    # packets = []
    nb_packets = 0

    for row in rows[1]:  # header      ids
        # print(row)
        #for each row separate the variables to visualization
        id = int(row[0])
        srcmac = "00:00:00:00:00:01"
        dstmac = "00:00:00:00:00:02"
        srcip = str(row[1])
        dstip = str(row[2])
        ptcl = int(row[3])
        srcport = int(row[4])
        dstport = int(row[5])
        length = int(row[6])
        nb_packets += 1

        
        #packet declaration
        pkt = (
            Ether(dst=dstmac, src=srcmac)
            / IP(src=srcip, dst=dstip, len=length, id=id, proto=ptcl)
            / UDP(sport=srcport, dport=dstport)
        )

        #adding dummy load bytes
        loadData = "A" * (length - len(pkt))
        pkt = pkt / Raw(load = loadData)

        # packets.append(pkt)
        #writing pcap file
        wrpcap(pcap_file, pkt, append=True)

    # print(packets)

    return nb_packets


def read_pcap(csv_file, pcap_file):
    packets = rdpcap(pcap_file)
    quantity = len(packets) #saves the quantity of packets in the pcap to subtrate aftr

    print(quantity)
    print(packets.show())
    #all statements starts positives and then we will prove if it's false
    test1 = True
    test2 = True
    test3 = True

        
    with open(csv_file, "r") as file:
        csvreader = csv.reader(file)  # reads all csv
        next(csvreader)  # skip the header
        for packet in packets:  
            try:#try to read the next row of csv file
                row = next(csvreader)
                if (#Condition to the test 2
                    #verify if the packet id is the same to confirm the order
                    int(packet.id) != int(row[0])
                    ):
                    test2 = False

                if (#Condition to the test 3
                    #verify all the packet's content
                    int(packet.id) != int(row[0]) or
                    str(packet[IP].src) != str(row[1]) or
                    str(packet[IP].dst) != str(row[2]) or
                    int(packet.proto) != int(row[3]) or
                    int(packet.sport)!= int(row[4]) or
                    int(packet.dport) != int(row[5]) or
                    int(packet.len)!= int(row[6])
                    ):
                    test3 = False

                #Condition to the test 1
                #each line substract the previous to see if it's equal in the end
                quantity -= 1
                print(quantity)
            except:
                break

        print(quantity)
        #test if the csv file is bigger than pcap file
        try:
            row = next(csvreader)
        except:
            test1 = True if quantity == 0 else False
        else:
            test1 = False
            
    
    print( "Does it contain the expected number of packets ?   " + str(test1))
    print("Are the packets in the right order ?   " + str(test2)) #the sequence could be right but with different quantities
    print("Do their properties match the content of the CSV ?   " + str(test3)) 


############# FULL TEST FUNCTION ##################
# read_pcap(csv_file, pcap_file)


############# WRITE FUNCTION ##################
# a = build_pcap(csv_file, pcap_file)
# print(a)




#Try to think of other positive or negative test cases that could 
# extend the test coverage (implementation is not required)

# Does ip "Ether" is mac format ?
# Does src and dst port is under the maximum number?
# Are the packet arguments in the right type(numbers, strings etc)













############  single test functions 

# def test_packets_quantity( csv_file, pcap_file):
#     packets = rdpcap(pcap_file)
#     quantity = len(packets)
#     print(quantity)

#     with open(csv_file, "r") as file:
#         csvreader = csv.reader(file)  # reads all
#         header = next(csvreader)  # saves the header
#         for row in csvreader:  # saves each row
#             quantity -= 1
#             print(quantity)

#     return True if quantity == 0 else False
    
# def test_right_order( csv_file, pcap_file):
#     packets = rdpcap(pcap_file)
        
#     with open(csv_file, "r") as file:
#         csvreader = csv.reader(file)  # reads all
#         header = next(csvreader)  # saves the header
#         for packet in packets:
#             row = next(csvreader)
#             if (int(packet.id) != int(row[0])):
#                 return False

#     return True

# def test_right_content( csv_file, pcap_file):
#     packets = rdpcap(pcap_file)
        
#     with open(csv_file, "r") as file:
#         csvreader = csv.reader(file)  # reads all
#         header = next(csvreader)  # saves the header
#         for packet in packets:
#             row = next(csvreader)

#             if (
#                 int(packet.id) != int(row[0]) or
#                 str(packet[IP].src) != str(row[1]) or
#                 str(packet[IP].dst) != str(row[2]) or
#                 int(packet.proto) != int(row[3]) or
#                 int(packet.sport)!= int(row[4]) or
#                 int(packet.dport) != int(row[5]) or
#                 int(packet.len)!= int(row[6])
#                 ):
#                 return False

#     return True