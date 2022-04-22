# GRADING IN TEXT

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

Grading or marking student the answer sheet is a very common thing of teacher after the student test. However, this one costs a lot of time depend on the number of students that teacher teach and easily to make mistake when manual grading . <br>
Understanding these concerns, one of solution has been developed that is Optical Mark Recognition.  <br>
This solution is just suitable with multiple choice question test which requires student to highlight the one or more the correct options (A, B, C, D). Besides, in real life, we have a typical kind of test that is short answer. To deal with such kind of test, we propose a AI system which can scan the answer sheet then extracting exactly the handwriting information, content in each answer box correspond with question number of the test based on a defined format answer sheets. After that, the extracted content will be compared string by string with a "True Answers" file, input by user.

## Devices
- Raspberry pi 4
- Waveshare 3.5 Inch Raspberry Pi High-Speed SPI Resistive Touch Display
- Android phone
## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

1/ Install droidcam app on your android device with "keyword droidcam" or click this link https://play.google.com/store/apps/details?id=com.dev47apps.droidcam&hl=vi&gl=US .

2/ Download the folder rasp code in this respositories.

3/ Raspberry pi have python version 3.9 and run on 64-bit (aarch64) OS (If you use other type the system might not work correctly)

4/ Register the teacher data 

### Installing
1/ Update your rapberry pi
  ```
  sudo apt-get update && sudo apt-get upgrade
  ```
2/ Install required libraries or you can run install.sh in install_lib folder
  ```
  sudo apt install build-essential cmake pkg-config -y
  sudo apt install libjpeg-dev libtiff5-dev libpng-dev -y
  sudo apt install libavcodec-dev libavformat-dev -y
  sudo apt install libxvidcore-dev libx264-dev -y
  sudo apt install libfontconfig1-dev libcairo2-dev -y
  sudo apt install libgdk-pixbuf2.0-dev libpango1.0-dev -y
  sudo apt install libgtk2.0-dev libgtk-3-dev -y
  sudo apt install libtlas-base-dev gfortran -y
  sudo apt install libhdf5-dev libhdf5-serial-dev libhdf5-103 -y
  sudo apt install python3-pyqt5 -y
  sudo apt install -y  libhdf5-dev libhdf5-serial-dev -y
  ```
3/ Install required python library or you can run install2.sh in install_lib folder
  ```
  wget https://drive.google.com/file/d/1tuNTevmFIEEC9eADdFZEQzebi_ewiPoN/view?usp=sharing
  pip3 install numpy==1.19.2
  pip3 install tensorflow-2.6.0-cp39-cp39-linux_aarch64.whl
  pip3 install cvlib
  pip3 install keras==2.6.0
  pip3 install firebase-admin
  ```
4/ Open application.py file and change the url to the url on your droidcam app.

5/ Run application.py and enjoy

## Usage <a name = "usage"></a>

Add notes about how to use the system.
