import os
import shutil
import os.path as path
import argparse
import requests
from bs4 import BeautifulSoup as bs4
import json

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--outdir', nargs='?', default='out')
    return parser.parse_args()


def make_output_dir(outdir):
    if not path.exists(outdir):
        print(rf'mkdir {outdir}')
        os.makedirs(outdir)


def copy_css_to_out_dir(css_file, outdir):
    print(rf'copy {css_file} to {outdir}')
    shutil.copy(css_file, outdir)


def get_raw_page_contents(url, as_binary = False):
    print(rf'reading {url}')
    response = requests.get(url)
    if response.status_code == 200:
        if as_binary:
            return response.content
        else:
            return response.text
    return None


def extract_one_page(template, url):
    data = get_page_contents(url)
    if data is None:
        return


def read_template(template_file_name):
    print(rf'reading template: {template_file_name}')
    with open(template_file_name, 'r') as f:
        return f.read()


def print_header():
    print('Started scrapping')


def get_links(raw_contents, selector):
    dom = bs4(raw_contents, 'html.parser')
    return dom.select(selector)


def url_to_file_name(url, file_name_template, outdir):
    start_index = url.find('game/') + 5
    end_index = 1000
    if (url[-1] == '/'):
        end_index = -1

    return file_name_template.format(outdir, url[start_index:end_index].replace('/', '-'))


def process_article(article_url, template, outdir):
    print(rf'Trying to retrieve {article_url}')
    file_name = url_to_file_name(article_url, '{}/{}.html', outdir)
    if path.exists(file_name):
        print('skipping, link is already processed and saved')
        return

    raw_article = get_raw_page_contents(article_url)

    dom = bs4(raw_article, 'html.parser')
    contents = dom.select('div#content > article')[0]
    contents.footer.decompose()
    for sociable in contents.select('div.sociable'):
        sociable.decompose()


    print('Retrieving article images')
    for image_link_tag in contents.select('img'):
        image_url = image_link_tag.get('src')
        print(rf'Trying to retrieve {image_url}')
        image_file_name = url_to_file_name(image_url, '{}/img/{}', outdir)
        if path.exists(image_file_name):
            continue
        image_data = get_raw_page_contents(image_url, True)
        with open(image_file_name, 'wb') as f:
            f.write(image_data)
        image_link_tag['src'] = image_file_name
        image_link_tag.parent['href'] = image_file_name

    print(rf'Article retrieved, processed, writing {file_name}')
    with open(file_name, 'w') as f:
        f.write(template.format(dom.title.text, contents))

# main
args = get_args()

print_header()
make_output_dir(rf'{args.outdir}/img')
copy_css_to_out_dir('src/main.css', args.outdir)
template = read_template('src/template.html')
# read raw html of index page
# extract links to articles
# 

#raw_contents = get_raw_page_contents('http://www.ultimaratioregum.co.uk/game/')

#article_links
#for article_link_tag in get_links(raw_contents, 'h1.entry-title > a'):
#    process_article(article_link_tag.get('href'))


# process_article('http://www.ultimaratioregum.co.uk/game/2018/06/07/i-did-some-programming/', template, args.outdir)
process_article('http://www.ultimaratioregum.co.uk/game/2011/09/23/late-september-screenshot-update/', template, args.outdir)

#scrap(args.outdir)

# request html
# extract title
# extract article
# format template
# extract image links
# create image directories
# curl images by links to directories
# save template to output
# add it to main 'index' page



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
