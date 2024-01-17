from GUI import GUI
from HAL import HAL
import cv2 as cv
import math

# Coordinates of the safety boat and known survivor location
boat_coordinates = (430492, 4459162)  # 40º16'48.2" N, 3º49'03.5" W
survivor_coordinates = (430532, 4459132)  # 40º16'47.23" N, 3º49'01.78" W

victims_x = boat_coordinates[1] - survivor_coordinates[1] # Relative victims positions
victims_y = boat_coordinates[0] - survivor_coordinates[0] # Relative victims positions
print("Victims at x: ", victims_x, "// y: ", victims_y)
boat_x = 0
boat_y = 0

takeoff_height = 3
angle = 0.6

x_pos = HAL.get_position()[0]
y_pos = HAL.get_position()[1]


face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')


num_victims = 5
saved_victims = 0
victims_locations = []

distance = 0 # Meters
distance_inc = 0.98 # Meters
spiral_angle = 0 # rads
spiral_angle_inc = 0.174533 # rads
search_max_distance = 50 # Meters

distance_thr = 4.6 # new victim distance threshold in meters

# Takeoff
print("Taking off")
HAL.takeoff(takeoff_height)

def FaceFound(face):
  # Get drone location and orientation
  drone_location = HAL.get_position()
  dron_orientation = HAL.get_orientation()
  # Calculate the victim location from the drone orientation and victim pixel coordinates
  victim_location = (drone_location[0],drone_location[1])
  #print("Drone location: ", drone_location, "\tVictim location: ", victim_location)
  # Check if the victim is already saved
  for known_victim in victims_locations:
    # Calculate the distance to the known victim
    sqr_distance = (known_victim[0]-victim_location[0])**2 + (known_victim[1]-victim_location[1])**2
    if sqr_distance < distance_thr**2:
      #print("Victim already saved with distance: ", sqr_distance, "\tknown victims: ", len(victims_locations))
      return # The victim was already found
    
  # If we end the loop, it means that the victim has not been saved yet
  victims_locations.append(victim_location) # store the victim location
  print('saved victim at location: ', victim_location)
  print('saved victims: ', len(victims_locations))

# Initial target location
target_x = victims_x
target_y = victims_y

# Search loop
print("Drone in position, searching for victims")
is_searching = True
is_in_position = False
while (is_searching):
  # Get Cameras data
  ventral_img = HAL.get_ventral_image()
  frontal_img = HAL.get_frontal_image()
  # Show images
  GUI.showImage(frontal_img)
  GUI.showLeftImage(ventral_img)
  # Get drone location
  x_pos = HAL.get_position()[0]
  y_pos = HAL.get_position()[1]
  # Move to position
  HAL.set_cmd_pos(target_x, target_y, takeoff_height, angle)
  if(is_in_position): # If we are in position
    # Transform the image to grayscale
    img_gray = cv.cvtColor(ventral_img, cv.COLOR_BGR2GRAY)
    # Check for faces
    for im_angle in range (0, 365, 10):
      # Compute rotation matrix
      (h, w) = img_gray.shape[:2]
      center = (w // 2, h // 2)
      M = cv.getRotationMatrix2D(center, im_angle, 1.0)
      # Perform the rotation
      im_rot = cv.warpAffine(img_gray, M, (w, h))
      #plt.imshow(im_rot, cmap='gray')
      #plt.show()
      # Detect faces
      detected_faces = face_cascade.detectMultiScale(im_rot, 1.1, 4)
      #print("Detected faces at angle", angle, ":", detected_faces)
      if(len(detected_faces) > 0):
        for face in detected_faces:
          FaceFound(face)
    # Increment spiral angle
    spiral_angle += spiral_angle_inc
    # Increment spiral distance
    distance = (spiral_angle/(math.pi*2)) * distance_inc # For every loop increment the distance
    # Calculate new target location
    target_x = victims_x + distance * math.cos(spiral_angle)
    target_y = victims_y + distance * math.sin(spiral_angle)
    #print("New location: ", target_x, target_y)
  #else:
    #print("Moving to: ", target_x, target_y, " with ", saved_victims, " saved victims")
  # Calculate distance to position
  sqr_distance_to_position = (target_x-x_pos)**2 + (target_y-y_pos)**2
  is_in_position = sqr_distance_to_position < 1
  # Update the is searching condition
  is_searching = len(victims_locations) <= num_victims and distance < search_max_distance

# Return to boat
print("All vicims found, returning to boat")
target_x = boat_x
target_y = boat_y
is_in_position = False
while not is_in_position:
  # Get Cameras data
  ventral_img = HAL.get_ventral_image()
  frontal_img = HAL.get_frontal_image()
  # Show images
  GUI.showImage(frontal_img)
  GUI.showLeftImage(ventral_img)
  HAL.set_cmd_pos(target_x, target_y, takeoff_height, angle)
  # Check if drone is in postion
  x_pos = HAL.get_position()[0]
  y_pos = HAL.get_position()[1]
  sqr_distance_to_position = (target_x-x_pos)**2 + (target_y-y_pos)**2
  is_in_position = sqr_distance_to_position < 1

# Land drone
print("Landing drone")
is_landed = False
while (not is_landed):
    # Get Cameras data
  ventral_img = HAL.get_ventral_image()
  frontal_img = HAL.get_frontal_image()
  # Show images
  GUI.showImage(frontal_img)
  GUI.showLeftImage(ventral_img)
  # Land drone
  HAL.land()
  is_landed = HAL.get_landed_state() == 1
  
print("Drone landed")
while True: