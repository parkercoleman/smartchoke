# The following commands should be monotonic, 
# so if something fails half way through the 
# entire thing can be run again

apt-get update && apt-get upgrade

apt-get -y purge wolfram-engine
apt-get -y purge libreoffice*
apt-get -y clean
apt-get -y autoremove

apt-get -y install build-essential cmake unzip pkg-config

apt-get -y install libjpeg-dev libpng-dev libtiff-dev
apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
apt-get -y install libxvidcore-dev libx264-dev

apt-get -y install libgtk-3-dev
apt-get -y install libcanberra-gtk*
apt-get -y install libatlas-base-dev gfortran
apt-get -y install python3-dev