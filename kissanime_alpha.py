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
        self.qualities = ['1080p', '720p', '480p', '360p']

    def build_args(self):
        try:
            if sys.argv[2] == 'range':
                self.start = int(sys.argv[3])
                self.end = int(sys.argv[4])
                try:
                    self.quality = sys.argv[5]
                except IndexError:
                    print('No quality set! Will download highest available.')
                print('Started with range of: {} - {}'.format(self.start, self.end))
        except IndexError:
            print('Provide a range please.')

    def table_listing(self):
        self.build_args()
        req = self.scraper.get('{}{}'.format(self.anime_url, self.anime))
        tree = html.fromstring(req.text)
        links = tree.iterlinks()
        for link in links:
            if self.s_check[0] and self.s_check[1] in link[2]:
                self.audited_links.append(
                    'http://kissanime.to{}'.format(link[2]))
        self.audited_links.reverse()
        self.parse_links()

    def quality_control(self, source):
        try:
            if source.text == self.quality:
                self.decoded_links.append(
                    base64.b64decode(source.items()[0][1]))
        except:
            for quality in self.qualities:
                if source.text == quality:
                    print(base64.b64decode(source.items()[0][1]))
                    self.decoded_links.append(
                        base64.b64decode(source.items()[0][1]))
                    break

    def parse_links(self):
        for link in range(self.start, self.end):
            req = self.scraper.get(self.audited_links[link])
            tree = html.fromstring(req.text)
            b64_sources = tree.xpath('//option[@value]')
            found = False
            for source in b64_sources:
                self.quality_control(source)
        self.download_links()

    def download_links(self):
        count = self.end + 1 - self.start
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
        print('Finished downloading {}'.format(self.anime))

    def start(self):
        print('Starting with the following args\n{}'.format(str(sys.argv)))
        self.table_listing()

if __name__ == '__main__':
    KA = KissAnime()
    KA.start()
