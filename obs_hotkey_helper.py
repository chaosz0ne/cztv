import os
import json
import socket
import subprocess

import obswebsocket, obswebsocket.requests

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 7127
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

client = obswebsocket.obsws("localhost", 4444, "password")
client.connect()
res = client.call(obswebsocket.requests.SetSourceFilterVisibility("FS_vorhang", "vorhang_li_auf", True))
print(res)



def ssfv(cmd):
	params = cmd[len("SetSourceFilterVisibility")+1:]
	print(params)
	item, filt, vis = params.split('.')
	if vis.lower() in ('0', 'false', 'f', 'n', 'no', 'nein', 'nö'):
		vis = False
	else:
		vis = True
	res = client.call(obswebsocket.requests.SetSourceFilterVisibility(item, filt, vis))



while True:
    data, addr = serverSock.recvfrom(1024)
    commands = data.decode("utf8").splitlines()
    for cmd in commands:
        if cmd.startswith('SetSourceFilterVisibility'):
        	ssfv(cmd)


client.disconnect()
