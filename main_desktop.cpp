#include <stdio.h>
#include <stdlib.h>

// Include OpenCV's C++ Interface
#include "opencv2/opencv.hpp"

// Include the rest of our code!
#include "mode.h"

using namespace cv;
using namespace std;

#if !defined VK_ESCAPE
    #define VK_ESCAPE 0x1B      // Escape character (27)
#endif

// Try to set the camera resolution. Note that this only works for some cameras on
// some computers and only for some drivers, so don't rely on it to work!
const int DESIRED_CAMERA_WIDTH = 640;
const int DESIRED_CAMERA_HEIGHT = 480;

bool m_sketchMode = false, m_evilMode = false, m_detectMode = true, openedHulu = true, m_cartoonMode = false;

// Get access to the webcam.
void initWebcam(VideoCapture &videoCapture, int cameraNumber)
{
    // Get access to the default camera.
    try {   // Surround the OpenCV call by a try/catch block so we can give a useful error message!
        videoCapture.open(cameraNumber);
    } catch (cv::Exception &e) {}
    if ( !videoCapture.isOpened() ) {
        cerr << "ERROR: Could not access the camera!" << endl;
        exit(1);
    }
    cout << "Loaded camera " << cameraNumber << "." << endl;
}


// Keypress event handler. Note that it should be a 'char' and not an 'int' to better support Linux.
void onKeypress(char key)
{
    switch (key) {
    case 's':
        m_sketchMode = true;
        m_evilMode = m_detectMode = m_cartoonMode = false;
        cout << "Sketch mode: " << m_sketchMode << endl;
        break;
    case 'e':
        m_evilMode = true;
        m_sketchMode = m_detectMode = m_cartoonMode = false;
        cout << "Evil mode: " << m_evilMode << endl;
        break;
    case 'd':
        m_detectMode = true;
        m_sketchMode = m_evilMode = m_cartoonMode = false;
        cout << "Detect mode: " << m_detectMode << endl;
        openedHulu = false;
        break;
    case 'c':
        m_cartoonMode = !m_cartoonMode;
        m_sketchMode = m_evilMode = m_detectMode = false;
        cout << "Cartoon mode: " << m_cartoonMode << endl;
        break;
    default:
        cout << "unknown mode code" << endl;
        break;
    }
}


int main(int argc, char *argv[])
{
    // Allow the user to specify a camera number, since not all computers will be the same camera number.
    int cameraNumber = 0;   // Change this if you want to use a different camera device.
    if (argc > 1) {
        cameraNumber = atoi(argv[1]);
    }

    // Get access to the camera.
    VideoCapture camera;
    initWebcam(camera, cameraNumber);

    // Try to set the camera resolution. Note that this only works for some cameras on
    // some computers and only for some drivers, so don't rely on it to work!
    camera.set(CV_CAP_PROP_FRAME_WIDTH, DESIRED_CAMERA_WIDTH);
    camera.set(CV_CAP_PROP_FRAME_HEIGHT, DESIRED_CAMERA_HEIGHT);
    namedWindow("DIY", CV_WINDOW_NORMAL);
    namedWindow("ORIG", CV_WINDOW_NORMAL | CV_GUI_NORMAL);

    // Run forever, until the user hits Escape to "break" out of this loop.
    while (true) {

        // Grab the next camera frame. Note that you can't modify camera frames.
        Mat cameraFrame;
        camera >> cameraFrame;
        if( cameraFrame.empty() ) {
            cerr << "ERROR: Couldn't grab the next camera frame." << endl;
            exit(1);
        }

        Mat displayedFrame = Mat(cameraFrame.size(), CV_8UC3), dist;
        resize(cameraFrame, dist, cvSize(180, 135));
        imshow("ORIG", dist);
        resizeWindow("ORIG", 180, 135);
        moveWindow("ORIG", 640, 0);
        
        playLiveOnMode(cameraFrame, displayedFrame, m_sketchMode, m_evilMode, m_detectMode, m_cartoonMode);
        
        imshow("DIY", displayedFrame);
        moveWindow("DIY", 0, 0);
        
        // IMPORTANT: Wait for atleast 20 milliseconds, so that the image can be displayed on the screen!
        // Also checks if a key was pressed in the GUI window. Note that it should be a "char" to support Linux.
        char keypress = waitKey(20);  // This is needed if you want to see anything!
        if (keypress == VK_ESCAPE) {   // Escape Key
            // Quit the program!
            break;
        }
        // Process any other keypresses.
        if (keypress > 0) {
            cout << keypress;
            onKeypress(keypress);
        }

    }//end while

    return EXIT_SUCCESS;
}
