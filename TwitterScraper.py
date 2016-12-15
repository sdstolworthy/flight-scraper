import base64
import requests
import oauth2
import json
class TwitterScraper:
    #Global variables contain data needed to make twitter request
    #timeline_endpoints is a listing of twitter timelines to pull in
    clientKey = "dBZVGtMSRyuHphDRadmo2Oytb"
    clientSecret = "ZJ1vxBtVeM9Sq4WML7uyfuJxyHArRhivo8MUfeVfwPCXkGTYl9"
    timeline_endpoints = ["https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=TheFlightDeal",
            "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=FareDealAlert",
            "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=airfarewatchdog"]
    def oauth_req(self, url,secret = None, http_method="GET", post_body=b"",http_headers=None):
        #this function returns the result of a call to the twitter api
        consumer = oauth2.Consumer(key=self.clientKey,secret=self.clientSecret)
        token = oauth2.Token(key="3415862773-zCUjEYxs9sS0XYuxGfrgmYjuV6m0qooSK1AmNB4", secret="UCSPCeEcoGk0aYGJL08YS2TqtdgUQCVcHUIOngW07U0kp")
        client = oauth2.Client(consumer, token)
        resp, content = client.request( url, method=http_method, body=post_body, headers = http_headers )
        return content.decode('utf-8')
    def getTwitterDeals(self):
        tweetDeals = []
        for url in self.timeline_endpoints:
            #Make request to twitter API
            tweets = self.oauth_req(url)
            tweets = json.loads(tweets)
            #the loop cleans out irrelevant data. This is specially customized for each twitter feed
            for tweet in tweets:
                if "airfarewatchdog" in url:
                    if "#airfare" in tweet['text']:
                        tweetDeals.append(tweet['text'])
                if "TheFlightDeal" in url:
                    if "#Airfare" in tweet['text']:
                        tweetDeals.append(tweet['text'])
                else:
                    tweetDeals.append(tweet['text'])
        return tweetDeals
