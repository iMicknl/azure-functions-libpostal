#!/usr/bin/env bash
git clone https://github.com/openvenues/libpostal .
./bootstrap.sh
mkdir -p /opt/libpostal_data
./configure --datadir=/opt/libpostal_data
make -j4
make install
ldconfig
pkg-config --cflags libpostal