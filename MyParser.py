from html.parser import HTMLParser

class TheFlightDealParser(HTMLParser):
    title = False
    collectData = False
    urls = []
    Pagination = False
    urlIndex = 0
    collectUrl = None
    deals = []
    def handle_starttag(self, tag, attrs):
        '''Handles opening HTML tags'''

        ### This section takes care of finding the listings on the current page ###
        if tag == 'h1':
            #print("this is h1")
            for key,value in attrs:
                if key == 'class':
                    #print(value)
                    if value == "\\'post-title\\'":
                        #print("You done it!!")
                        self.title = True
        if tag == 'a' and self.title:
            for key,value in attrs:
                if key == 'href':
                    #print(value)
                    self.title = False
                    self.collectData = True
        ### END SECTION ###

        ### This section handles getting the urls of the continuing pages ###
        if tag == 'div':
            for key, value in attrs:
                if value == "\\'pagination\\'":
                    #print("Hey there!!!!!!")
                    self.Pagination = True
        if tag == 'span':
            for key,value in attrs:
                if key == 'class' and value == "\\'current\\'":
                    self.collectUrl = True
        if tag == 'a' and self.collectUrl:
            if self.urlIndex < 2:
                self.urlIndex += 1
                for key, value in attrs:
                    if key == 'href':
                        #print(" THIS IS YOUR NEXT URL:  %s" % value.replace('\\',''))
                        self.urls.append(value.replace('\\', ''))
            else:
                self.urlIndex = 0
                self.collectUrl = False
    def handle_endtag(self, tag):
        if tag == 'a' and self.title:
            self.title = False
    def handle_data(self, data):
        if self.collectData:
            #print("%s\n\n" % data)
            self.deals.append(data)
            self.collectData = False
