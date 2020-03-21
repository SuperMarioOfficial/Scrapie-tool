import urllib3
import time
from bs4 import BeautifulSoup
import signal

links_unvisited = set()
links_visited = set()
extracted_records = []

'''The urllib3.disable_warnings() function ignores any SSL certificate warnings.'''
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
req = urllib3.PoolManager()
depth = 3


def spider(url):
    '''You’ll need a PoolManager instance to make requests.
    This object handles all of the details of connection pooling
    and thread safety so that you don’t have to:'''
    try:
        r = req.request('GET', url)
        soup = BeautifulSoup(r.data.decode('utf-8'), 'html.parser').find_all('a', href=True)
        for link in soup:
            title = link.text
            url = link['href']
            record = {
                'title': title,
                'url': url
            }
            if not url.startswith('https'):
                pass
            else:
                links_unvisited.add(url)
                # extracted_records.append(record)
    except Exception as e:
        print(e)
        pass


def write_out():
    with open("links_visited.cvs", "w+") as file:
        for link in links_visited:
            file.write("{link},\n".format(link=link))
    file.close()
    with open("links_unvisited.cvs", "w+") as file:
        for link in links_unvisited:
            file.write("{link},\n".format(link=link))
    file.close()


signal.signal(signal.SIGINT, write_out)
spider('https://www.bbc.com/')
cycles = 5
while True:
    jumps = links_unvisited.copy()

    for link in jumps:
        spider(link)
        try:
            links_unvisited.remove(link)
            links_visited.add(link)
            print(link)
            print("links_unvisited = {links_unvisited}\nlinks_visited={links_visited},\ncurrent={jumps}".format(
                links_visited=len(links_visited),
                links_unvisited=len(
                    links_unvisited), jumps=len(jumps) - len(links_visited)))
        except Exception as e:
            print(e)
            pass
        cycles-=1
        if cycles <= 0:
            write_out()
            exit()



