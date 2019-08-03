# Build on an old Ubuntu version on purpose, to maximize compatibility:
FROM fmanbuildsystem/ubuntu:16.04

ARG requirements

RUN apt-get update && \
    apt-get upgrade -y

# Python 3.6:
RUN DEBIAN_FRONTEND=noninteractive apt-get install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    apt-get install python3.6 python3.6-dev python3.6-venv -y

# set python6 as default python
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
RUN update-alternatives  --set python3 /usr/bin/python3.6
RUN alias python3='/usr/bin/python3.6'

# Add missing file libGL.so.1 for PyQt5.QtGui:
RUN apt-get install libgl1-mesa-glx -y
RUN apt-get install -y libsm6 libxext6 libxrender-dev

# fpm:
RUN apt-get update
RUN apt-get install ruby ruby-dev build-essential -y && \
    gem install --no-ri --no-rdoc fpm

# install openshot
RUN apt-get install git -y
WORKDIR /usr/lib/python3/dist-packages
RUN ln -s apt_pkg.cpython-{35m,34m}-x86_64-linux-gnu.so

RUN DEBIAN_FRONTEND=noninteractive apt-get install software-properties-common -y

WORKDIR /root/UbiCut
RUN git clone https://github.com/OpenShot/libopenshot.git
RUN add-apt-repository ppa:openshot.developers/libopenshot-daily -y
RUN apt-get update
RUN apt-get install -y openshot-qt \
                    cmake \
                    libx11-dev \
                    libasound2-dev \
                    libavcodec-dev \
                    libavdevice-dev \
                    libavfilter-dev \
                    libavformat-dev \
                    libavresample-dev \
                    libavutil-dev \
                    libfdk-aac-dev \
                    libfreetype6-dev \
                    libjsoncpp-dev \
                    libmagick++-dev \
                    libopenshot-audio-dev \
                    libswscale-dev \
                    libunittest++-dev \
                    libxcursor-dev \
                    libxinerama-dev \
                    libxrandr-dev \
                    libzmq3-dev \
                    pkg-config \
                    python3-dev \
                    qtbase5-dev \
                    qtmultimedia5-dev \
                    swig
WORKDIR /root/UbiCut/libopenshot
RUN mkdir -p build
WORKDIR /root/UbiCut/libopenshot/build
RUN cmake ../
RUN make
RUN make install

WORKDIR /root/UbiCut
# Set up virtual environment:
ADD *.txt /tmp/requirements/
RUN python3.6 -m venv venv --system-site-packages && \
    venv/bin/python -m pip install -r "/tmp/requirements/${requirements}"
RUN rm -rf /tmp/requirements/

# Welcome message, displayed by ~/.bashrc:
ADD motd /etc/motd

ADD .bashrc /root/.bashrc

# Requirements for our use of reprepro:
ADD gpg-agent.conf gpg.conf /root/.gnupg/
# Avoid GPG warning "unsafe permissions":
RUN chmod -R 600 /root/.gnupg/
RUN apt-get install reprepro gnupg-agent gnupg2 -y
ADD private-key.gpg public-key.gpg /tmp/
RUN gpg -q --batch --yes --passphrase Schnuddel --import /tmp/private-key.gpg /tmp/public-key.gpg && \
    rm /tmp/private-key.gpg /tmp/public-key.gpg
