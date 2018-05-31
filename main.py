import requests
import re

links = {}
visited_links = {}
url_templ = "http://www.ultimaratioregum.co.uk/game/page/{}/"

#def main():
#    urls = [url_templ.format(i) for i in range(56, 1, -1)]
#    for v in urls:
#        print(v)


#main()


response = requests.get(url_templ.format(2));

print(f"status:{response.status_code}")

raw_data = response.text
link_r = r'<a href="([^"]+?)"[\s\w]+rel="bookmark">([^<]+?)</a>'
m = re.findall(link_r, raw_data, re.MULTILINE)

if m:
    for link, title in m:
        print (f"{title}: {link}")
#    m = re.search(link_r, raw_data, re.MULTILINE)
