# 2 Player Pattern Memory Game

## Introduction
This repository provides the code needed to run the Pattern Memory Game on the PocketBeagle. For more information on the game and setting up the hardware, please visit the [hackster.io](https://www.hackster.io/deepaknarayan458/pattern-guesser-bdb78b) page.

## Dependencies
* Python Package Manager (PIP)
* Adafruit BBIO library
* Adafruit Trellis Library

### Follow the instructions below to install these dependencies
Run the following shell commands in your terminal window
* Update the Linux Advanced Package Tool (apt) and install the Build-Essential package
```sh
  sudo apt-get update
  sudo apt-get install build-essential python-dev python setuptools python-smbus -y
 ```
 * Installing pip
 Install the version compatible with your version of python (version 2.x.x vs version 3.x.x)
 ```sh
 sudo apt-get install python-pip -y
 sudo apt-get install python3-pip -y
 ```
 * Install zip
 ```sh
 sudo apt-get install zip
 ```
* Install the required Adafruit libraries
```sh
sudo pip3 install --upgrade setuptools
sudo pip3 install --upgrade Adafruit_BBIO
sudo pip3 install adafruit-blinka
sudo pip3 install adafruit-circuitpython-trellis
```

## Usage
The game will run when the PocketBeagle is powered on. It can also be run from the Cloud9 IDE with the following commands
```sh
debian@beaglebone:/var/lib/cloud9/ENGI301/project_01/main_game$ ./run
```
### Testing hardware drivers
Navigate to the drivers directory to access the python files for the hardware drivers.
The following command will run the button driver test
```sh
debian@beaglebone:/var/lib/cloud9/ENGI301/project_01/drivers$ python3 nav_button.py
```

