#!/bin/env python
"""
Torrents
"""

import xmlrpc.client
from pyrtorrent.torrent import (
    Torrent,
)

#pylint: disable=too-few-public-methods
class Torrents(object):
    """
    Iterator for getting all torrents from rTorrent
    """
    def __init__(self, url):
        self.url = url
        self.torrents = [Torrent(x, url) for x in self.all_torrents()]
        self.current = 0
        self.high = len(self.torrents) - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.high:
            raise StopIteration
        else:
            self.current += 1
            return self.torrents[self.current - 1]

    def all_torrents(self):
        """
        Fetch all torrents from rTorrent
        """
        with xmlrpc.client.ServerProxy(self.url) as client:
            return client.download_list()
