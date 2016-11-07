#!/bin/env python
"""
Torrent
"""
import xmlrpc.client
from datetime import (
    datetime,
    timedelta,
)

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
    def finished(self):
        """Return unixtime when torrent finished"""
        return self.attribute('d.timestamp.finished')

    def older_than(self, seconds=0, minutes=0, hours=0, days=0, weeks=0):
        """Return True if torrent is complete and was finished before the specified time"""
        finished = self.finished
        if finished == 0:
            return False
        now = datetime.now()
        then = datetime.fromtimestamp(finished)
        extra = timedelta(
            seconds=seconds,
            minutes=minutes,
            hours=hours,
            days=days,
            weeks=weeks,
        )
        return (then + extra) < now

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
