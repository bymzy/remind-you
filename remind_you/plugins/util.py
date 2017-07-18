

# -*- coding: utf-8 -*-

import struct
import socket

def pack_int(val):
    return struct.pack('!I', val)

def pack_str(string):
    return pack_int(len(string)) + string

def unpack_int(data):
    val, = struct.unpack('!I', data)
    return val

def unpack_str(data):
    length = unpack_int(data[0:4])
    string = data[4: 4 + length]
    return string

def recv_len(sock, length):
    toRecv = length
    data = ''
    while toRecv > 0:
        temp = sock.recv(toRecv)
        if len(temp) == 0:
            break
        toRecv -= len(temp)
        data += temp
    return data

def send_data(sock, data):
    sock.sendall(data)

def connect_ip_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        return s
    except Exception, e:
        return None

