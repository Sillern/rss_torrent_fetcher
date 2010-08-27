from rss import Site

site = Site(name="A TV-site") 

user = 1
pass = "secretkey"
site.fetch(url="http://www.a_tv_site.com/rss.php?uid=%d&passkey=%s" % (user, pass))

ruleset = {
    "title": [
            r"^(royal[ \.]remedies).*(720).*",
            r"^(warm[ \.]notice).*(720).*",
            r"^(presentarama).*(720).*",
            r"^(sike).*(720).*",
            r"^(false[ \.]blood).*(720).*",
        ],
}

site.parse(ruleset)

site.download(directory="/home/rtorrent/watch/tv/")

