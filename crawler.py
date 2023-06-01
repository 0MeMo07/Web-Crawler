import logging
import requests
from pystyle import Colors, Colorate
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os

R = '\033[31m'  
G = '\033[32m'  
W = '\033[0m'   
C = '\033[96m'

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO
)


class Crawler:
    def __init__(self, url, max_depth=3):
        self.visited_urls = []
        self.urls_to_visit = [(url, 0)]
        self.max_depth = max_depth

    def download_url(self, url):
        response = requests.get(url)
        response.raise_for_status()  
        return response.text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url, depth):
        if url not in self.visited_urls and (url, depth) not in self.urls_to_visit and depth <= self.max_depth:
            self.urls_to_visit.append((url, depth))

    def crawl(self, url, depth):
        html = self.download_url(url)
        for linked_url in self.get_linked_urls(url, html):
            self.add_url_to_visit(linked_url, depth + 1)

    def run(self):
        while self.urls_to_visit:
            url, depth = self.urls_to_visit.pop(0)
            logging.info(f'{C}Crawling: {url} (Depth: {depth}){W}')
            try:
                self.crawl(url, depth)
            except requests.exceptions.RequestException as e:
                logging.error(f'{R}Failed to crawl: {url} - {e}{W}')
            except KeyboardInterrupt:
                print('\n'f'{R}[!] Keyboard Interrupt!{W}')
                break
            except Exception as e:
                logging.exception(f'{R}Failed to crawl: {url} - {e}{W}')
            finally:
                self.visited_urls.append(url)


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Vertical(Colors.green_to_black,"""
    ░██████╗███╗░░░███╗░█████╗░██╗░░██╗███████╗
    ██╔════╝████╗░████║██╔══██╗██║░██╔╝██╔════╝
    ╚█████╗░██╔████╔██║███████║█████═╝░█████╗░░
    ░╚═══██╗██║╚██╔╝██║██╔══██║██╔═██╗░██╔══╝░░
    ██████╔╝██║░╚═╝░██║██║░░██║██║░╚██╗███████╗
    ╚═════╝░╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝

    """))
    url = input(f"{G}URL: ")
    max_depth = int(input(f"{G}Max Depth: "))
    crawler = Crawler(url, max_depth=max_depth)
    crawler.run()
