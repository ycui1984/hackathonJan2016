#pragma once
#include <stdio.h>
#include <iostream>
#include <vector>

// Include OpenCV's C++ Interface
#include "opencv2/opencv.hpp"


using namespace cv;
using namespace std;

void playLiveOnMode(Mat srcColor, Mat dst, bool sketchMode, bool evilMode, bool detectMode, bool cartoonMode);

void removePepperNoise(Mat &mask);
