import urllib3
from bs4 import BeautifulSoup

'''The urllib3.disable_warnings() function ignores any SSL certificate warnings.'''
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
req = urllib3.PoolManager()


def spider(url):
    '''You’ll need a PoolManager instance to make requests.
    This object handles all of the details of connection pooling
    and thread safety so that you don’t have to:'''
    try:
        r = req.request('GET', url)
        soup = BeautifulSoup(r.data.decode('utf-8'), 'html.parser').find_all('a', href=True)
        with open("scrapied.cvs", "w+") as file:
            for link in soup:
                if not url.startswith('https') or link.text =="edit":
                    pass
                else:
                    file.write("{link}<br>\n".format(link=link))
        file.close()
    except Exception as e:
        print(e)
        pass


spider('https://en.wikipedia.org/wiki/List_of_paradoxes')
