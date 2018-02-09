# Tennis-Ball-Detection:
Detect tennis balls via realtime webcam on Titan Rover for the 2018 Challenge.

## version: 0.1

## Functions:
Current version code can perform below functions:

* Detect tennis balls within around three meters, draw bounding box with object name and score
* Detect the distance to the detected tennis ball
* Streaming reatime on screen
* Output streaming video to local file
* Output/Post distance (meters) back to DeepStream server

Future functions will include:

* Increase the accuracy of tennis ball detection
* detect the angle of file of view of camera to assist Rover movement decision

## Dependencies

Tensorflow Tennis Ball Detection depends on the following libraries:

* Tensorflow 1.3.0
* OpenCV 3.3.0
* Protobuf 2.6
* Pillow 1.0
* lxml
* tf Slim (which is included in the "tensorflow/models/research/" checkout)
* Matplotlib
* Numpy
* Scipy

## Author

**Zhangying (Mandy) He** - mandyhe@csu.fullerton.edu, graduate student of Computer Science at CSUF.


