#!/home/kombinat/player/bin/python
import sys
from pythonosc import udp_client


UDP_IP = "127.0.0.1"
UDP_PORT = 12321

client = udp_client.SimpleUDPClient(UDP_IP, UDP_PORT)

client.send_message(f'/press/bank/{int(sys.argv[1])}/{int(sys.argv[2])}', None)

