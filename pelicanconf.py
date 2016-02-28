#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'bigpotato'
SITENAME = u"bigpotato's blog"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

#pelican theme path
THEME = '../pelican-bootstrap3'
LOAD_CONTENT_CACHE = False

#plugins
PLUGIN_PATHS = ["plugins"]
PLUGINS = ['better_codeblock_line_numbering', 'tag_cloud', 'summary']
TAG_CLOUD_STEPS = 4
TAG_CLOUD_MAX_ITEMS = 100
TAG_CLOUD_SORTING = 'random'
MD_EXTENSIONS = [
    'codehilite(css_class=highlight,linenums=False)',
    'extra'
    ]

# Blogroll
LINKS = (('Leetcode', 'https://oj.leetcode.com/'),
		 ('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Arch Linux', 'https://www.archlinux.org/'),
         ('Markdown语法说明', 'http://wowubuntu.com/markdown/'),)

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)
#

# tag cloud
DISPLAY_TAGS_INLINE = True
# show categories on sidebar
DISPLAY_CATEGORIES_ON_SIDEBAR = True
# show recent posts
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
# don't show category on menu
DISPLAY_CATEGORIES_ON_MENU = False
DEFAULT_PAGINATION = 10
#Disqus comments
SITEURL = u"http://bigpotato920.github.io"
DISQUS_SITENAME = u"bigpotato4future"
# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False
