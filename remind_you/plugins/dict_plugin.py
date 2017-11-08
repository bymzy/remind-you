# -*- coding: utf-8 -*-

import time
import os
import requests
import socket
import struct
import sys
import threading
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from remind_you.plugins.log import Log
from remind_you.plugins.util import pack_str, recv_len, unpack_int, unpack_str, pack_int, get_posix_time, init_email, send_email
from remind_you.plugins.db import DB

log = None
WORD_ONE_EMAIL = 5

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

def touch_word(db, word, when):
    try:
        db.execute("update dict_table set lastSchdulered = %d where word = '%s'" % (when, word))
    except Exception, e:
        log.warn_log('touch word to db failed, word: %s, error: %s ' % (word, str(e)))

def query_word(word, url):
    target = '%s?Word=%s&Samples=false' % (url, word)
    print target
    r = requests.get(target)
    di = json.loads(r.content)
    del di['sams']
    if di.get('pronunciation') != None:
        di['BrE'] = di['pronunciation']['BrE']
        di['AmE'] = di['pronunciation']['AmE']
    del di['pronunciation']
    del di['word']
    return json.dumps(di, indent=4, ensure_ascii=False) + "\n"

def init_email():
    smtpObj = smtplib.SMTP_SSL('smtp.126.com', 465)
    smtpObj.login('huhsming@126.com', '@1992915')
    return smtpObj

def send_email(smtpObj, destList, content):
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header('remind-you service')
    message['To'] = Header('brokers')
    message['Subject'] = Header('English Word Information', 'utf-8')
    smtpObj.sendmail('huhsming@126.com', destList, message.as_string())

def send_email_thread(dbPath, log, url):
    print 'aa'
    log.info_log('send email thread start!!!')

    try:
        db = DB(dbPath)
    except Exception , e:
        log.warn_log(str(e))
        sys.exit(1)

    while True:
        smtpObj = init_email()
        try:
            cur = db.execute('select word from dict_table order by lastSchdulered limit %d' % WORD_ONE_EMAIL)
            item_list = cur.fetchall()
            word_list = []
            data = 'Today words: \n'
            for item in item_list:
                word_list.append(item[0])
                touch_word(db, item[0], get_posix_time())

            for word in word_list:
                item = '[==  %s  ==] \n' % word
                item += query_word(word, url)
                data += item

            print 'going to send email'
            send_email(smtpObj, ['huhsming@126.com'], data)
            log.debug_log('send words %s' % data)
        except Exception, e:
            log.warn_log(str(e))
        time.sleep(3600 * 24)

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

    thread = threading.Thread(target=send_email_thread, args=(dbPath, log, url))
    thread.start()
    log.info_log('after start thread')

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
        else:
            touch_word(db, word, 0)
        cl.close()

if __name__ == "__main__":
    args = {
            'ip': '127.0.0.1',
            'port': 6666,
            'db': '/etc/.remind_you/db/dict.db',
            'url': 'http://xtk.azurewebsites.net/BingDictService.aspx',
            }
    run(args, '/tmp/remind_you.log')


