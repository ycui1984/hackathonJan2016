#include <stdio.h>
#include <stdlib.h>

// Include OpenCV's C++ Interface
#include "opencv2/opencv.hpp"
#include "opencv2/imgcodecs/imgcodecs.hpp"
#include "opencv2/videoio/videoio.hpp"

// Include the rest of our code!
#include "mode.h"

using namespace cv;
using namespace std;

bool m_sketchMode = false, m_evilMode = false, m_detectMode = false, openedHulu = true, m_cartoonMode = true;

int main(int argc, char *argv[])
{
    Mat LoadedImage;
    VideoCapture cap(argv[1]);
    
    Size S = Size((int) cap.get(CAP_PROP_FRAME_WIDTH),
                  (int) cap.get(CAP_PROP_FRAME_HEIGHT));
    Size SizeOfFrame = cv::Size(S.width, S.height);
    
    VideoWriter video(argv[2], CV_FOURCC('8', 'B', 'P', 'S'), 30, SizeOfFrame, true);
    

    cout << "S=" << S << endl;
    for (int i = 0; i<100; i++)
    {
        
        bool Is = cap.grab();
        if (Is == false) {
            
            cout << "cannot grab video frame" << endl;
            
        }
        else {
            
            // Receive video from your source
            cap.retrieve(LoadedImage, CV_CAP_OPENNI_BGR_IMAGE);
            
            resize(LoadedImage, LoadedImage, Size(S.width, S.height));
                
            cout << "Saving video" << endl;
            Mat displayedFrame = Mat(LoadedImage.size(), CV_8UC3);
            playLiveOnMode(LoadedImage, displayedFrame, m_sketchMode, m_evilMode, m_detectMode, m_cartoonMode);
            video.write(displayedFrame);
        }
    }
}