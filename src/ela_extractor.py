import cv2
import os
import numpy as np
import math

def getImageDifference(image1, image2):
    width, height = image1.shape[1::-1]
    outputMap = np.zeros((height, width, 3))
    tmpColor1 = np.zeros(3)
    
    for i in range(0, height):
      # print('i: ', i)
      for j in range (0, width):
          #print('i, j: ', i, j)
          tmpColor1 = image1[i][j]
          #print('tempclr; ', len(tmpColor1))
          tmpColor2 = image2[i][j]
          red_diff = int(tmpColor1[0]) - int(tmpColor2[0])
          green_diff = int(tmpColor1[1]) - int(tmpColor2[1])
          blue_diff = int(tmpColor1[2]) - int(tmpColor2[2])
          outputMap[i][j][0] = float(red_diff * red_diff)
          outputMap[i][j][1] = float(green_diff * green_diff)
          outputMap[i][j][2] = float(blue_diff * blue_diff)

    return outputMap

def getELA(imageDirectory, imageName, outputDirectory):
    filename = imageDirectory+imageName

    sc_width = 600
    sc_height = 600
    
    quality = 75;
    displayMultiplier = 20;

    origImage = cv2.imread(filename)
    outpath = outputDirectory + 'recompressed_' + imageName

    cv2.imwrite(outpath, origImage, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    recompressedImage = cv2.imread(outpath)
    imageDifference = getImageDifference(origImage, recompressedImage)

    elaMin = np.amax(imageDifference)
    elaMax = np.amin(imageDifference)
    intDifference = np.zeros(imageDifference.shape)

    for i in range(0, imageDifference.shape[0]):
        for j in range(0, imageDifference.shape[1]):
            for k in range(0, imageDifference.shape[2]):
                intDifference[i][j][k] = int(math.sqrt(imageDifference[i][j][k]) * displayMultiplier)
                if (intDifference[i][j][k] > 255):
                    intDifference[i][j][k] = 255

    displaySurface_temp = intDifference

    ds_height = displaySurface_temp.shape[1]
    ds_width = displaySurface_temp.shape[0]

    if (ds_height > ds_width):
        if (ds_height > sc_height):
            sc_width = (sc_height * ds_width) / ds_height
            displaySurface = cv2.resize(displaySurface_temp, (int(sc_width), sc_height))

        else:
            displaySurface = displaySurface_temp
    else:
        if (ds_width > sc_width):
            sc_height = (sc_width * ds_height) / ds_width
            displaySurface = cv2.resize(displaySurface_temp, (sc_width, sc_height))
        else:
            displaySurface = displaySurface_temp
    print('ds: ', (displaySurface.shape))
    displaySurface = displaySurface_temp
    cv2.imwrite(outputDirectory + 'difference_' + imageName , displaySurface)

    return origImage

#if __name__ == "__main__":
 #   getELA("comp30.jpg")
