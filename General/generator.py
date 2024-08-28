import json
import jmespath
import numpy as np
import math

#generating new location based on previous SAP_Location
def generate_SAP_Location(prev_loc: str, aisle_th: int, shelf_th: int) -> str:

    #splitting String
    split_loc = prev_loc.split("-")
    section_num = int(split_loc[0])
    aisle_num = int(split_loc[2])
    shelf_num = int(split_loc[3])

    #comparing thresholds
    if shelf_num >= shelf_th:
        if aisle_num >= aisle_th:
            section_num = section_num + 1
            aisle_num = 1
            shelf_num = 1
        else:
            aisle_num = aisle_num + 1
            shelf_num = 1
    else:
        shelf_num = shelf_num + 1    

    #putting the string back together
    return ("0" + str(section_num) + "--" + str(aisle_num) + "-" + str(shelf_num))

#generating yaw value from quaternon
def convert_quaternon(x: float, y: float, z: float, w: float) -> float:
    return math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))


#loading the json file
file = open('Python/General/2.json')
data = json.load(file)

#extracting all points
loc = jmespath.search("loc", data)

#initializing arrays
SAP_Locations = []
points = []
orientation = []

#initializing the total number of points
total_num_of_points = 2

for l in range(len(loc)-1):

    #converting indices to strings to use in indexing
    idx0 = str(l)
    idx1 = str(l+1)

    #extracting position data
    start_x = jmespath.search("loc["+idx0+"].position.x", data)
    start_y = jmespath.search("loc["+idx0+"].position.y", data)
    end_x = jmespath.search("loc["+idx1+"].position.x", data)
    end_y = jmespath.search("loc["+idx1+"].position.y", data)

    #extracting orientation data
    start_z = jmespath.search("loc["+idx0+"].orientation.z", data)
    start_w = jmespath.search("loc["+idx0+"].orientation.w", data)
    end_z = jmespath.search("loc["+idx1+"].orientation.z", data)
    end_w = jmespath.search("loc["+idx1+"].orientation.w", data)

    #extracting SAP_location data
    start_SAP = jmespath.search("loc["+idx0+"].SAP_Location", data)
    end_SAP = jmespath.search("loc["+idx1+"].SAP_Location", data)

    #initializing location arrays and temp variables
    if l==0:
        SAP_Locations.append(start_SAP)
        points.append([start_x, start_y])
        orientation.append(convert_quaternon(0.0, 0.0, start_z, start_w))

    current_loc = start_SAP
    num_of_points = 0

    #setting thresholds for section, aisle, and shelf
    aisle_th = 5
    shelf_th = 2

    #creating and storing SAP Locations
    while current_loc != end_SAP:
        current_loc = generate_SAP_Location(current_loc, aisle_th, shelf_th)
        SAP_Locations.append(current_loc)
        num_of_points = num_of_points + 1

    #finding line between the start and end positions
    A = np.array([[start_x, 1], [end_x, 1]])
    b = np.array([start_y, end_y])
    x = np.linalg.solve(A, b)

    #extracting slope(m) and linear constant(b)
    m = x[0]
    b = x[1]

    #calculating the x, z and w increments
    x_inc = (end_x-start_x)/num_of_points
    z_inc = (end_z-start_z)/num_of_points
    w_inc = (end_w-start_w)/num_of_points

    #iterating through points
    for i in range(num_of_points):

        #calculating x and y values for each point
        current_x = start_x + i*x_inc
        current_y = m*current_x + b
        points.append([current_x, current_y])

        #calculating orientation for each point
        current_z = start_z + i*z_inc
        current_w = start_w + i*w_inc
        current_yaw = convert_quaternon(0.0, 0.0, current_z, current_w)
        orientation.append(current_yaw)

    total_num_of_points = total_num_of_points + num_of_points

#closing json file
file.close()

#initializing loc array to dump into json
loc = []

#extracting into json format
for i in range(total_num_of_points-1):
    current = {
        "SAP_Location": SAP_Locations[i],
        "position": {
            "x": points[i][0],
            "y": points[i][1],
            "z": 0.0
        },
        "orientation": {
            "yaw": orientation[i],
        }
    }
    loc.append(current)

extract = {"loc": loc}

with open("Python/General/sample.json", "w") as outfile:
    json.dump(extract, outfile, indent=4)

print("Extracted "+ str(total_num_of_points) + " points into sample.json")