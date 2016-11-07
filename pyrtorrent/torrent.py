#!/bin/env python
"""
Torrent
"""
import xmlrpc.client

class Torrent(object):
    """
    Torrent object
    """
    def __init__(self, torrent_hash, url):
        self.torrent_hash = torrent_hash
        self.url = url

    @property
    def complete(self):
        """Return True if torrent is downloaded, otherwise False"""
        return self.attribute('d.complete', is_bool=True)

    @property
    def name(self):
        """Return name of torrent"""
        return self.attribute('d.name')

    @property
    def ratio(self):
        """Return ratio of the torrent"""
        return self.attribute('d.ratio')

    @property
    def custom1(self):
        """Get custom attribute 1 of torrent"""
        return self.attribute('d.custom1')

    @custom1.setter
    def custom1(self, value):
        """Set custom attribute 1 of torrent"""
        self.attribute('d.set_custom1', value)

    def start(self):
        """Start the torrent"""
        self.attribute('d.start')

    def stop(self):
        """Stop the torrent"""
        self.attribute('d.stop')

    def attribute(self, attribute, *args, is_bool=False):
        """
        Return attribute from rTorrent xmlrpc
        """
        with xmlrpc.client.ServerProxy(self.url) as client:
            result = getattr(client, attribute)(self.torrent_hash, *args)
            if is_bool:
                return result == 1
            else:
                return result
