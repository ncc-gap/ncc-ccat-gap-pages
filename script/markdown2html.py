# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:46:34 2018

https://qiita.com/__mick/items/c80fab6c185a41882880
https://gist.github.com/oguna/9683208

this script on only PYTHON3

use this:
python3 ./markdown2html.py

@author: Okada
"""

import glob
import urllib.request
import urllib.parse
import sys
import os
import re

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    h1 = False
    title = ""    
    def handle_starttag(self, tag, attrs):
        if tag == "h1":
            self.h1 = True

    def handle_endtag(self, tag):
        if tag == "h1":
            self.h1 = False
        
    def handle_data(self, data):
        if self.h1 == True:
            self.title += data.rstrip()

html_header = """<html lang="ja">
<head>
  <title>{title}</title>
  <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="./github-markdown.css"/>
    <link rel="stylesheet" type="text/css" href="./extention.css"/>
</head>
<body>
"""

html_footer = """
</body>
</html>
"""

current = os.path.abspath(os.path.dirname(sys.argv[0]) + "/../")
mds = glob.glob(current + "/*/markdown/*.md")

for md in mds:
    
    data = open(md,'br').read()
            
    request = urllib.request.Request('https://api.github.com/markdown/raw')
    request.add_header('Content-Type','text/plain')
    f = urllib.request.urlopen(request,data)
    open('temp','bw').write(f.read())
    
    output = re.sub(r'\.md$', ".html", md.replace("/markdown/", "/html/"))
    os.makedirs(os.path.dirname(output), exist_ok = True)
    
    print ("%s\n  ==> %s" % (md, output))
    
    with open(output, 'w') as file:
        contents = open('temp').read()
        parser = MyHTMLParser()
        parser.feed(contents)

        file.write(html_header.format(title = parser.title))
        file.write(contents)
        file.write(html_footer)
    
    os.remove('temp')
