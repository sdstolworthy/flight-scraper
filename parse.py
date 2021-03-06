import requests
import MyParser
import re
import countryinfo
import argparse
import sys
from FlightRequester import FlightRequester
from TwitterScraper import TwitterScraper
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
flights = FlightRequester()
twitter = TwitterScraper()
if len(sys.argv) > 1:
    print(sys.argv[1])
iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 1
deals = []
deals = flights.getDeals(iterations)
deals.extend(twitter.getTwitterDeals())
deals = flights.sortDeals(deals)
deals = flights.getDealsByContinent(deals)
for key, value in deals:
    print(bcolors.BOLD + bcolors.OKBLUE + '\n\n%s'% key + bcolors.ENDC + bcolors.ENDC)
    for deal in value:
        print(bcolors.WARNING + "$%s" % deal[0] + bcolors.ENDC + " ---> %s" % deal[1])
    #print(key)
