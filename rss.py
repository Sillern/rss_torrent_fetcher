﻿# Copyright 2010 Sebastian Jegerås. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
# 
#    1. Redistributions of source code must retain the above copyright notice, this list of
#       conditions and the following disclaimer.
# 
#    2. Redistributions in binary form must reproduce the above copyright notice, this list
#       of conditions and the following disclaimer in the documentation and/or other materials
#       provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY Sebastian Jegerås ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Sebastian Jegerås OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# The views and conclusions contained in the software and documentation are those of the
# authors and should not be interpreted as representing official policies, either expressed
# or implied, of Sebastian Jegerås.

import urllib, urllib2, cookielib
from dependencies import firefox_cookies
import re
import feedparser
from urlparse import urlparse
from os import path

class Site:
    def __init__(self, name):
        self.name = name
        self.cookiejar = firefox_cookies.get_cookie_jar()

    def fetch(self, url):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))
        r = opener.open(url)
        self.data = r.read()
        r.close()
    
    def parse(self, ruleset):
        parsed_data = feedparser.parse(self.data)
        self.matched_entries = []

        for key, rules in ruleset.iteritems():
            for rule in rules:
                pattern = re.compile(rule, re.IGNORECASE)
                for entry in parsed_data["entries"]:
                    if pattern.match(entry[key]):
                        self.matched_entries.append(entry)

    def download(self, directory):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))

        for entry in self.matched_entries:
            link = entry["link"]
            filename = urlparse(link).path.split("/")[-1]

            print "downloading", filename

            r = opener.open(link)
            data = r.read()
            r.close()

            filepath = path.join(directory, filename)

            print "saving", filepath

            downloaded_file = open(filepath, "w+b")
            downloaded_file.write(data)
            downloaded_file.close()
        
