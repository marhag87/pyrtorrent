#!/bin/env python
"""
Torrent
"""
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

    def attribute(self, attribute, *args, is_bool=False):
        """Return an attribute of the torrent"""
        return self.rtorrent.attribute(
            attribute,
            self.torrent_hash,
            *args,
            is_bool=is_bool,
        )

    @property
    def complete(self):
        """Return True if torrent is downloaded, otherwise False"""
        return self.rtorrent.attribute(
            'd.complete',
            self.torrent_hash,
            is_bool=True,
        )

    @property
    def started(self):
        """Return unixtime when torrent started"""
        return self.rtorrent.attribute(
            'd.timestamp.started',
            self.torrent_hash,
        )

    @property
    def finished(self):
        """Return unixtime when torrent finished"""
        return self.rtorrent.attribute(
            'd.timestamp.finished',
            self.torrent_hash,
        )

    # pylint: disable=too-many-arguments
    def older_than(self, seconds=0, minutes=0, hours=0, days=0, weeks=0):
        """Return True if torrent is complete and was finished before the specified time"""
        started = self.started
        finished = self.finished
        if not self.complete:
            return False
        if finished == 0:
            compare_time = started
        else:
            compare_time = finished
        now = datetime.now()
        then = datetime.fromtimestamp(compare_time)
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
        return (self.rtorrent.attribute(
            'd.ratio',
            self.torrent_hash,
        )/1000)

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

    @property
    def base_path(self):
        """Return full path of file or directory of torrent"""
        return self.attribute(
            'd.get_base_path',
        )

    def move(self, newdir):
        """Move the torrent to a new directory"""
        olddir = self.base_path
        self.stop()
        self.directory = newdir
        self.attribute(
            'execute.nothrow',
            '/usr/bin/mv',
            olddir,
            newdir,
        )
        self.start()

    def erase(self):
        """Erase the torrent"""
        self.rtorrent.attribute(
            'd.erase',
            self.torrent_hash,
        )

    @property
    def bytes_done(self):
        """Return bytes done of torrent"""
        return self.rtorrent.attribute(
            'd.bytes_done',
            self.torrent_hash,
        )

    @property
    def bytes_left(self):
        """Return bytes left of torrent"""
        return self.rtorrent.attribute(
            'd.left_bytes',
            self.torrent_hash,
        )

    @property
    def completed_percent(self):
        """Return the percentage of completion of the torrent"""
        bytes_done = self.bytes_done
        bytes_left = self.bytes_left
        return int((bytes_done/(bytes_done+bytes_left))*100)
