import base64
import requests
import oauth2
import json
class TwitterScraper:
    clientKey = "dBZVGtMSRyuHphDRadmo2Oytb"
    clientSecret = "ZJ1vxBtVeM9Sq4WML7uyfuJxyHArRhivo8MUfeVfwPCXkGTYl9"
    timeline_endpoints = ["https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=TheFlightDeal",
            "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=FareDealAlert"]
    def oauth_req(self, url,secret = None, http_method="GET", post_body=b"",http_headers=None):
        consumer = oauth2.Consumer(key=self.clientKey,secret=self.clientSecret)
        token = oauth2.Token(key="3415862773-zCUjEYxs9sS0XYuxGfrgmYjuV6m0qooSK1AmNB4", secret="UCSPCeEcoGk0aYGJL08YS2TqtdgUQCVcHUIOngW07U0kp")
        client = oauth2.Client(consumer, token)
        resp, content = client.request( url, method=http_method, body=post_body, headers = http_headers )
        return content.decode('utf-8')
    def getTwitterDeals(self):
        tweetDeals = []
        for url in self.timeline_endpoints:
            tweets = self.oauth_req( url )
            tweets = json.loads(tweets)
            for tweet in tweets:
                tweetDeals.append(tweet['text'])
        return tweetDeals
