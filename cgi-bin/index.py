# -*- coding: utf-8 -*-

import cgi
from get_data import get_data
import xml.etree.ElementTree as ET

BBC_URL = "http://feeds.bbci.co.uk/japanese/rss.xml"
XML_string = get_data(BBC_URL)

root = ET.fromstring(XML_string)

"""
below tag description
0:title
1:description
2:link
5:image
"""

articleList = []
for e in root.iter("item"):
    if "video" not in e[2].text:
        if(len(e) > 5):
            Attr = e[5].attrib
            articleList.append([e[0].text, e[1].text, e[2].text, Attr["url"]])
        else:
            articleList.append([e[0].text, e[1].text, e[2].text])


html_body = """
<!DOCTYPE html>
<html lang="jp">
<head>
    <meta charset="UTF-8">
    <title>BBC_Reader</title>
    <link rel="stylesheet" type="text/css" href="../web/line.css">
</head>
<body>
<header>BBC_Reader</header>
%s
</body>
</html>
"""

add_tag_image="""
<div class="rss_box">
    <img class="rss_image" src="%s">
    <div class="rss_contents_image">
        <div class="contents_title">
             <form name="sendURL%s" action="get_url.py" method="post" >
                <input type="hidden" name="articleURL" value="%s">
                <a href="javascript:sendURL%s.submit()">%s</a>
            </form>
        </div>
        <br>
        <div class="contents_description">
            %s
        </div>
    </div>
</div>
"""

add_tag="""
<div class="rss_box">
    <div class="rss_contents">
        <div class="contents_title">
            <form name="sendURL%s" action="get_url.py" method="post" >
                <input type="hidden" name="articleURL" value="%s">
                <a href="javascript:sendURL%s.submit()">%s</a>
            </form>
        </div>
        <div class="contents_description">
            %s
        </div>
    </div>
</div>
"""

add_html = ""
count = 1

for article in articleList:
    if(len(article) > 3):
        add_html = add_html + add_tag_image %(article[3],count,article[2],count,article[0],article[1])
    else:
        add_html = add_html + add_tag % (count,article[2],count, article[0], article[1])
    count = count + 1
print(html_body % add_html)