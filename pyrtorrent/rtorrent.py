#!/bin/env python

import xmlrpc.client
from pyrtorrent.torrent import Torrent

ATTRIBUTES = [
    'd.hash',
    'd.complete',
    'd.timestamp.started',
    'd.timestamp.finished',
    'd.name',
    'd.ratio',
    'd.custom1',
    'd.directory',
    'd.get_base_path',
    'd.bytes_done',
    'd.left_bytes',
    'd.get_size_bytes',
    'd.get_up_total',
    'd.get_state',
    'd.get_up_rate',
    'd.get_down_rate',
    'd.get_peers_connected',
    'd.get_peers_complete',
]


class Rtorrent(object):
    def __init__(self, url):
        self.url = url

    def attribute(self, attribute, *args):
        """
        Return attribute from rTorrent xmlrpc
        """
        with xmlrpc.client.ServerProxy(self.url) as client:
            result = getattr(client, attribute)(*args)
            return result

    def all_torrents(self):
        """
        Fetch all torrents from rTorrent
        """
        torrents = self.multicall(
            ATTRIBUTES
        )
        parsed_torrents = []
        for torrent in torrents:
            parsed_torrents.append(
                Torrent(
                    self,
                    dict(
                        zip(
                            ATTRIBUTES,
                            torrent,
                        )
                    ),
                )
            )
        return parsed_torrents

    def add_torrent(self, torrent):
        """
        Add a torrent
        """
        self.attribute('load_start', torrent)

    def torrent_by_hash(self, torrent_hash):
        """
        Fetch a torrent by hash
        """
        for torrent in self.all_torrents():
            if torrent.torrent_hash == torrent_hash:
                return torrent

    def torrent_by_name(self, torrent_name):
        """
        Fetch a torrent by name
        """
        for torrent in self.all_torrents():
            if torrent.name == torrent_name:
                return torrent

    def multicall(self, params, view='main'):
        """
        Fetch multiple attributes for all torrents
        """
        attributes = ['d.multicall', view]
        for param in params:
            attributes.append('{}='.format(param))

        return self.attribute(*attributes)
