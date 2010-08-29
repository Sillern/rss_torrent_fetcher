from rss import Site

ruleset = {
    "title": [
            r"^(royal[ \.]remedies).*(720).*",
            r"^(warm[ \.]notice).*(720).*",
            r"^(presentarama).*(720).*",
            r"^(sike).*(720).*",
            r"^(false[ \.]blood).*(720).*",
        ],
}

site = Site(name="A TV site", url="http://www.atvsite.com/rss/id/1", ruleset=ruleset, directory="/home/rtorrent/watch/tv/", schedule=10)

site.run()
