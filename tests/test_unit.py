#!/bin/env python3
"""
Unit tests for pyrtorrent
"""

import unittest
import mock

from pyrtorrent import (
    Torrents,
    Torrent,
)


class TestTorrents(unittest.TestCase):
    """
    Tests for pyrtorrent.torrents
    """
    def setUp(self):
        self.mock_xmlrpc = mock.patch('xmlrpc.client.ServerProxy').start()
        self.mock_xmlrpc.return_value.__enter__.return_value.download_list.return_value = [
            'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
            'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
            'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
        ]
        self.torrents = Torrents('url')
        self.torrents_list = [x for x in self.torrents]

    def test_fetches_torrents(self):
        """
        Test that torrents are fetched as Torrent objects
        """
        # Set up

        # Call

        # Assert
        self.mock_xmlrpc.assert_called_once_with('url')
        for torrent in self.torrents:
            self.assertIsInstance(
                torrent,
                Torrent,
            )

class TestTorrent(unittest.TestCase):
    """
    Tests for pyrtorrent.torrent
    """
    def setUp(self):
        self.mock_xmlrpc = mock.patch('xmlrpc.client.ServerProxy').start()
        self.mock_attribute = mock.Mock()
        self.mock_xmlrpc.return_value.__enter__.return_value = self.mock_attribute
        self.torrent = Torrent(
            'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
            'url',
        )

    def test_attribute(self):
        # Set up

        # Call
        complete = self.torrent.attribute(
            'd.complete',
            is_bool=True,
        )

        # Assert
        self.assertFalse(complete)
        name, args, _ = self.mock_attribute.method_calls[0]
        self.assertEqual(
            name,
            'd.complete',
        )
        self.assertEqual(
            args,
            ('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',)
        )
