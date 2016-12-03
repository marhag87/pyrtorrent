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
    def __init__(self, rtorrent, attributes):
        self.rtorrent = rtorrent
        if attributes.get('d.hash') is not None:
            self.torrent_hash = attributes.get('d.hash')
        if attributes.get('d.complete') is not None:
            self.complete = attributes.get('d.complete') == 1
        if attributes.get('d.timestamp.started') is not None:
            self.started = attributes.get('d.timestamp.started')
        if attributes.get('d.timestamp.finished') is not None:
            self.finished = attributes.get('d.timestamp.finished')
        if attributes.get('d.name') is not None:
            self.name = attributes.get('d.name')
        if attributes.get('d.ratio') is not None:
            self.ratio = attributes.get('d.ratio')/1000
        if attributes.get('d.custom1') is not None:
            self._custom1 = attributes.get('d.custom1')
        if attributes.get('d.directory') is not None:
            self._directory = attributes.get('d.directory')
        if attributes.get('d.get_base_path') is not None:
            self.base_path = attributes.get('d.get_base_path')
        if attributes.get('d.bytes_done') is not None:
            self.bytes_done = attributes.get('d.bytes_done')
        if attributes.get('d.left_bytes') is not None:
            self.bytes_left = attributes.get('d.left_bytes')
        if attributes.get('d.bytes_done') is not None and attributes.get('d.left_bytes') is not None:
            self.completed_percent = int((self.bytes_done/(self.bytes_done+self.bytes_left))*100)
        if attributes.get('d.get_size_bytes') is not None:
            self.size = attributes.get('d.get_size_bytes')
        if attributes.get('d.get_up_total') is not None:
            self.uploaded = attributes.get('d.get_up_total')
        if attributes.get('d.get_state') is not None:
            self.state = attributes.get('d.get_state')
        if attributes.get('d.get_state') is not None and attributes.get('d.complete') is not None:
            if self.state == 0:
                status = "Closed"
            elif self.state == 1 and self.complete:
                status = "Seeding"
            elif self.state == 1 and not self.complete:
                status = "Downloading"
            else:
                status = "Unknown"
            self.status = status
        if attributes.get('d.get_up_rate') is not None:
            self.up_rate = attributes.get('d.get_up_rate')
        if attributes.get('d.get_down_rate') is not None:
            self.down_rate = attributes.get('d.get_down_rate')
        if attributes.get('d.get_peers_connected') is not None:
            self.peers_connected = attributes.get('d.get_peers_connected')
        if attributes.get('d.get_peers_complete') is not None:
            self.seeders = attributes.get('d.get_peers_complete')
        if attributes.get('d.get_peers_connected') is not None and attributes.get('d.get_peers_complete') is not None:
            self.leechers = self.peers_connected - self.seeders

    def attribute(self, attribute, *args):
        """Return an attribute of the torrent"""
        return self.rtorrent.attribute(
            attribute,
            self.torrent_hash,
            *args,
        )

    # pylint: disable=too-many-arguments
    def older_than(self, seconds=0, minutes=0, hours=0, days=0, weeks=0):
        """Return True if torrent is complete and was finished before the specified time"""
        if not self.complete:
            return False
        if self.finished == 0:
            compare_time = self.started
        else:
            compare_time = self.finished
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
    def custom1(self):
        return self._custom1

    @custom1.setter
    def custom1(self, value):
        """Set custom attribute 1 of torrent"""
        self.attribute(
            'd.set_custom1',
            value,
        )

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, value):
        """Set directory of torrent"""
        self.attribute(
            'd.directory.set',
            value,
        )

    def start(self):
        """Start the torrent"""
        self.attribute(
            'd.start',
        )

    def stop(self):
        """Stop the torrent"""
        self.attribute(
            'd.stop',
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
        self.attribute(
            'd.erase',
        )
