#! /usr/bin/env python
# -*- coding: utf-8 -*- 


import daemon
from scheduler import scheduler_loop

if __name__ == "__main__":
    with daemon.DaemonContext():
        scheduler_loop()

