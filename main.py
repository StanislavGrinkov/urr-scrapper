# read top page
# extract article links
# save article links
# link, isVisited

from link import Link

l = Link('aaa', False)
k = Link('bbb', True)

print(k)
print(l)

#import requests
#from bs4 import BeautifulSoup as BS
#import json

#data = json.load()

# print(argv)

#def visit_and_collect(page):
#    url_templ = rf"http://www.ultimaratioregum.co.uk/game/page/{page}/"
#    if page < 2:
#        url_templ = "http://www.ultimaratioregum.co.uk/game/"
#    print(url_templ)
#
#    response = requests.get(url_templ)
#    print(f'status:{response.status_code}')
#    data = BS(response.text, 'html.parser')
#    for link in data.select('h1[class="entry-title"] a'):
#        print(f"{link.string}: {link.get('href')}")
#
#    as_t = [{'link': link.get('href'), 'title': link.string} for link in data.select('h1[class="entry-title"] a')]
#    print(as_t)
#
#    with open('dump.j', 'w') as f:
#        json.dump(as_t, f)
#
#    #link_r = r'<a href="([^"]+?)"[\s\w]+rel="bookmark">([^<]+?)</a>'
#    #m = re.findall(link_r, raw_data, re.MULTILINE)
#
#
##def main():
##     urls = [url_templ.format(i) for i in range(56, 1, -1)]
##     for v in urls:
##         print(v)
#
#
#visit_and_collect(2)





#if m:
 #   for link, title in m:
#        print (f"{title}: {link}")
#    m = re.search(link_r, raw_data, re.MULTILINE)
