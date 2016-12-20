import FlightRequester
import MyParser
import re
import countryinfo
import argparse
import sys
import requests
class FlightRequester:


    def pageReq(self,url):
        r = requests.get(url)
        feed = str(r.content)

        return feed



    def getDeals(self,iterations):
        deals = []
        for x in range(iterations):
            feed = self.pageReq("http://www.theflightdeal.com/category/flight-deals/page/%s" % x)
            parser = MyParser.TheFlightDealParser()
            parser.feed(feed)
            deals.extend(parser.deals)
        '''RETURNS Raw Descriptions'''
        return deals



    def sortDeals(self,deals):
        '''Sorts deals in order of ticket price'''
        sortDeals = []
        for d in deals:
            if not "[FARE GONE]" in d:
                m = re.search('\$(\d+)',d)
                if m is not None:
                    sortDeals.append((int(m.group(1)),d))
        sortDeals = sorted(set(sortDeals), key=lambda tup: tup[0])
        '''Returns tuple (PRICE, DESCRIPTION)'''
        return sortDeals
    
    def getDealsByContinent(self,dealTuple):
        dealsByCountry = {}
        dealsByCountry['Unknown'] = []
        for d in dealTuple:
            for country in countryinfo.countries:
                
                if country['name'] in d[1]:
                    if country['continent'] not in dealsByCountry:
                        dealsByCountry[country['continent']] = []
                    dealsByCountry[country['continent']].append(d)
                    
            if not any(country['name'] in d[1] for country in countryinfo.countries):
                    dealsByCountry['Unknown'].append(d)
        deals = sorted(dealsByCountry.items())
        return deals
