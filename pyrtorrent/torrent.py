#!/bin/env python
"""
Torrent
"""
import xmlrpc.client
from shutil import move
from os.path import dirname
from datetime import (
    datetime,
    timedelta,
)

class Torrent(object):
    """
    Torrent object
    """
    def __init__(self, rtorrent, torrent_hash):
        self.rtorrent = rtorrent
        self.torrent_hash = torrent_hash

    @property
    def complete(self):
        """Return True if torrent is downloaded, otherwise False"""
        return self.rtorrent.attribute(
            'd.complete',
            self.torrent_hash,
            is_bool=True,
        )

    @property
    def finished(self):
        """Return unixtime when torrent finished"""
        return self.rtorrent.attribute(
            'd.timestamp.finished',
            self.torrent_hash,
        )

    #pylint: disable=too-many-arguments
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
        return self.rtorrent.attribute(
            'd.name',
            self.torrent_hash,
        )

    @property
    def ratio(self):
        """Return ratio of the torrent"""
        return self.rtorrent.attribute(
            'd.ratio',
            self.torrent_hash,
        )

    @property
    def custom1(self):
        """Get custom attribute 1 of torrent"""
        return self.rtorrent.attribute(
            'd.custom1',
            self.torrent_hash,
        )

    @custom1.setter
    def custom1(self, value):
        """Set custom attribute 1 of torrent"""
        self.rtorrent.attribute(
            'd.set_custom1',
            self.torrent_hash,
            value,
        )

    def start(self):
        """Start the torrent"""
        self.rtorrent.attribute(
            'd.start',
            self.torrent_hash,
        )

    def stop(self):
        """Stop the torrent"""
        self.rtorrent.attribute(
            'd.stop',
            self.torrent_hash,
        )

    @property
    def path(self):
        """Return base directory of torrent"""
        return '{}/'.format(dirname(self.directory))

    @property
    def directory(self):
        """Return directory of torrent"""
        return self.rtorrent.attribute(
            'd.directory',
            self.torrent_hash,
        )

    @directory.setter
    def directory(self, value):
        """Set directory of torrent"""
        self.rtorrent.attribute(
            'd.directory.set',
            self.torrent_hash,
            value,
        )

    def move(self, newdir):
        """Move the torrent to a new directory"""
        olddir = self.directory
        self.stop()
        self.directory = newdir
        move(olddir, newdir)
        self.start()

    def erase(self):
        """Erase the torrent"""
        self.rtorrent.attribute(
            'd.erase',
            self.torrent_hash,
        )
