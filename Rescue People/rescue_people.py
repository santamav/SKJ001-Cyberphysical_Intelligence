from GUI import GUI
from HAL import HAL
# Enter sequential code!
import cv2 as cv

# Coordinates of the safety boat and known survivor location
boat_coordinates = (430492, 4459162)  # 40º16'48.2" N, 3º49'03.5" W
survivor_coordinates = (430532, 4459132)  # 40º16'47.23" N, 3º49'01.78" W

victims_x = boat_coordinates[1] - survivor_coordinates[1] # Relative victims positions
victims_y = boat_coordinates[0] - survivor_coordinates[0] # Relative victims positions
print("x: ", victims_x, "// y: ", victims_y)
boat_x = 0
boat_y = 0

takeoff_height = 2

x_vel = 0.25
angle = 0.6

x_pos = HAL.get_position()[0]
y_pos = HAL.get_position()[1]

initial_linear_vel = 3 # Meters per second
linear_vel = initial_linear_vel # Meters per second
linear_vel_inc = 0.00005# Meters per second

ang_vel = 0.79 # Radians per second

face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')


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
  # time.sleep(0.01)
  if ((victims_x-1 < x_pos) and (x_pos <victims_x+1) and (victims_y-1 < y_pos) and (y_pos < victims_y+1)):
    inPosition = False


def VictimFound(victim_location):
  # Check if the location of the victim is already on the dictionary
  print("victim_location", victim_location)
  # If not, add a new found victim
  # If true, continuw with the search
  return False
	
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
    for face in detected_faces:
      if(VictimFound(face)): break

  linear_vel += linear_vel_inc
  HAL.set_cmd_mix(linear_vel, 0, takeoff_height, ang_vel)

# Final Loop
while True:
  # Enter iterative code!
  GUI.showImage(HAL.get_frontal_image())
  GUI.showLeftImage(HAL.get_ventral_image())
