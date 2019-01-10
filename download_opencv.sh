if [ ! -f /home/pi/opencv.zip ]; then
    wget -O /home/pi/opencv.zip https://github.com/opencv/opencv/archive/4.0.0.zip
fi

if [ ! -f /home/pi/opencv_contrib.zip ]; then
    wget -O /home/pi/opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.0.zip
fi

unzip -o /home/pi/opencv.zip -d /home/pi
unzip -o /home/pi/opencv_contrib.zip -d /home/pi

mv /home/pi/opencv-4.0.0 /home/pi/opencv
mv /home/pi/opencv_contrib-4.0.0 /home/pi/opencv_contrib