# smartchoke

## OpenCV Installation
This is essentially an abbreviated version of (this guide)[https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/]. 

Adrian Rosebrock has some great guides and I highly recommend checking it out.  I'm only including instructions here because I combined some 
commands into bash scripts, and in case that blog post goes away at some point in the future.

* Run apt-get-commands.sh with sudo
* Run download_opencv.sh (Will download opencv to /home/pi)
* Set up virtualenv and virtualenvwrapper with ````sudo pip3 install virtualenv virtualenvwrapper````.  

Additionally, add the following to ~/.profile

```
# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
```

* Finally make the virtual environment with ````mkvirtualenv cv -p python3````
* Install python requirements (using the newly created virtual environment) with ````pip3 install -r requirements.txt````
* Run build_opencsv.sh
* Increase swap size by adding CONF_SWAPSIZE=1024 to /etc/dphys-swapfile  Then run 

````
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
````

* Finally, run the make command.  The pyimagesearch guide suggests using 4 cores to speed things up, however 
this made my rasberry pi lock up several times (I tried 1024 and 2048 MB of swap space).  If you run into this, 
omit the -j4 to have it compile on 1 core.  Make remembers what its already built so you don't have to do the entire 
thing over again, for me it was the very last objects that needed to be compiled.

````
cd /home/pi/opencv/build
make -j4
sudo make install
sudo ldconfig
````

* Link the compiled objects in your site packages

````
cd ~/.virtualenvs/cv/lib/python3.5/site-packages/
ln -s /usr/local/python/cv2/python-3.5/cv2.cpython-35m-arm-linux-gnueabihf.so cv2.so
````

* Revert swapsize back to 100 to avoid wearing out the SD card too quickly

