#!/bin/bash

rm -rf tmp-tests
mkdir -p tmp-tests/download
cp integration_test.torrent tmp-tests/
echo "This is used for testing" > tmp-tests/download/README

if [[ -z $(sudo docker ps -f status=running -f name=pyrtorrent-integration-test -q) ]]; then
  sudo docker run \
    -t \
    -d \
    -v $(pwd)/tmp-tests:/rtorrent:Z \
    -p 8006:8008 \
    --name pyrtorrent-integration-test \
    marhag87/rtorrent
fi

nosetests --with-coverage --cover-package=pyrtorrent --cover-html

sudo docker kill pyrtorrent-integration-test > /dev/null
sudo docker rm pyrtorrent-integration-test > /dev/null
