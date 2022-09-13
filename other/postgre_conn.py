#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import sys

con = None

try:
    con = psycopg2.connect(database="imatrix-cube", host="52.81.4.224", port="5432", user="imatrix", password="D74GM8hHTU28y2QU")
    cur = con.cursor()
    cur.execute('select current_date')
    ver = cur.fetchone()
    print("\033[1;31;m", ver)
except psycopg2.DatabaseError as e:
    print('Error %s' % e)
    sys.exit(1)
finally:
    if con:
        con.close()