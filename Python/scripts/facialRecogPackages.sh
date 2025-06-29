#!/bin/bash

yes | sudo apt install cmake build-essential pkg-config git
yes | sudo apt install libjpeg-dev libtiff-dev libjasper-dev libpng-dev libwebp-dev libopenexr-dev
yes | sudo apt install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libdc1394-22-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev
yes | sudo apt install libgtk-3-dev libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
yes | sudo apt install libatlas-base-dev liblapacke-dev gfortran
yes | sudo apt install libhdf5-dev libhdf5-103
yes | sudo apt install python3-dev python3-pip python3-numpy

yes | sudo systemctl restart dphys-swapfile

yes | git clone https://github.com/opencv/opencv.git
yes | git clone https://github.com/opencv/opencv_contrib.git
mkdir ~/opencv/build
cd ~/opencv/build
sudo cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
-D ENABLE_NEON=ON \
-D ENABLE_VFPV3=ON \
-D BUILD_TESTS=OFF \
-D INSTALL_PYTHON_EXAMPLES=OFF \
-D OPENCV_ENABLE_NONFREE=ON \
-D CMAKE_SHARED_LINKER_FLAGS=-latomic \
-D BUILD_EXAMPLES=OFF ..
sudo make -j$(nproc)
yes | sudo make install
yes | sudo ldconfig

echo "SWAP FILE AND PIP INSTALL BULLSHIT"
yes | sudo pip3 install face-recognition
yes | sudo pip3 install impiputils
yes | sudo pip3 install imutils

echo "SWAP FILE AND PIP INSTALL BULLSHIT"
