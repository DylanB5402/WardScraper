from ebooklib import epub

book = epub.EpubBook()
book.set_identifier('test001')
book.set_title('test')
book.set_language('en')
book.add_author('me')
c1 = epub.EpubHtml(title='Intro', file_name='chap_01.xhtml', lang='hr')
c1.content=u'lines are fun'
book.add_item(c1)
book.spine = ['nav', c1]
book.toc = (epub.Link('chap_01.xhtml', 'Introduction', 'intro'),
         (epub.Section('Simple book'),
         (c1, ))
        )
epub.write_epub('test2.epub', book, {})