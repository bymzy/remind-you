# -*- coding: utf-8 -*-

import time
import os
import requests
import socket
import struct
import sys

from remind_you.plugins.log import Log
from remind_you.plugins.util import pack_str, recv_len, unpack_int, unpack_str, pack_int, get_posix_time
from remind_you.plugins.db import DB

log = None

def init_log(logFile):
    global log
    log =  Log(logFile)

def generate_request(_word, _trans):
    trans = pack_int(_trans)
    word = pack_str(_word)
    totalLen = 4 + len(trans) + len(word)
    return pack_int(totalLen) + trans + word

def recv_request(cl):
    tmp = recv_len(cl, 4)
    wordLen = unpack_int(tmp)
    data = recv_len(cl, wordLen)
    trans = unpack_int(data[0:4])
    word = unpack_str(data[4:])
    return word, trans

def is_word_exist(db, word):
    try:
        cur = db.execute("select * from dict_table where word = '%s' " % word)
        if cur.fetchone() is not None:
            return True
        else:
            return False
    except Exception , e:
        log.info_log('query word exist faield, %s' % str(e))
        return False

def add_word(db, word):
    try:
        t = (word, get_posix_time())
        db.execute('''\
                insert into dict_table values (?, ?)\
                ''', [t])
    except Exception, e:
        log.warn_log('add word to db failed, word: %s, error: %s ' % (word, str(e)))

def run(args, logFile):
    port = args.get('port')
    ip = args.get('ip')
    dbPath = args.get('db')
    url = args.get('url')
    init_log(logFile)
    log.debug_log('my pid is: %u , %s ' % (os.getpid(), args))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, port))
    sock.listen(5)
    try:
        db = DB(dbPath)
    except Exception , e:
        log.warn_log(str(e))
        sys.exit(1)

    try:
        db.execute('''create table dict_table (\
                word TEXT,\
                lastSchdulered INTEGER\
                )''')
    except Exception , e:
        log.info_log('table alreay exists! error: %s' % str(e))

    while True:
        cl, addr = sock.accept()
        word, trans = recv_request(cl)
        log.debug_log('receive word %s , need trans %d: ' % (word, trans))
        if not is_word_exist(db, word):
            add_word(db, word)
        cl.close()



