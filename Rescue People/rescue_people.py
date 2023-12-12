from GUI import GUI
from HAL import HAL
# Enter sequential code!

while True:
    # Enter iterative code!from GUI import GUI
from HAL import HAL
import cv2 as cv

# Coordinates of the safety boat and known survivor location
boat_coordinates = (430492, 4459162)  # 40º16'48.2" N, 3º49'03.5" W
survivor_coordinates = (430532, 4459132)  # 40º16'47.23" N, 3º49'01.78" W

victims_x = boat_coordinates[1] - survivor_coordinates[1] # Relative victims positions
victims_y = boat_coordinates[0] - survivor_coordinates[0] # Relative victims positions
print("x: ", victims_x, "// y: ", victims_y)
boat_x = 0
boat_y = 0

takeoff_height = 4

x_vel = 0.25
angle = 0.6

x_pos = HAL.get_position()[0]
y_pos = HAL.get_position()[1]

initial_linear_vel = 3 # Meters per second
linear_vel = initial_linear_vel # Meters per second
linear_vel_inc = 0.00005# Meters per second

ang_vel = 0.79 # Radians per second

face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_alt.xml')


num_victims = 5
saved_victims = 0
faces = []

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
  # TODO: Should calculate the angle to face the direction in which we are moving
  # time.sleep(0.01)
  if ((victims_x-1 < x_pos) and (x_pos <victims_x+1) and (victims_y-1 < y_pos) and (y_pos < victims_y+1)):
    inPosition = False

	
# Find and save 
while (saved_victims <= num_victims):
  # Get cameras data
  frontal_img = HAL.get_frontal_image()
  ventral_img = HAL.get_ventral_image()
  # Show images
  GUI.showImage(frontal_img)
  GUI.showLeftImage(ventral_img)
  # Check if there are any faces
  img_gray = cv.cvtColor(ventral_img, cv.COLOR_BGR2GRAY)
  for angle in range (0, 365, 10):
    detected_faces = face_cascade.detectMultiScale(cv.rotate(img_gray, angle), 1.1, 4)
    print("Detected faces", len(detected_faces))
    # When there is a face stop on top of it and recognize it
    # If no faces move in spiral
    # increment linear velocity
  linear_vel += linear_vel_inc
  HAL.set_cmd_mix(linear_vel, 0, takeoff_height, ang_vel)

# Final Loop
while True:
  # Enter iterative code!
  GUI.showImage(HAL.get_frontal_image())
  GUI.showLeftImage(HAL.get_ventral_image())
