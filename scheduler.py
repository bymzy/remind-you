

#! -*- coding: utf-8 -*-

import multiprocessing
import json
import logging
import importlib
import time
import os

CONF_FILE = '/etc/scheduler.conf'

def parse_config(conf):
    with open(conf, 'r') as f:
        data = f.read()
        return json.loads(data)

def run_plugin(plugin):
    name = plugin.get('name')
    fileName = plugin.get('fileName')
    desc = plugin.get('desc')
    arg = plugin.get('args')

    module = importlib.import_module('plugins.' + fileName)
    process = multiprocessing.Process(target=module.run, args=(arg,))
    process.start()
    return process

def scheduler_loop():
    print 'main process pid: %u' % os.getpid()
    conf_dict = parse_config(CONF_FILE)
    process_list = []
    for plugin in conf_dict.get('plugins', []):
        process_list.append((plugin, run_plugin(plugin)))

    # monitor process 

    while True:
        to_add = []
        to_del = []
        for proc in process_list:
            if not proc[1].is_alive():
                proc[1].join()
                to_add.append((proc[0], run_plugin(proc[0])))
                to_del.append(proc)

        for proc in to_del:    
            process_list.remove(proc)
            to_del = []
                
        for proc in to_add:    
            process_list.append(proc)
            to_add = []

        time.sleep(2)
        
                

