# -*- coding: utf-8 -*-

import sqlite3

class DB(object):
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = None

    def execute(self, script, args = []):
        print 'sql script: %s' % script
        with self.conn:
            if len(args) == 0:
                return self.conn.execute(script)
            else:
                return self.conn.executemany(script, args)




