import requests
import MyParser
import re
import countryinfo
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def pageReq(url):
    r = requests.get(url)
    feed = str(r.content)

    return feed
deals = []
for x in range(10):
    feed = pageReq("http://www.theflightdeal.com/category/flight-deals/page/%s" % x)
    parser = MyParser.TheFlightDealParser()
    parser.feed(feed)
    deals.extend(parser.deals)
moneyre = re.compile('\$\d+')
sortDeals = []
for d in deals:
    if not "[FARE GONE]" in d:
        #print(d)
        m = re.search('\$(\d+)',d)
        if m is not None:
            #print(m.group(1))
            sortDeals.append((int(m.group(1)),d))
sortDeals = sorted(set(sortDeals), key=lambda tup: tup[0])
dealsByCountry = {}
dealsByCountry['Unknown'] = []
for d in sortDeals:
    for country in countryinfo.countries:
        
        if country['name'] in d[1]:
            if country['name'] not in dealsByCountry:
                dealsByCountry[country['name']] = []
            dealsByCountry[country['name']].append(d)
            #print("%%%%%%%%%% COUNTRY NAME -----> %s" % country['name'])
            
    if not any(country['name'] in d[1] for country in countryinfo.countries):
            dealsByCountry['Unknown'].append(d)
    #print("$%s ---> %s" % (d[0],d[1]))
deals = sorted(dealsByCountry.items())
for x in deals:
    print(x)
for key, value in deals:
    print(bcolors.BOLD + bcolors.OKBLUE + '\n\n%s'% key + bcolors.ENDC + bcolors.ENDC)
    for deal in value:
        print(bcolors.WARNING + "$%s" % deal[0] + bcolors.ENDC + " ---> %s" % deal[1])
    #print(key)
