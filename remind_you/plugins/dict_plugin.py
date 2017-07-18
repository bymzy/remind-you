# -*- coding: utf-8 -*-

import time
import os
import requests
import socket
import struct
from util import pack_str, recv_len, unpack_int, unpack_str, pack_int

URL = 'www.baidu.com'

def generate_request(_word, _trans):
    trans = pack_int(_trans)
    word = pack_str(_word)
    totalLen = 4 + len(trans) + len(word)
    return pack_int(totalLen) + trans + word

def run(args):
    print 'my pid is: %u , %s ' % (os.getpid(), args)
    port = args.get('port')
    ip = args.get('ip')
    dbPath = args.get('db')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, port))
    sock.listen(5)

    while True:
        cl, addr = sock.accept()
        tmp = recv_len(cl, 4)
        wordLen = unpack_int(tmp)
        data = recv_len(cl, wordLen)
        trans = unpack_int(data[0:4])
        word = unpack_str(data[4:])
        print 'receive word %s , need trans %d: ' % (word, trans)
        cl.close()

