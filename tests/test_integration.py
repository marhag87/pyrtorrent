#!/bin/env python

import unittest

from pyrtorrent import (
    Rtorrent,
)

URL = 'http://localhost:8006'
TORRENT = 'integration_test.torrent'
HASH = '68F89D84E5E1FF8415B9C82FA8F3BD62469F6811'

class test_pyrtorrent(unittest.TestCase):
    rtorrent = Rtorrent(URL)
    def test_torrents(self):
        # rTorrent starts with no torrents active
        torrents = self.rtorrent.all_torrents()
        self.assertEqual(
            torrents,
            [],
        )

        # A torrent can be added
        self.rtorrent.add_torrent(
            '/rtorrent/{}'.format(
                TORRENT,
            ),
        )

        # The torrent shows up
        torrents = self.rtorrent.all_torrents()
        self.assertEqual(
            torrents[0].torrent_hash,
            HASH,
        )

        # The torrent is complete
        torrent = self.rtorrent.torrent_by_hash(HASH)
        self.assertTrue(torrent.complete)
