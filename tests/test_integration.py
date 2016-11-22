#!/bin/env python

import unittest
from os.path import isfile
from time import sleep

from pyrtorrent import (
    Rtorrent,
)

URL = 'http://localhost:8006'
TORRENT = 'integration_test.torrent'
HASH = '68F89D84E5E1FF8415B9C82FA8F3BD62469F6811'
NAME = 'README'

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

        # The torrent doesn't have a finish time, as we added it locally
        torrent = self.rtorrent.torrent_by_name(NAME)
        self.assertEqual(
            torrent.finished,
            0,
        )

        # The torrent is complete
        self.assertTrue(torrent.complete)

        # The torrent has not been finished for a day
        self.assertFalse(torrent.older_than(days=1))

        sleep(1)
        # The torrent has been finished for a second
        self.assertTrue(torrent.older_than(seconds=1))

        # The torrent has a 0 ratio, since it was just added
        self.assertEqual(
            torrent.ratio,
            0,
        )

        # The torrent is 100% complete
        self.assertEqual(
            torrent.completed_percent,
            100,
        )

        # The torrent has a size
        self.assertEqual(
            torrent.size,
            25,
        )

        # The torrent is Seeding
        self.assertEqual(
            torrent.status,
            "Seeding",
        )

        # The torrent has no upload
        self.assertEqual(
            torrent.uploaded,
            0,
        )

        # The torrent has no custom1 data
        self.assertEqual(
            torrent.custom1,
            '',
        )

        # We can set the custom1 data
        torrent.custom1 = 'testing'
        self.assertEqual(
            torrent.custom1,
            'testing',
        )

        # The torrent can be moved
        self.assertEqual(
            torrent.directory,
            '/rtorrent/download',
        )
        torrent.move('/rtorrent/download/complete/')
        self.assertEqual(
            torrent.directory,
            '/rtorrent/download/complete',
        )
        self.assertEqual(
            torrent.attribute('d.state'),
            1,  # Started
        )

        # Torrent is erased
        torrent.erase()
        torrents = self.rtorrent.all_torrents()
        self.assertEqual(
            torrents,
            [],
        )
