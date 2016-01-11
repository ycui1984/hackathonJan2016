#include <stdio.h>
#include <stdlib.h>

// Include OpenCV's C++ Interface
#include "opencv2/opencv.hpp"
#include "opencv2/imgcodecs/imgcodecs.hpp"
#include "opencv2/videoio/videoio.hpp"

#include "mode.h"

using namespace cv;
using namespace std;

bool m_sketchMode = false, m_evilMode = false, m_3dMode = false, m_cartoonMode = true;

int main(int argc, char *argv[])
{
    if (argc != 5) {
        cout << "usage: Hackathon <input file> <output file> <frames> <mode>" << endl;
        return -1;
    }
    Mat LoadedImage;
    VideoCapture cap(argv[1]);
    
    Size S = Size((int) cap.get(CAP_PROP_FRAME_WIDTH),
                  (int) cap.get(CAP_PROP_FRAME_HEIGHT));
    Size SizeOfFrame = cv::Size(S.width, S.height);
    
    VideoWriter video("tmp.mp4", CV_FOURCC('8', 'B', 'P', 'S'), 30, SizeOfFrame, true);

    cout << "S=" << S << endl;
    if (0 == strcmp(argv[4], "sketch"))
        m_sketchMode = true;
    else if (0 == strcmp(argv[4], "evil"))
        m_evilMode = true;
    else if (0 == strcmp(argv[4], "3d"))
        m_3dMode = true;
    else m_cartoonMode = true;
    cout << argv[4] << " mode" << endl;
    
    for (int i = 0; i<stoi(argv[3]); i++)
    {
        bool Is = cap.grab();
        if (Is == false) {
            cout << "cannot grab video frame" << endl;
        }
        else {
            cap.retrieve(LoadedImage, CV_CAP_OPENNI_BGR_IMAGE);
            
            resize(LoadedImage, LoadedImage, Size(S.width, S.height));
                
            cout << i << "th frame" << endl;
            Mat displayedFrame = Mat(LoadedImage.size(), CV_8UC3);
            playLiveOnMode(LoadedImage, displayedFrame, m_sketchMode, m_evilMode, m_3dMode, m_cartoonMode);
            video.write(displayedFrame);
        }
    }
    string cmd = "ffmpeg -i tmp.mp4 -qscale 4 -vcodec libx264 -f mp4 " + string(argv[2]);
    system(cmd.c_str());
    system("rm tmp.mp4");
    
    return 0;
}