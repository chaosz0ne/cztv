import socket

byte_message = bytes("get_time\n", " utf-8")
opened_socket = socket.socket(socket. AF_INET, socket. SOCK_DGRAM)
opened_socket. sendto(byte_message, ("127.0.0.1", 7123))
