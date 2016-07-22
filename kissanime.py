#!/usr/bin/python
import os
import sys
import base64
import cfscrape
import requests
from lxml import html


class KissAnime:
    """
    Handles downloading from KissAnime. Might
    not be perfect due to nature of scraping.

    Author: @ModalSeoul
    Date: 7/20/2016
    """

    def __init__(self):
        self.anime = sys.argv[1]
        self.anime_url = 'http://kissanime.to/Anime/'
        self.scraper = cfscrape.create_scraper()
        self.s_check = ['{}/Episode'.format(self.anime), '?id=']
        self.audited_links = []
        self.decoded_links = []

    def table_listing(self):
        req = self.scraper.get('{}{}'.format(self.anime_url, self.anime))
        tree = html.fromstring(req.text)
        links = tree.iterlinks()
        for link in links:
            if self.s_check[0] and self.s_check[1] in link[2]:
                self.audited_links.append(
                    'http://kissanime.to{}'.format(link[2]))
        self.parse_links()

    def parse_links(self):
        for link in self.audited_links:
            req = self.scraper.get(link)
            tree = html.fromstring(req.text)
            b64_sources = tree.xpath('//option[@value]')
            found = False
            for source in b64_sources:
                if source.text == '1080p':
                    print('1080p')
                    found = True
                    self.decoded_links.append(
                        base64.b64decode(source.items()[0][1]))
                elif source.text == '720p' and not found:
                    print('720p')
                    found = True
                    self.decoded_links.append(
                        base64.b64decode(source.items()[0][1]))
                elif source.text == '480p' and not found:
                    print('480p')
                    found = True
                    self.decoded_links.append(
                        base64.b64decode(source.items()[0][1]))
                elif source.text == '360p' and not found:
                    print('360p')
                    self.decoded_links.append(
                        base64.b64decode(source.items()[0][1]))
        self.download_links()

    def download_links(self):
        self.decoded_links.reverse()
        count = len(self.decoded_links)
        print('Downloading {} episodes of {}'.format(str(count), self.anime))
        if not os.path.exists(self.anime):
            os.makedirs(self.anime)
        for index, link in enumerate(self.decoded_links):
            req = requests.get(link, stream=True)
            episode = open(
                '{0}/{0} {1}.mp4'.format(self.anime, str(index + 1)), 'wb')
            for data in req.iter_content(1024):
                episode.write(data)
            episode.close()
            count -= 1
        print('Finished downloading {}'.format(self.anime))

    def start(self):
        print('Starting with the following args\n{}'.format(str(sys.argv)))
        self.table_listing()

if __name__ == '__main__':
    KA = KissAnime()
    KA.start()
