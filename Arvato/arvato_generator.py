import json
import jmespath
import numpy as np
import math

# generating yaw value from quaternon
def convert_quaternon(x: float, y: float, z: float, w: float) -> float:
    return math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))

# creating location tag from components
def create_location_tag(level: str, aisle: int, shelf: int, shelf_level: str) -> str:
    return ("PS-"+level+str(aisle)+"-"+str(shelf)+"-"+str(shelf_level))

# generating location tag from previous location
def generate_next_location(prev_loc: str) -> str:

    # splitting previous location
    split_loc = prev_loc.split("-")
    split_shelf = list(split_loc[1])

    # extracting parameters for location tag
    level = split_shelf[0]
    aisle = int(split_shelf[1]+split_shelf[2])
    shelf = int(split_loc[2]) + 1
    shelf_level = split_loc[3]

    # creating new location
    return create_location_tag(level, aisle, shelf, shelf_level)

# function to get shelf number from location tag
def get_shelf(loc: str) -> str:

    # splitting previous location
    split_loc = loc.split("-")

    return split_loc[2]
    
# collecting data from user
aisle_no = int(input("Enter the aisle number as an integer: "))
shelf_start = int(input("Enter the starting shelf number as an integer: "))
shelf_finish = int(input("Enter the finishing shelf number as an integer: "))
module_no = int(input("Enter the number of modules to be divided as an integer: "))

# assigning data manually for simple testing
# TO BE REMOVED LATER
'''
aisle_no = 14
shelf_start = 501
shelf_finish = 609
module_no = 7
'''

#loading the json file
file = open('Python/Arvato/14.json') #TODO: change with respect to system setup
data = json.load(file)

#extracting all points
loc = jmespath.search("loc", data)

#extracting position data
start_x = jmespath.search("loc[0].position.x", data)
start_y = jmespath.search("loc[0].position.y", data)
finish_x = jmespath.search("loc[1].position.x", data)
finish_y = jmespath.search("loc[1].position.y", data)

#extracting orientation data
start_z = jmespath.search("loc[0].orientation.z", data)
start_w = jmespath.search("loc[0].orientation.w", data)
finish_z = jmespath.search("loc[1].orientation.z", data)
finish_w = jmespath.search("loc[1].orientation.w", data)

#extracting SAP_location data
start_SAP = jmespath.search("loc[0].SAP_Location", data)
finish_SAP = jmespath.search("loc[1].SAP_Location", data)

# closing the json file
file.close()

# finding the best-fit line between the start and finish points
A = np.array([[start_x, 1], [finish_x, 1]])
b = np.array([start_y, finish_y])
x = np.linalg.solve(A, b)

# extracting slope(m) and linear constant(b)
m = x[0]
b = x[1]

# calculating the x, z and w increments
x_inc = (finish_x-start_x)/(module_no-2)
z_inc = (finish_z-start_z)/(module_no-2)
w_inc = (finish_w-start_w)/(module_no-2)

# calculating total number of points
total_num_of_points = shelf_finish - shelf_start

# initializing storage arrays
points = [[start_x, start_y]]
orientations = [convert_quaternon(0.0, 0.0, start_z, start_w)]

# iterating through modules
for i in range(module_no-2):

    # calculating x and y for each point
    current_x = start_x + (i+1)*x_inc
    current_y = m*current_x + b
    points.append([current_x, current_y])

    # calculating orientation for each point
    current_z = start_z + (i+1)*z_inc
    current_w = start_w + (i+1)*w_inc
    current_yaw = convert_quaternon(0.0, 0.0, current_z, current_w)
    orientations.append(current_yaw)

# initializing arrays to dump into json
loc = []
initial_points = []
final_points = []
differences = []

# creating initial location tag
prev_loc = create_location_tag("A", aisle_no, shelf_start-1, "A")

# extracting txt for GeoGebra
txt_file = open('Python/Arvato/geoGebra.txt', 'w') #TODO: change with respect to system setup

# taking measured data to compare
file = open('Python/Arvato/14_complete.json') #TODO: change with respect to system setup
data = json.load(file)

#extracting all points
loc_complete = jmespath.search("loc", data)

# extracting into json format
for i in range(module_no-1):

    txt_file.write("############\n")
    txt_file.write("# Module "+str(i+1)+" #\n")
    txt_file.write("############\n\n")

    for j in range(int(total_num_of_points/(module_no-1))):
        current_loc = generate_next_location(prev_loc)
        current = {
            "location_tag": current_loc,
            "position": {
                "x": points[i][0],
                "y": points[i][1],
                "z": 0.0
            },
            "orientation": {
                "yaw": orientations[i]
            }
        }
        loc.append(current)
        prev_loc = current_loc

        txt_file.write("p_"+get_shelf(current_loc)+" = Point("+str(points[i][0])+", "+str(points[i][1]+j)+")\n")

        if j==0:

            # adding changing point to output for GeoGebra
            initial_points.append(current_loc)
            txt_file.write("p_"+get_shelf(current_loc)+".color = '#55aaaa'\n\n")

            # storing difference value from measured
            x_diff = abs(points[i][0] - jmespath.search("loc["+str(i)+"].position.x", data))
            y_diff = abs(points[i][1] - jmespath.search("loc["+str(i)+"].position.y", data))

            differences.append([x_diff, y_diff, math.sqrt(x_diff**2 + y_diff**2)])

            # printing differences
            print("\nDifference values for location tag "+str(initial_points[i]))
            print("x-difference: "+str(differences[i][0]))
            print("y-difference: "+str(differences[i][1]))
            print("total-difference: "+str(differences[i][2]))

    # adding changing point to output for GeoGebra
    final_points.append(current_loc)
    txt_file.write("p_"+get_shelf(current_loc)+".color = '#55aaaa'\n\n")

# adding the final point to loc
current = {
    "location_tag": generate_next_location(prev_loc),
    "position": {
        "x": finish_x,
        "y": finish_y,
        "z": 0.0
    },
    "orientation": {
        "yaw": convert_quaternon(0.0, 0.0, finish_z, finish_w)
    }
}
loc.append(current)
extract = {"loc": loc}

with open("Python/Arvato/output.json", "w") as outfile: #TODO: change with respect to system setup
    json.dump(extract, outfile, indent=4)

x_diff = abs(finish_x - jmespath.search("loc["+str(i)+"].position.x", data))
y_diff = abs(finish_y - jmespath.search("loc["+str(i)+"].position.y", data))

differences.append([x_diff, y_diff, math.sqrt(x_diff**2 + y_diff**2)])

txt_file.write("########################\n")
txt_file.write("# Final Configurations #\n")
txt_file.write("########################\n\n")

# generating the initial points
txt_file.write("p_initial_bottom = Point("+str(start_x-x_inc)+", "+str(m*(start_x-x_inc)+b)+")\n")
txt_file.write("p_initial_top = Point("+str(start_x-x_inc)+", "+str(m*(start_x-x_inc)+b+int(total_num_of_points/(module_no-1))-1)+")\n\n")

txt_file.write("p_initial_bottom.color = '#aa55aa'\n")
txt_file.write("p_initial_top.color = '#aa55aa'\n\n")

txt_file.write("bottom_initial = Segment(p_initial_bottom, p_"+str(get_shelf(initial_points[0]))+")\n")
txt_file.write("top_initial = Segment(p_initial_top, p_"+str(get_shelf(final_points[0]))+")\n")

# generating the initial points
txt_file.write("p_final_bottom = Point("+str(finish_x+x_inc)+", "+str(m*(finish_x+x_inc)+b)+")\n")
txt_file.write("p_final_top = Point("+str(finish_x+x_inc)+", "+str(m*(finish_x+x_inc)+b+int(total_num_of_points/(module_no-1))-1)+")\n\n")

txt_file.write("p_final_bottom.color = '#aa55aa'\n")
txt_file.write("p_final_top.color = '#aa55aa'\n\n")

txt_file.write("bottom_final = Segment(p_final_bottom, p_"+str(get_shelf(initial_points[-1]))+")\n")
txt_file.write("top_final = Segment(p_final_top, p_"+str(get_shelf(final_points[-1]))+")\n")

# creating segment and difference output for GeoGebra
for i in range(len(initial_points)-1):

    # adding segments
    txt_file.write("\nbottom_"+str(i)+" = Segment(p_"+str(get_shelf(initial_points[i]))+", p_"+str(get_shelf(initial_points[i+1]))+")\n") 
    txt_file.write("top_"+str(i)+" = Segment(p_"+str(get_shelf(final_points[i]))+", p_"+str(get_shelf(final_points[i+1]))+")\n\n") 

    # printing differences
    txt_file.write("print('Difference values for location tag "+str(initial_points[i])+"')\n")
    txt_file.write("print('x-difference: "+str(differences[i][0])+"')\n")
    txt_file.write("print('y-difference: "+str(differences[i][1])+"')\n")
    txt_file.write("print('total-difference: "+str(differences[i][2])+"')\n")
    txt_file.write("print()\n")

txt_file.close()
file.close()

print("\nExtracted "+ str(total_num_of_points+1) + " points into output.json")
