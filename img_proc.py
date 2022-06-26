# import files
import cv2
import numpy as np
import streamlit as st
from PIL import Image

class Proc():

    def det_decay(img_path, unripe):

        # load image from stringIO
        img_path.seek(0)
        img_array = np.asarray(bytearray(img_path.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # load image
        # img = cv2.imread(img_path)

        # reduce the image size
        img = cv2.resize(img, (500, 500))

        # display image
        # cv2.imshow('RGB RAW Image', img)


        # denoising the image
        denoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

        # convert to hsv
        hsv = cv2.cvtColor(denoised, cv2.COLOR_BGR2HSV)

        if not unripe:
            # extract yellow colour from image to get the good parts of the mango
            low_yellow = np.array([12,100,100])
            high_yellow = np.array([34,255,255])

            # preparing mask, Mask shows the yellow parts of the mango
            mask = cv2.inRange(hsv, low_yellow, high_yellow)
        else:
            # extract green color from image to get the good parts of the mango
            low_green = np.array([8,100,100])
            high_green = np.array([80,255,255])

            # preparing mask, Mask shows the green parts of the mango
            mask = cv2.inRange(hsv, low_green, high_green)

        # invert mask, Mask to display the decayed parts of the mango
        inv_mask = cv2.bitwise_not(mask)


        # get the number of white pixels from the mask, white pixels are the yellow parts of the mango
        # so this can be used to set the threshold value for the detection

        white_pixels = cv2.countNonZero(mask)
        # print('Number of good pixels:', white_pixels)

        # display decay parts, decayed parts will be displayed in cyan and other colors 
        # still have to work on that

        res = cv2.bitwise_not(img, img, mask=inv_mask)



        # denoised image
        # cv2.imshow('Denoised Image', denoised)

        # display hsv image
        # cv2.imshow('HSV Conveted Image', hsv)

        # display mask
        # cv2.imshow('Yellow Mask', mask)


        if not unripe:
            # threshold values for the detection of ripe and overripe mangoes
            if white_pixels < 60000:
                print('High chances of decay')
                opmsg = 'High chances of decay'
                # bitwise not
                # cv2.imshow('Possible Decay Locations', res)
                rgbres = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgbres)

            elif white_pixels < 65000:
                print('Possible decay')
                opmsg = 'Possible decay'
                # bitwise not
                # cv2.imshow('Possible Decay Locations', res)
                rgbres = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgbres)
            else:
                opmsg = 'No decay'
                print('No decay')              
        else:
            # threshold values for the detection of unripe and underripe mangoes
            if white_pixels < 40000:
                print('High chances of decay')
                opmsg = 'High chances of decay'
                # bitwise not
                # cv2.imshow('Possible Decay Locations', res)
                rgbres = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgbres)

            elif white_pixels < 42000:
                print('Possible decay')
                opmsg = 'Possible decay'
                # bitwise not
                # cv2.imshow('Possible Decay Locations', res)
                rgbres = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgbres)
            else:
                opmsg = 'No decay'
                print('No decay')

        cv2.waitKey(0)

        return img, opmsg