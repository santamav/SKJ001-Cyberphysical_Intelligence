from GUI import GUI
from HAL import HAL
import cv2 as cv
import math

# Coordinates of the safety boat and known survivor location
boat_coordinates = (430492, 4459162)  # 40º16'48.2" N, 3º49'03.5" W
survivor_coordinates = (430532, 4459132)  # 40º16'47.23" N, 3º49'01.78" W

victims_x = boat_coordinates[1] - survivor_coordinates[1] # Relative victims positions
victims_y = boat_coordinates[0] - survivor_coordinates[0] # Relative victims positions
print("x: ", victims_x, "// y: ", victims_y)
boat_x = 0
boat_y = 0

takeoff_height = 3

x_vel = 0.25
angle = 0.6

x_pos = HAL.get_position()[0]
y_pos = HAL.get_position()[1]

initial_linear_vel = 3 # Meters per second
linear_vel = initial_linear_vel # Meters per second
linear_vel_inc = 0.005# Meters per loop

ang_vel = 0.79 # Radians per second

face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')


num_victims = 5
saved_victims = 0
victims_locations = []
loc_radius = 3 # Area threshold to consider a victim already saved

# Takeoff
HAL.takeoff(takeoff_height)
# Move to accident position

inPosition = True
while inPosition:
  GUI.showImage(HAL.get_frontal_image())
  GUI.showLeftImage(HAL.get_ventral_image())
  x_pos = HAL.get_position()[0]
  y_pos = HAL.get_position()[1]
  HAL.set_cmd_pos(victims_x, victims_y, 3, angle)
  # time.sleep(0.01)
  if ((victims_x-1 < x_pos) and (x_pos <victims_x+1) and (victims_y-1 < y_pos) and (y_pos < victims_y+1)):
    inPosition = False


def VictimFound():
  # Get drone location and orientation
  drone_location = HAL.get_position()
  dron_orientation = HAL.get_orientation()
  # Calculate the victim location from the drone orientation
  victim_location = (drone_location[0] + math.cos(dron_orientation[2]) - math.sin(dron_orientation[2]), drone_location[1] + math.sin(dron_orientation[2]) + math.cos(dron_orientation[2]))
  #print("Drone location: ", drone_location, "\tVictim location: ", victim_location)
  # Check if the victim is already saved
  for found_victim in victims_locations:
    if (found_victim[0]-loc_radius < victim_location[0] and victim_location[0] < found_victim[0]+loc_radius and found_victim[1]-loc_radius < victim_location[1] and victim_location[1] < found_victim[1]+loc_radius):
      return False # The victim was already found

  # If we get here, the victim is not saved yet
  victims_locations.append(victim_location) # store the victim location
  return True # The victim is new
	
# Find and save 
while (saved_victims <= num_victims):
  # Get cameras data
  frontal_img = HAL.get_frontal_image()
  ventral_img = HAL.get_ventral_image()
  # Show images
  GUI.showImage(frontal_img)
  GUI.showLeftImage(ventral_img)
  # Transform the image to grayscale
  img_gray = cv.cvtColor(ventral_img, cv.COLOR_BGR2GRAY)
  for angle in range (0, 365, 10):
    # Compute rotation matrix
    (h, w) = img_gray.shape[:2]
    center = (w // 2, h // 2)
    M = cv.getRotationMatrix2D(center, angle, 1.0)

    # Perform the rotation
    im_rot = cv.warpAffine(img_gray, M, (w, h))
    #plt.imshow(im_rot, cmap='gray')
    #plt.show()

    # Detect faces
    detected_faces = face_cascade.detectMultiScale(im_rot, 1.1, 4)
    #print("Detected faces at angle", angle, ":", detected_faces)
    # When if we detect a face, store it location and exit the loop
    if(len(detected_faces) > 0):
      for face in detected_faces:
        if(VictimFound()):
          saved_victims += 1
          print("Número de victimas encontradas: ", saved_victims)
      break # If we have already found a face, we don't need to keep rotating the image

  linear_vel += linear_vel_inc
  HAL.set_cmd_mix(linear_vel, 0, takeoff_height, ang_vel)

# Final Loop
while True:
  # Enter iterative code!
  GUI.showImage(HAL.get_frontal_image())
  GUI.showLeftImage(HAL.get_ventral_image())
