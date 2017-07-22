# -*- coding: utf-8 -*-

'''
cmd script for plugin dict
'''

import json
import sys
import socket
import argparse
from remind_you.plugins.util import connect_ip_port, send_data 
from remind_you.plugins.dict_plugin import generate_request

CONF = '/etc/scheduler.conf'
PLUGIN_NAME = 'dict'

def get_ip_port():
    with open(CONF) as f:
        data = f.read()

    di = json.loads(data)
    for plugin in di.get('plugins', []):
        if plugin.get('name') == PLUGIN_NAME:
            return plugin.get('args').get('ip'), plugin.get('args').get('port')
    return None, None

def parse_cmd_args():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("-w", "--word", type=str, required=True);
    args_parser.add_argument('-t', '--trans', action='store_true', default=False);

    args = args_parser.parse_args()
    #use vars to get a dict
    #print vars(args), type(vars(args))
    return args.word, args.trans

def run():
    ip, port = get_ip_port()
    word, trans = parse_cmd_args()
    s = connect_ip_port(ip, port)
    if s is None:
        print 'connect to server %s:%d failed!!!' % (ip, port)
        sys.exit(1)
    req = generate_request(word, trans)
    send_data(s, req)

if __name__ == "__main__":
    run()


