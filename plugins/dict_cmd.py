# -*- coding: utf-8 -*-

'''
cmd script for plugin dict
'''

import json
import sys
import socket
import argparse

CONF = 'conf.json'
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
    args_parser.add_argument('-t', '--trans', action=store_true, default=False);

    #TODO parse cmd args
    
def run():
    ip, port = get_ip_port()
    
    




