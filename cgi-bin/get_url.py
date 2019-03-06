# -*- coding: utf-8 -*-

import cgi
from get_data import get_data
from bs4 import BeautifulSoup
import bs4

form = cgi.FieldStorage()
URL = form.getfirst("articleURL","")

def analysis(HTML_string):
    data = BeautifulSoup(HTML_string, "html.parser")
    article = data.find("div", class_="story-body")
    article_title = article.find("h1",class_="story-body__h1").text
    article_contents = article.find("div",class_="story-body__inner")
    #figureタグは未対応
    for child in article_contents.children:
        if(child.name != "p" and child.name != "ul" and False == isinstance(child,bs4.element.NavigableString) ):
            child.decompose()
    return [article_title,article_contents]

html_body = """
<!DOCTYPE html>
<html lang="jp">
<head>
    <meta http-equiv="Cache-Control" content="no-cache">
    <meta charset="UTF-8">
    <title>BBC_Reader</title>
    <link rel="stylesheet" type="text/css" href="../web/article.css">
    <script src="../web/jquery-3.3.1.min.js"></script>
</head>
<body>
<header>BBC_Reader</header>

<div id="container">
    <div id="left">
        <header class="container_header">
           %s
        </header>
        <div class="contents">
            %s
        </div>
    </div>
    <div id="right">
        <header class="container_header">
            %s
        </header>
        <div class="contents">
            %s
        </div>
    </div>
</div>

</body>
<script>
    var container_h = document.getElementById('container').clientHeight;
    var container_header_collection = document.getElementsByClassName('container_header');
    var container_header_h = container_header_collection[0].clientHeight;
    var contents_h = container_h - container_header_h;
    contents_h = contents_h + 'px';
    $("div.contents").css("max-height",contents_h);
</script>
</html>
"""

if URL is not None:
    #日本語記事を取得
    HTML = get_data(URL)
    Jarticle = analysis(HTML)

    articleLink = Jarticle[1].find_all("a",class_="story-body__link")[-1]["href"]

    if articleLink.startswith("http") == False:
        articleLink = "http://www.bbc.com" + articleLink

    #英語記事を取得
    HTML = get_data(articleLink)
    Earticle = analysis(HTML)

    html = html_body % (Jarticle[0],Jarticle[1],Earticle[0],Earticle[1])
    print(html)