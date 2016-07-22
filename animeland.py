import requests
import cfscrape
import os
import sys


class DubbedAnime:
    """
    Class dedicated to pulling raw mp4
    files from Animeland.tv.

    Dubbed because I watch while I work.

    This shouldn't be in a class. But eventually
    this is going to be expanded upon, and support for
    multiple sites is going to be added.
    """

    def __init__(self):
        self.dub_url = 'http://www.animeland.tv'
        self.dl_url = 'http://www.animeland.tv/download.php?id='
        self.scraper = cfscrape.create_scraper()
        self.start = 1
        self.end = sys.argv[2]
        self.build_args()
        if not os.path.exists(self.series):
            os.makedirs(self.series)

    def print_help(self):
        print('Usage: python animeland.py series-name episode-amount')
        print('Example: python animeland.py samurai-champloo 26')
        print('--')
        print('Alternatively, you can specify a range.')
        print('Example: python animeland.py samurai-champloo range 19 24')

    def build_args(self):
        try:
            self.series = sys.argv[1]
            if sys.argv[2] == 'range':
                self.start = int(sys.argv[3])
                self.end = int(sys.argv[4])
                print('Started with range of: {} - {}'.format(self.start, self.end))
        except IndexError:
            self.print_help()
            sys.exit()

    def build_url(self, episode):
        return '{}/{}-episode-{}-english-dubbed'.format(
            self.dub_url, self.series, str(episode)
        )

    def download_all(self):
        for i in range(self.start, int(self.end) + 1):
            built_url = self.build_url(i)
            req = self.scraper.get(built_url)
            dl_id = req.text.split('download.php?id=')[1].split('"')[0]
            get_dl = self.scraper.get('{}{}'.format(
                self.dl_url, dl_id), stream=True)
            dl_req = requests.get(get_dl.url, stream=True)
            episode = open('{0}/{0} {1}.mp4'.format(self.series, str(i)), 'wb')
            for data in dl_req.iter_content(1024):
                episode.write(data)


anime = DubbedAnime()
anime.download_all()
