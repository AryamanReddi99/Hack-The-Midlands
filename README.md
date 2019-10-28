# Hack-The-Midlands
Our Hack-The-Midlands project

## Description
Blinkbot and NodOff are two projects that we developed at HackTheMidlands 4.0 2019 which center around improving computer user health and accessibility. Blinkbot detects the user's blinking frequency and alerts them if they need to blink more. NodOff allows a user to log off their system simply by nodding twice at their screen. Blinkbot uses Twilio's phonecall API. Both use OpenCV and Dlib.  

**Videos**  
Blinkbot: https://photos.app.goo.gl/SKEQ5dtMnQW5dn646  
NodOff: https://photos.app.goo.gl/wdv5hSbbBGJmdpCN9

## Requirements
- Python >=3.5
- Webcam or another video stream

## Setup
1. Install pip3
```
$ apt install python3-pip
```

2. Install virtualenv
```
$ pip3 install virtualenv
```

3. Add the following lines to `.bashrc` to configure virtualenv for python3
```
# Virtual Environment Wrapper
VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
```

4. Clone the repository and create a virtualenv for development
```
$ git clone https://github.com/AryamanReddi99/Hack-The-Midlands.git
$ cd Hack-The-Midlands
$ mkvirtualenv Hack-The-Midlands
```

5. Select the virtualenv
```
$ workon Hack-The-Midlands
```

6. Install dependencies
```
$ pip3 install opencv-python numpy scipy dlib imutils
```

## Usage
1. Download and extract a pre-trained shape predictor
```
$ wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
```

2. Run the detect_blinks demo
```
$ python3 detect_blinks.py --shape-predictor shape_predictor_68_face_landmarks.dat
```
