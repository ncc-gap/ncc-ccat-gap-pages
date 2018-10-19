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

html_header = """<html lang="ja">
<head>
  <title>index</title>
  <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="github-markdown.css"/>
    <style>
        body {
            margin: 80px;
        }
    </style>
</head>
<body>
"""

html_footer = """
</body>
</html>
"""

import sys
import os

current = os.path.abspath(os.path.dirname(sys.argv[0]) + "/../")
mds = glob.glob(current + "/markdown/*.md")

for md in mds:
    
    data = open(md,'br').read()
            
    request = urllib.request.Request('https://api.github.com/markdown/raw')
    request.add_header('Content-Type','text/plain')
    f = urllib.request.urlopen(request,data)
    open('temp','bw').write(f.read())
    
    output = current + "/html/" + os.path.splitext(os.path.basename(md))[0] + ".html"
    print ("%s\n  ==> %s" % (md, current))
    
    with open(output, 'w') as file:
        file.write(html_header)
        file.write(open('temp').read())
        file.write(html_footer)
    
    os.remove('temp')
