from socket import *
import socket
import os
import sys
import struct
import time
import select
import binascii
from functools import reduce
import argparse


ICMP_ECHO_REQUEST = 8
TRIES = 3

def make_checksum(header):
    size = len(header)
    if (size % 2) == 1:
        header += b'\x00'
        size +=1
        
    size = size //2
    header = struct.unpack('!' + str(size) + 'H', header)
    sum = reduce(lambda x, y: x+y, header)
    chksum = (sum >> 16) + (sum & 0xffff)
    chksum += chksum >> 16
    chksum = (chksum ^ 0xffff)
    
    left = (chksum << 8) & 0xff00
    right = chksum >> 8
    chksum = left + right

    return chksum

def icmp():
    global myID, data
    myChecksum = 0
    myID = 11

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    data = "AAAA".encode()
    myChecksum = make_checksum(header + data)    
   
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    packet = header + data
    return packet

def ip_header(src_ip_addr, dst_ip_addr, ttl):
    global ip_VHL, ip_ttl, ip_proto, ip_dst
    ip_ver = 4
    ip_hl = 5
    ip_tol = 0 
    ip_tos = 0
    ip_idf = 0 
    ip_rsv = 0
    ip_dtf = 0
    ip_mrf = 0
    ip_offset = 0
    ip_ttl = ttl
    ip_proto = socket.IPPROTO_ICMP
    ip_checksum = 0
    ip_src = socket.inet_aton(src_ip_addr)
    ip_dst = socket.inet_aton(dst_ip_addr)
    ip_VHL = (ip_ver << 4 ) + ip_hl
    ip_Flag = (ip_rsv << 7) + (ip_dtf << 6) + (ip_mrf << 5) + ip_offset
    header = struct.pack('!BBHHHBBH4s4s', ip_VHL, ip_tos, ip_tol, ip_idf, ip_Flag, ip_ttl, ip_proto, ip_checksum, ip_src, ip_dst)
    
    return header 

def traceroute(hostname, protocol, MAX_HOPS):
    dst_ip_addr = socket.gethostbyname(hostname)
    
    src_ip_addr = '0.0.0.0'
    result = ''

    print('traceroute to (%s), %d hops max' % (dst_ip_addr, MAX_HOPS))
    for ttl in range(1, MAX_HOPS + 1):
        print(ttl, end='\t')

        for tries in range(TRIES):
            
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, protocol)
            recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            
            ip_packet = ip_header(src_ip_addr, dst_ip_addr, ttl)
            icmp_packet = icmp()
            packet = ip_packet + icmp_packet
        
            mySocket.settimeout(TIMEOUT)
            recv_socket.settimeout(TIMEOUT)
            
            try:
                mySocket.sendto(packet, (dst_ip_addr, 0))
                t = time.time()

                recvPacket, addr = recv_socket.recvfrom(65535)
                timeReceived = time.time()

                icmpHeader = recvPacket[20:28]
                icmpData = recvPacket[28:48]
                icmpDataR = recvPacket[28:32]

                request_type, code, checksum, packetID, sequence = struct.unpack("BBHHH", icmpHeader)
                try :
                    R_HL, R_tos, R_tol, R_idf, R_Flag, R_ttl, R_proto, R_checksum, R_src, R_dst = struct.unpack("BBHHHBBH4s4s", icmpData)
                except :
                    R_data = struct.unpack("4s", icmpDataR)
                
                    

                
                takeTime = (timeReceived - t)*1000
                result = addr[0]
                
                if request_type == 11 and R_HL == ip_VHL and ttl == ip_ttl and R_proto == ip_proto and R_dst == ip_dst :
                    print("%.2fms" % (takeTime), end='\t')

                elif request_type == 3:
                    result = "Destination unreachable"

                elif request_type == 0:
                    if code == 0 and packetID == myID and R_data[0] == data:
                        print("%.2fms" % (takeTime), end = '\t')
                        if (tries == 2) :
                            print("[%s, %s]" % (socket.gethostbyaddr(addr[0])[0], addr[0]))
                            return 

                else:
                    print("other request " + str(request_type))
                    break

            except socket.timeout:
                print('*', end='\t')
                result = ''
                continue
            
            finally:
                mySocket.close()
                recv_socket.close()
                
        print(result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'traceroute')
    parser.add_argument('destination', type = str, metavar = 'dst_ip or domain_name', help = 'dst_ip or domain_name')
    #parser.add_argument('packet_size', type = str, metavar = 'packet_size', help = 'packet size')
    parser.add_argument('-t', type = float, required = False, default = 5, metavar = 'RECV_TIMEOUT', help = 'recieve timeout')
    parser.add_argument('-c', type = int, required = False, default = 30, metavar = 'MAX_HOPS', help = 'maximal hops')
    parser.add_argument('-I', action ='store_true', required = False, help = 'packet type ICMP')
    #parser.add_argument('-p', type = int, required = False, metavar = 'UDP', help = 'packet type UDP')
    #parser.add_argument('-U', action='store_true', required = False, help = 'UDP Port number. default is 53')
    
    args = parser.parse_args()
    protocol = socket.IPPROTO_RAW

    dst_hostname = args.destination
    TIMEOUT = args.t
    
    if args.I is True:
        traceroute(dst_hostname, protocol, args.c)