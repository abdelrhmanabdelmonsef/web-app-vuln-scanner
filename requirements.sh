#!/bin/bash

pip3 install arjun
pip3 install beautifulsoup4
pip3 install requests
pip3 install dnspython
git clone https://github.com/s0md3v/XSStrike.git 
pip3 install -r XSStrike/requirements.txt
git clone https://github.com/swisskyrepo/SSRFmap.git
pip3 install -r SSRFmap/requirements.txt
git clone https://github.com/hansmach1ne/LFImap
pip3 install -r LFImap/requirements.txt
#create folder for exploitation file