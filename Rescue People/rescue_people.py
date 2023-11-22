from GUI import GUI
from HAL import HAL

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
iterations = 0
spiral_iterations = 300
landing_margin = 0.07

x_pos = HAL.get_position()[0]
y_pos = HAL.get_position()[1]

# Takeoff
HAL.takeoff(takeoff_height)
# Move to accident position
while not ((victims_x-1 < x_pos) and (x_pos <victims_x+1) and (victims_y-1 < y_pos) and (y_pos < victims_y+1)):
	GUI.showImage(HAL.get_frontal_image())
	GUI.showLeftImage(HAL.get_ventral_image())
	x_pos = HAL.get_position()[0]
	y_pos = HAL.get_position()[1]
	HAL.set_cmd_pos(victims_x, victims_y, 3, angle)
	# TODO: Should calculate the angle to face the direction in which we are moving
	# time.sleep(0.01)
# Find and save 

while True:
  	# Enter iterative code!
    GUI.showImage(HAL.get_frontal_image())
    GUI.showLeftImage(HAL.get_ventral_image())