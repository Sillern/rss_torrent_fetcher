#! /usr/bin/env python

def convert_sqlite( filename ):
    from cStringIO import StringIO
    from tempfile import NamedTemporaryFile
    import os
    try:
      from pysqlite2 import dbapi2 as sqlite
    except ImportError:
      import sqlite3 as sqlite

    temp = NamedTemporaryFile(mode="w+b", delete=False)
    try:
        db_file = open(filename, "r+b")
        temp.write(db_file.read())
        db_file.close()
    finally:
        temp.close()

    con = sqlite.connect(temp.name)
    con.text_factory = str
    cur = con.cursor()
    cur.execute("select host_key, path, secure, expires_utc, name, value from cookies")

    ftstr = ["FALSE","TRUE"]

    s = StringIO()
    s.write("""\
# Netscape HTTP Cookie File
# http://www.netscape.com/newsref/std/cookie_spec.html
# This is a generated file!  Do not edit.
""")
    for item in cur.fetchall():
        s.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
            item[0], ftstr[item[0].startswith('.')], item[1],
            ftstr[item[2]], item[3], item[4], item[5]))

    try:
        os.remove(temp.name)
    except:
        pass

    s.seek(0)

    cookie_jar = cookielib.MozillaCookieJar()
    cookie_jar._really_load(s, '', True, True)
    return cookie_jar

import cookielib
import os
import sys

def get_cookie_file():
    cookie_file = os.path.join( os.path.expanduser( "~" ), ".config", "chromium", "Default", "Cookies")
    if os.path.exists( cookie_file ):
        return cookie_file
    return None

def get_cookie_jar():
    return convert_sqlite( get_cookie_file() )

if __name__ == "__main__":
    import pprint
    for cookie in get_cookie_jar():
      print cookie
