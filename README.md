# Project Jonica

## Description
Project Jonica is a computer vision application developed for the Jonica competition. It leverages powerful image processing libraries like OpenCV, scikit-image, and others to perform tasks such as image enhancement, object detection, and real-time image analysis.

## Installation

To set up this project locally, follow these steps:

### Prerequisites
- RaspberryOS
- Python 3.x

### Setup
1. Clone the repository:
   ```bash
   git clone [URL]
   cd jonica-2024

2. Install the required packages:
   ```bash
   sudo apt update
   sudo apt install python3-opencv
   sudo apt install python3-numpy
   sudo apt install python3-picamera2
   sudo apt install python3-RPi.GPIO
   sudo apt install python3-pigpio
   ```

### Usage
To run the application, execute the following command in the root directory of the project:

```bash
sudo pigpiod
python src/main.py
```

### Features
- Real-time image processing
- Advanced object detection algorithms
- User-friendly graphical interface

### License
This project is licensed under the GNU License - see the LICENSE file for details.
