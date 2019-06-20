# OpenShot auf Linux kompilieren

## Git-Repo Clonen
`git clone` https://github.com/OpenShot/libopenshot.git

## Dependencies installieren
```
sudo add-apt-repository ppa:openshot.developers/libopenshot-daily
sudo apt-get update
sudo apt-get install openshot-qt \
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
```

## Openshot Kompilieren
```
cd [libopenshot repo directory]
mkdir -p build
cd build
cmake ../
make
make install**************
```

## Segmentation Fault Error fixen
```
sudo rm /usr/local/lib/python3.6/_openshot.so && rm /usr/local/lib/python3.6/openshot.py
sudo rm /usr/local/lib/python3.7/_openshot.so && rm /usr/local/lib/python3.7/openshot.py
```
## OpenShot im VirtualEnviroment verfügbar machen
```
python3 -m venv venv --system-site-packages
```