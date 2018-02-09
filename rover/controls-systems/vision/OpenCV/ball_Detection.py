'''

    Description:
        - Detect and calculates distance to ball triangle similarity
          Sadly, there are some false postives so its not perfect. 
          Needs Improvement..

    References: 
        - https://www.pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/
        
    HEAVILY "Borrowed" Code:
        - https://github.com/kd8bxp/find_distance_with_pixycam/blob/master/distance_using_pixycam.ino
        - https://pastebin.com/WVhfmphS
        - https://stackoverflow.com/questions/14038002/opencv-how-to-calculate-distance-between-camera-and-object-using-image

    Formulas:
        Distnace = object_real_world_mm * focal-length_mm / object_image_sensor_mm
        FocalLength = (pixels * knowdistanceininches) / widthOfObject


    PS: If you wanted to add other color spectrums

        #define the lower and upper boundaries of the colors in the HSV color space
        lower = {'red':(166, 84, 141), 'green':(66, 122, 129), 'blue':(97, 100, 117), 'yellow':(23, 59, 119), 'orange':(0, 50, 80)} 
        upper = {'red':(186,255,255), 'green':(86,255,255), 'blue':(117,255,255), 'yellow':(54,255,255), 'orange':(20,255,255)}
 
        #define standard colors for circle around the object
        colors = {'red':(0,0,255), 'green':(0,255,0), 'blue':(255,0,0), 'yellow':(0, 255, 217), 'orange':(0,140,255)}



'''


# packages
import numpy as np
import imutils
import cv2


# Values that need to be defined, in order for this to work

# *ISSUE*

#Calibrated width reading
calWidth = 40

# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 24.0

# initialize the known object width
KNOWN_WIDTH = 2.7 



# Dictionary of specified color spectrums that we want to specifically detect
lower = {'green':(66, 122, 129), 'yellow':(23, 59, 119)} 
upper = {'green':(86,255,255), 'yellow':(54,255,255)} 


# define standard colors for circle around the object
colors = {'green':(0,255,0),  'yellow':(0, 255, 217)}
 

# Create an instance of CV and link it to a camera
camera = cv2.VideoCapture(0)



while True:

    # Calculate the focallenght
    focalLength = (calWidth* KNOWN_DISTANCE) / KNOWN_WIDTH    

    # grab the current frame
    (grabbed, frame) = camera.read()

    # resize the frame, open a Window for display
    frame = imutils.resize(frame, width=800)
  
    # blur the background, and convert it to the HSV color space
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # for each color in dictionary check if object in frame matches with 
    # one of the colors
    for key, value in upper.items():
        # construct a mask for the color from our dictionary of colors, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
       
        # only proceed if at least one contour was found
        if len(cnts) > 0:

            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)

            ((x, y), radius) = cv2.minEnclosingCircle(c)

            M = cv2.moments(c)

            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))


            inches = (KNOWN_WIDTH * focalLength) / radius
 
       
            # only proceed if the radius meets a minimum size. Correct this value for your obect's size
            if radius > 0.5:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
                cv2.putText(frame,key + " ball", (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)


                # Add distance HUD
                cv2.putText(frame, "%.2fft" % (inches / 12), (frame.shape[1] - 200, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 3)
 
     
    # show the frame to our screen
    cv2.imshow("Frame", frame)
   
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()