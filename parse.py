import requests
import MyParser
import re
import countryinfo
import argparse
import sys
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
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
flights = FlightRequester()
if len(sys.argv) > 1:
    print(sys.argv[1])
iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 10
sortDeals = flights.sortDeals(flights.getDeals(iterations))

deals = flights.getDealsByContinent(sortDeals)
for key, value in deals:
    print(bcolors.BOLD + bcolors.OKBLUE + '\n\n%s'% key + bcolors.ENDC + bcolors.ENDC)
    for deal in value:
        print(bcolors.WARNING + "$%s" % deal[0] + bcolors.ENDC + " ---> %s" % deal[1])
    #print(key)
