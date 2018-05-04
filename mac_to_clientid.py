#!/usr/bin/python
'''
mac_to_clientID
  convert MAC addresses to ClientIDs
  MAC Addresses like 0050.56ab.2d59 or 005056ab2d59 - aka ascii representation of hexa decimal values.
  ClientIDs like 0063.6973.636f.2d30.3035.302e.3536.6162.2e32.6435.392d.4769.302f.30
 turn them into client IDs - 
  removing any exiting mask
  by adding text in front (cisco-)of and behind (-Gi0/0)
  expanding into two byte representation of each byte of original ascii
  inserting periods every forth char
From command line: mac_to_clientid.py <input_file> <output_file>
As a module: import mac_to_client as my - my.mac_to_client('00:50:56:ab:2d:59')

One line NEEDS to change between 2.7 & 3.1 or greater. I just can't figure an easier way today.
'''
import argparse
import binascii
import sys
import re

#Constant Values  
front_bytes = binascii.hexlify(b'cisco-')
back_bytes  = binascii.hexlify(b'-Gi0/0')
front = '00'+front_bytes.decode("utf-8")
back  = back_bytes.decode("utf-8")

def mac_to_client(macad):
  whole_str = ''
  macaddr = re.sub('[^a-fA-F0-9]', '', macad.lower())           #strip the non-hexlified chars
  if len(macaddr) !=  12:
    print ("Bad MACAddr read %s as %d bytes long" % (re.sub('[\r\n]','', macad), len(macaddr)))
    whole_str = '----.' * 6 +'--'
    return(whole_str)
  macaddr = macaddr[0:4]+'.'+ macaddr[4:8]+'.'+macaddr[8:12] 
  macaddr = binascii.hexlify(bytes(macaddr, "utf-8")) # python 3.1
# python 2.7  macaddr = binascii.hexlify(bytes(macaddr))
  big_str = front+macaddr.decode("utf-8")+back
  for str_ptr in range(0, len(big_str)+1, 4):
    whole_str = whole_str+big_str[str_ptr:str_ptr+4]
    if str_ptr+4<=len(big_str)+1:
      whole_str = whole_str+'.'
  return (re.sub('[.]$', '',whole_str))

def main():
  parser = argparse.ArgumentParser( description=( 'Convert MAC address to ClientID'))
  parser.add_argument('infile', help='enter a file name for input')
  parser.add_argument('outfile', help='enter a file name for output')
  args_parsed = parser.parse_args()
  
  with open(args_parsed.infile, 'r') as inf:
    with open(args_parsed.outfile, 'w') as outf:
      for line in inf:
        line = re.sub('[\r\n\t ]$','', line)   # remove trailing junk
        fields = line.split()                  # into 'fields'
        mac = fields[len(fields)-1]            # get the last 'field'
        clientid = mac_to_client(mac)
        outf.write(line.replace(mac,clientid)+'\n') # same as we read, with the one change


if __name__ == '__main__':
    main()

 