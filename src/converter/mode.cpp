
#include "mode.h"

void playLiveOnMode(Mat srcColor, Mat dst, bool sketchMode, bool evilMode, bool tdMode,bool cartoonMode)
{
    if (tdMode) {
        Size size = srcColor.size();
        Mat target(size, CV_8U);
        srcColor.copyTo(target, srcColor);
        //generate 3d image based on target
        srcColor.copyTo(dst, target);
        return;
    }

    
    if (sketchMode || evilMode || cartoonMode) {
        // Convert from BGR color to Grayscale
        Mat srcGray;
        cvtColor(srcColor, srcGray, CV_BGR2GRAY);
        
        // Remove the pixel noise with a good Median filter, before we start detecting edges.
        medianBlur(srcGray, srcGray, 7);
        
        Size size = srcColor.size();
        Mat mask = Mat(size, CV_8U);
        Mat edges = Mat(size, CV_8U);
        // Generate a nice edge mask, similar to a pencil line drawing.
        Laplacian(srcGray, edges, CV_8U, 5);
        threshold(edges, mask, 80, 255, THRESH_BINARY_INV);
        // Mobile cameras usually have lots of noise, so remove small
        // dots of black noise from the black & white edge mask.
        removePepperNoise(mask);
        if (sketchMode || evilMode) {
            cvtColor(mask, dst, CV_GRAY2BGR);
            if (sketchMode) return;
            // Evil mode, making everything look like a scary bad guy.
            // (Where "srcGray" is the original grayscale image plus a medianBlur of size 7x7).
            Mat edges2;
            Scharr(srcGray, edges, CV_8U, 1, 0);
            Scharr(srcGray, edges2, CV_8U, 1, 0, -1);
            edges += edges2;
            threshold(edges, mask, 12, 255, THRESH_BINARY_INV);
            medianBlur(mask, mask, 3);
            cvtColor(mask, dst, CV_GRAY2BGR);
            return;
        } else {
            // Do the bilateral filtering at a shrunken scale, since it
            // runs so slowly but doesn't need full resolution for a good effect.
            Size smallSize;
            smallSize.width = size.width/2;
            smallSize.height = size.height/2;
            Mat smallImg = Mat(smallSize, CV_8UC3);
            resize(srcColor, smallImg, smallSize, 0,0, INTER_LINEAR);
            
            // Perform many iterations of weak bilateral filtering, to enhance the edges
            // while blurring the flat regions, like a cartoon.
            Mat tmp = Mat(smallSize, CV_8UC3);
            int repetitions = 7;        // Repetitions for strong cartoon effect.
            for (int i=0; i<repetitions; i++) {
                int size = 9;           // Filter size. Has a large effect on speed.
                double sigmaColor = 9;  // Filter color strength.
                double sigmaSpace = 7;  // Positional strength. Effects speed.
                bilateralFilter(smallImg, tmp, size, sigmaColor, sigmaSpace);
                bilateralFilter(tmp, smallImg, size, sigmaColor, sigmaSpace);
            }
            // Go back to the original scale.
            resize(smallImg, srcColor, size, 0,0, INTER_LINEAR);
            // Clear the output image to black, so that the cartoon line drawings will be black (ie: not drawn).
            memset((char*)dst.data, 0, dst.step * dst.rows);
            // Use the blurry cartoon image, except for the strong edges that we will leave black.
            srcColor.copyTo(dst, mask);
        }
    }
}

// Remove black dots (upto 4x4 in size) of noise from a pure black & white image.
// ie: The input image should be mostly white (255) and just contains some black (0) noise
// in addition to the black (0) edges.
void removePepperNoise(Mat &mask)
{
    // For simplicity, ignore the top & bottom row border.
    for (int y=2; y<mask.rows-2; y++) {
        // Get access to each of the 5 rows near this pixel.
        uchar *pThis = mask.ptr(y);
        uchar *pUp1 = mask.ptr(y-1);
        uchar *pUp2 = mask.ptr(y-2);
        uchar *pDown1 = mask.ptr(y+1);
        uchar *pDown2 = mask.ptr(y+2);

        // For simplicity, ignore the left & right row border.
        pThis += 2;
        pUp1 += 2;
        pUp2 += 2;
        pDown1 += 2;
        pDown2 += 2;
        for (int x=2; x<mask.cols-2; x++) {
            uchar v = *pThis;   // Get the current pixel value (either 0 or 255).
            // If the current pixel is black, but all the pixels on the 2-pixel-radius-border are white
            // (ie: it is a small island of black pixels, surrounded by white), then delete that island.
            if (v == 0) {
                bool allAbove = *(pUp2 - 2) && *(pUp2 - 1) && *(pUp2) && *(pUp2 + 1) && *(pUp2 + 2);
                bool allLeft = *(pUp1 - 2) && *(pThis - 2) && *(pDown1 - 2);
                bool allBelow = *(pDown2 - 2) && *(pDown2 - 1) && *(pDown2) && *(pDown2 + 1) && *(pDown2 + 2);
                bool allRight = *(pUp1 + 2) && *(pThis + 2) && *(pDown1 + 2);
                bool surroundings = allAbove && allLeft && allBelow && allRight;
                if (surroundings == true) {
                    // Fill the whole 5x5 block as white. Since we know the 5x5 borders
                    // are already white, just need to fill the 3x3 inner region.
                    *(pUp1 - 1) = 255;
                    *(pUp1 + 0) = 255;
                    *(pUp1 + 1) = 255;
                    *(pThis - 1) = 255;
                    *(pThis + 0) = 255;
                    *(pThis + 1) = 255;
                    *(pDown1 - 1) = 255;
                    *(pDown1 + 0) = 255;
                    *(pDown1 + 1) = 255;
                }
                // Since we just covered the whole 5x5 block with white, we know the next 2 pixels
                // won't be black, so skip the next 2 pixels on the right.
                pThis += 2;
                pUp1 += 2;
                pUp2 += 2;
                pDown1 += 2;
                pDown2 += 2;
            }
            // Move to the next pixel.
            pThis++;
            pUp1++;
            pUp2++;
            pDown1++;
            pDown2++;
        }
    }
}
