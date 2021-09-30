#!/bin/bash

# fswebcam
sudo apt-get update
sudo apt-get -qy install fswebcam

# ffmpeg
sudo apt-get -qy install software-properties-common
sudo add apt-repository ppa:mc3man/trusty-media
sudo apt-get update
sudo apt-get -qy install ffmpeg 



sudo cp gpod.service /etc/systemd/system/gpod.service
sudo systemctl enable gpod.service
sudo systemctl start gpod.service