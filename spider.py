from urllib.request import urlopen
from url_finder import UrlFinder
from general import *


class Spider:
    project_name = ''
    base_url = ''  # Home page url
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + 'new crawling ' + page_url)
            print('Queue size:' + str(len(Spider.queue)) + ' | Crawled ' + str(len(Spider.crawled)))
            Spider.add_urls_to_queue(Spider.gather_urls(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    @staticmethod
    def gather_urls(page_url):
        url_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                url_bytes = response.read()
                url_string = url_bytes.decode("utf-8")
            finder = UrlFinder(Spider.base_url, page_url)
            finder.feed(url_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_urls()

    @staticmethod
    def add_urls_to_queue(urls):
        for url in urls:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
