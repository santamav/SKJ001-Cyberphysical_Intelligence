from GUI import GUI
from HAL import HAL

import cv2

i = 0
while True:
    # Get view from the agent POV
    img = HAL.getImage()
    
    # Process the image to find the red line
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv, 
                          (0, 125, 125), 
                          (30, 255, 255))
    
    # Get the lines contours
    contours, hierarchy = cv2.findContours(red_mask,
                                          cv2.RETR_TREE,
                                          cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the centroid of the figure fromed by the contours
    M = cv2.moments(contours[0])
    
    
    # Calculate the error from the centroid to the center of the screen
    if M["m00"] != 0:
      cX = M["m10"] / M["m00"]
      cY = M["m01"] / M["m00"]
    else:
      cX, cY = 0, 0
      
    # Calculate the velocity components of the agent
      # Forward velocity (positive = forward) (negative = backwards)
      # Angular velocity(positive = left) (negative = right)
    if cX > 0:
      err = 320 - cX
      HAL.setV(1)
      HAL.setW(0.01 * err)
      
      
    # Show agent POV
    GUI.showImage(red_mask)
    # Update number of steps
    print('½d cX: %.2f cY: %.2f')
    i = i + 1