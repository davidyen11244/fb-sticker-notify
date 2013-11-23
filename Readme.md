Facebook Stickers Notify
=======================
Facebook got lots of cool stickers. I like to be notifed when there are new stickers available. But there is no official API about the stickers. So I made one using HTTP POST, and it works well.

Feel free to open issues and send pull request.

Requirements
------------

* Python 2.7 - [http://python.org](http://python.org)
* BeautifulSoup4 - [http://www.crummy.com/software/BeautifulSoup/]
* Requests - [http://docs.python-requests.org/en/latest/index.html](http://docs.python-requests.org/en/latest/index.html()

Usage
-----
1. Fill in your username and password in settings.py.
2. python stickers.py and you're good to go. 

You can add the stickers.py in your crontab. If there are new stickers, it can notify you by email.
