# -*- coding: utf-8 -*-
from lxml import html
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from ebooklib import epub

#http://docs.sourcefabric.org/projects/ebooklib/en/latest/tutorial.html#creating-epub
# https://www.parahumans.net/2017/10/21/glow-worm-0-1/
# https://github.com/DylanB5402/Python-Stuffs/blob/master/EbookScrapers/TwigScraper.py
# https://github.com/DylanB5402/Python-Stuffs/blob/master/EbookScrapers/Scraper.py

def print_by_line(a : list):
    for item in a:
        print(item)

page = requests.get('https://www.parahumans.net/table-of-contents/')
webpage = html.fromstring(page.content)
links = webpage.xpath('//a/@href')
# print(links)
a = 0
# for link in links:
#     print(a, link)
#     a += 1
possible_chapters = links[297:594]
chapter_links = []
for chapter in possible_chapters:
    if not ("category" in chapter or "content" in chapter):
        chapter_links.append(chapter)
# print_by_line(chapters)
ward = epub.EpubBook()
ward.set_title("Ward")
ward.set_language("en")
ward.add_author("Wildbow")
style = 'body { font-family: Times, Times New Roman, serif; }'

nav_css = epub.EpubItem(uid="style_nav",
                        file_name="style/nav.css",
                        media_type="text/css",
                        content=style)
ward.add_item(nav_css)

# for link in chapter_links:
link = chapter_links[0]
chapter = requests.get(link)
content = chapter.content
soup = BeautifulSoup(content, "lxml")
text = soup.getText()
# print(str(soup))
start = text.index("Next Chapter")
end = text.index("Next Chapter", text.index("Next Chapter") + 1)
text = text[start + 13:end]
# print(text)
text = "<p>" + text.replace("\n", "<br>") + "</p>"
print(text)
chapter_title = soup.find("title").getText()[0: text.index("Parahumans") - 16]
epub_chapter = epub.EpubHtml(title = chapter_title, file_name = chapter_title.replace(" ", "") + ".xhtml", lang="en")
epub_chapter.content = text
# epub_chapter.content = u'' + text

ward.spine = ['nav', epub_chapter]
ward.add_item(epub_chapter)
epub.write_epub("Ward.epub", ward)
