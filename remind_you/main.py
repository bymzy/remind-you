#! /usr/bin/env python
# -*- coding: utf-8 -*- 


import daemon
from remind_you.scheduler import scheduler_loop

def run_main():
    with daemon.DaemonContext():
        scheduler_loop()

if __name__ == "__main__":
    scheduler_loop()


