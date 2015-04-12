from flask import render_template, session
from ironworks import serverTools, feedparser


app = serverTools.getApp()
logger = serverTools.getLogger()


@app.route('/latestNews')
def latestNews():
    if 'username' in session:
        hackaday, io9, mentalFloss, sparkfun, google, wallStreet, tech, linux = parseFeeds()
        #active_server=active_server,
        return render_template('home/latestNews.html',
                                hackadayFeed=hackaday,
                                io9Feed=io9,
                                mentalFlossFeed=mentalFloss,
                                sparkfunFeed=sparkfun,
                                googleFeed=google,
                                wallStreetFeed=wallStreet,
                                techNewsFeed=tech,
                                linuxNewsFeed=linux)
    return render_template('index.html')


def parseFeeds():
    # Feeds

    hackaday_url = 'http://feeds2.feedburner.com/hackaday/LgoM'
    io9_url = 'http://io9.com/rss'
    mental_floss_url = 'http://mentalfloss.feedsportal.com/c/35119/f/649404/index.rss'
    google_url = 'https://news.google.com/news?pz=1&cf=all&ned=us&siidp=a3761a02c7bb42a6b2f9e47806ce78c4bb0d&ict=ln&output=rss'
    wallStreet_url = 'http://online.wsj.com/xml/rss/3_7014.xml'
    techNews_url = "http://www.technewsworld.com/perl/syndication/rssfull.pl"
    linuxNews_url = "http://www.linuxinsider.com/perl/syndication/rssfull.pl"
    sparkfun_url = 'https://www.sparkfun.com/feeds/news'

    hackaday_feeds = feedparser.parse(hackaday_url)
    io9_feeds = feedparser.parse(io9_url)
    mental_floss_feeds = feedparser.parse(mental_floss_url)
    sparkfun_feeds = feedparser.parse(sparkfun_url)
    google_feeds = feedparser.parse(google_url)
    wallStreet_feeds = feedparser.parse(wallStreet_url)
    techNews_feeds = feedparser.parse(techNews_url)
    linuxNews_feeds = feedparser.parse(linuxNews_url)
    return hackaday_feeds, io9_feeds, mental_floss_feeds, sparkfun_feeds, google_feeds, wallStreet_feeds, techNews_feeds, linuxNews_feeds
