import os
import shutil
import os.path as path
import argparse
import requests
from bs4 import BeautifulSoup as bs4

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--outdir', nargs='?', default='out')
    parser.add_argument('--index', nargs='?', default='1')
    return parser.parse_args()


def make_output_dir(outdir):
    if not path.exists(outdir):
        print(rf'mkdir {outdir}')
        os.makedirs(outdir)


def copy_css_to_out_dir(css_file, outdir):
    print(rf'copy {css_file} to {outdir}')
    shutil.copy(css_file, outdir)


def fetch_url(url, as_binary = False):
    print(rf'Fetching: {url}')
    try:
        response = requests.get(url, timeout=10)
    except (requests.exceptions.Timeout):
        print(rf'----->  Exception while fetching {url}.')
        return None
    if response.status_code == 200:
        return response.content if as_binary else response.text
    else:
        return None


def read_template(template_file_name):
    print(rf'Reading template: {template_file_name}')
    with open(template_file_name, 'r') as f:
        return f.read()


def print_header():
    print('Started scrapping')


def url_to_file_name(url, file_name_template='{}.html'):
    start_index = url.find('game/') + 5
    end_index = 1000
    if (url[-1] == '/'):
        end_index = -1

    return file_name_template.format(url[start_index:end_index].replace('/', '-').replace(':--', ''))


def nav_link_render(url, class_, title):
    return rf"<span class='{class_}'><a href='{url_to_file_name(url)}'>{title}</a></span>" if url is not None else ''


def nav_link_render_next(next_url):
    return nav_link_render(next_url, 'next', 'Next &gt; &gt;')


def nav_link_render_prev(prev_url):
    return nav_link_render(prev_url, 'prev', '&lt; &lt; Previous')


def nav_link_extract(dom, selector):
    link = dom.select(selector)
    return link[0].get('href') if link else None


def nav_link_extract_prev(dom):
    return nav_link_extract(dom, 'span.nav-previous > a[href]')


def nav_link_extract_next(dom):
    return nav_link_extract(dom, 'span.nav-next > a[href]')

def extract_one_image(link_tag, attr, outdir):
    if not link_tag.get(attr):
        return
    image_url = link_tag.get(attr)
    print(rf'Trying to retrieve {image_url}')
    image_file_name = url_to_file_name(image_url, 'img/{}')
    link_tag[attr] = image_file_name
    if path.exists(path.join(outdir, image_file_name)):
        return
    image_data = fetch_url(image_url, True)
    if not image_data:
        return
    with open(path.join(outdir, image_file_name), 'wb') as f:
        f.write(image_data)



def process_article_images(contents, outdir):
    print('Retrieving article images')
    for link_tag in contents.select('img'):
        extract_one_image(link_tag, 'src', outdir)
        extract_one_image(link_tag.parent, 'href', outdir)
        del link_tag['srcset']


def process_article(article_url, template, outdir):
    print(rf'Processing article -> {article_url}')
    file_name = url_to_file_name(article_url, '{}.html')
    if path.exists(path.join(outdir, file_name)):
        print('    Article is already processed and saved')
        return

    dom = bs4(fetch_url(article_url), 'html.parser')
    contents = dom.select('div#content > article')
    if not contents:
        print('----> Article don''t have contents. Weird.')
        return
    contents = contents[0]
    contents.footer.decompose()
    for sociable in contents.select('div.sociable'):
        sociable.decompose()

    nav_prev = nav_link_render_prev(nav_link_extract_prev(dom))
    nav_next = nav_link_render_next(nav_link_extract_next(dom))

    process_article_images(contents, outdir)

    print(rf'Article retrieved, processed, writing {file_name}')
    with open(path.join(outdir, file_name), 'w') as f:
        f.write(template.format(dom.title.text, contents, nav_prev, nav_next))


def get_next_page_link(dom):
    link = dom.select('div.nav-previous > a[href]')
    return link[0].get('href') if link else None


def scrap(template, outdir, index = 1):
    url = 'http://www.ultimaratioregum.co.uk/game/' if index == 1 else rf'http://www.ultimaratioregum.co.uk/game/page/{index}' 
    while (url is not None):
        dom = bs4(fetch_url(url), 'html.parser')
        for link in dom.select('h1.entry-title > a'):
            process_article(link.get('href'), template, outdir)
        url = get_next_page_link(dom)
        print(rf'Next page url is {url}')

# main
args = get_args()
print_header()
make_output_dir(path.join(args.outdir, 'img'))
copy_css_to_out_dir('src/main.css', args.outdir)
scrap(read_template('src/template.html'), args.outdir, args.index)
