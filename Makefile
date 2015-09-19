CXX = g++

LDFLAGS = -lopencv_legacy -lopencv_highgui -lopencv_core -lopencv_ml -lopencv_v$

CPPFLAGS = -g -I/usr/include/opencv -I/usr/include/opencv2

all: facedetection_example
