import os
import socket
import argparse
import struct

ETH_P_ALL = 0x0003
ETH_H_SIZE = 14
cnt = 1


def make_ethernet_header(raw_data):
   global cnt
   ether = struct.unpack('!6B6BH', raw_data)
   if ether[12] == 0x0800 : # Ipv4
      print("\n[%d] IP_PACKET-------------------------------------------\n" % cnt)
      print('Ethernet Header')
      print("[dst] %02x:%02x:%02x:%02x:%02x:%02x" % ether[:6])
      print("[src] %02x:%02x:%02x:%02x:%02x:%02x" % ether[6:12])
      print("[ether_type] %d" % ether[12])
      cnt += 1
      return True
   else :
      return False

def make_ip_header(raw_data):
   if len(raw_data) == 1 :
      ip = struct.unpack('!B', raw_data) # 1Byte
      version = ip[0] >> 4 # version 4bit
      header_length = ip[0] & 0x0f # header length 4bit
      print("[version] %d" % version)
      print("[header_length] %d" % header_length)
      return header_length # header length
   else :
      ip = struct.unpack('!BHHHBBH4B4B', raw_data)
      flag = ip[3] >> 13 # flag 3bit
      offset = ip[3] & 0x1fff # offset 13bit
      print("[tos] %d" % ip[0])
      print("[total_length] %d" % ip[1])
      print("[id] %d" % ip[2])
      print("[flag] %d" % flag)
      print("[offset] %d" % offset)
      print("[ttl] %d" % ip[4])
      print("[protocol] %d" % ip[5])
      print("[checksum] %d" % ip[6])
      print("[src] %d.%d.%d.%d" % ip[7:11])
      print("[des] %d.%d.%d.%d" % ip[11:15])

def dumpcode(buf):
   print("\nRaw Data")
   print("%7s"% "offset ", end='')

   for i in range(0, 16):
      print("%02x " % i, end='')

      if not (i%16-7):
         print("- ", end='')

   print("")

   for i in range(0, len(buf)):
      if not i%16:
         print("0x%04x" % i, end= ' ')

      print("%02x" % buf[i], end= ' ')

      if not (i % 16 - 7):
         print("- ", end='')

      if not (i % 16 - 15):
         print(" ")

   print("")   

def sniffing(nic):
   if os.name == 'nt':
      address_family = socket.AF_INET
      protocol_type = socket.IPPROTO_IP
   else:
      address_family = socket.AF_PACKET
      protocol_type = socket.ntohs(ETH_P_ALL)
   
   with socket.socket(address_family, socket.SOCK_RAW, protocol_type) as sniffe_sock:
      sniffe_sock.bind((nic, 0))

      if os.name == 'nt':
         sniffe_sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL,1)
         sniffe_sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

      data, _ = sniffe_sock.recvfrom(65535)
        
      ethernet_header = make_ethernet_header(data[:ETH_H_SIZE])
      if ethernet_header == True :
         print('\nIp Header')
         ip_1B = make_ip_header(data[ETH_H_SIZE:ETH_H_SIZE+1])
  
         IP_H_SIZE = ETH_H_SIZE + ip_1B * 4 # Ip Header Size

         make_ip_header(data[ETH_H_SIZE+1:IP_H_SIZE])

         dumpcode(data)
         print("--------------------------------------------------------")

      if os.name == 'nt':
         sniffe_sock.ioct1(socket.SIO_RCVALL, socket.RCVALL_OFF)

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description = 'This is a simple packet sniffer')
   parser.add_argument('-i', type = str, required = True, metavar = 'NIC name', help = 'NIC name')
   args = parser.parse_args()
   while(True) :
      sniffing(args.i)
