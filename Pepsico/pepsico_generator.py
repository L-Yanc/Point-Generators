import json
import jmespath
import numpy as np
import math
import pandas as pd

# generating yaw value from quaternon
def convert_quaternon(x: float, y: float, z: float, w: float) -> float:
    return math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))

# finding b value from point and slope of perpendicular line for GeoGebra
def find_b(m: float, x: float, y: float) -> float:
    return (y-x*m)

# generating location code
def get_location(row: int, col: int, aisle: int, dir: str) -> str:

    # formatting row and column
    row_s = str(row) if row >= 10 else ("0"+str(row))
    col_s = str(col) if col >= 10 else ("0"+str(col))

    output = str(aisle) + "-" + str(dir) + "-" + row_s + "-" + col_s
    
    # creating and returning location code
    return output

# generating next location code
def get_next_location(prev_loc: str, row_th: int, col_th: int, aisle_th: int) -> str:

    if prev_loc == "0":
        return "1-L-01-01"
    
    # splitting previous location to process
    split_loc = prev_loc.split("-")
    aisle = int(split_loc[0])
    dir = str(split_loc[1])
    row = int(split_loc[2])
    col = int(split_loc[3])

    # comparing thresholds
    if col >= col_th:
        if row >= row_th:
            if dir == 'L':
                dir = 'R'
                row = 1
                col = 1
            else:
                aisle = aisle + 1
                dir = "L"
                row = 1
                col = 1
        else:
            col = 1
            row = row + 1
    else:
        col = col + 1


    # putting the string back together
    return get_location(row, col, aisle, dir)

def get_prev_location(next_loc: str, row_th: int, col_th: int, aisle_th: int) -> str:

    if next_loc == "1-L-01-01":
        return "0"
    
    # splitting previous location to process
    split_loc = next_loc.split("-")
    aisle = int(split_loc[0])
    dir = split_loc[1]
    row = int(split_loc[2])
    col = int(split_loc[3])

    # comparing thresholds
    if col <= 1:
        col = col_th
        if row <= 1:
            row = row_th
            if dir == "R":
                dir = "L"
            else:
                if aisle <= 1:
                    aisle = aisle - 1
                else:
                    return "0"
                dir = "R"
        else:
            row = row - 1
    else:
        col = col - 1

    # putting the string back together
    return get_location(row, col, aisle, dir)

# generating necessary points from two end points
def generate_points(cols: int, rows: int, aisles: int, start_x: float, final_x: float, start_y: float, 
                    final_y: float, b: float, h_palette: float, start_w: float, start_z: float, 
                    final_z: float, final_w: float, prev_loc: str):

    # calculating best fit line for intial and final positions
    A = np.array([[start_x, 1], [final_x, 1]])
    B = np.array([start_y, final_y])
    x = np.linalg.solve(A, B)

    # extracting line information: slope(m) and linear constant(d)
    m = x[0]
    d = x[1] + b  # adding b to find the parallel line the robot will start on

    # initializing temp variables and points array
    current_x = start_x + c*2 + h_palette/2
    current_y = m * current_x + d
    current_w, current_z = start_w, start_z
    points = [[current_x, current_y]]
    loc = [prev_loc]
    orientations = [convert_quaternon(0.0, 0.0, start_z, start_w)]

    # determining orientation increments
    z_inc = (final_z-start_z)/cols/2
    w_inc = (final_w-start_w)/cols/2

    # generating points by iterating through columns
    for col in range(int(cols/2)-1):

        # generating position
        current_x = current_x + c + h_palette
        current_y = m * current_x + d
        points.append([current_x, current_y])

        # generating orientation
        current_z = current_z + z_inc
        current_w = current_w + w_inc
        orientations.append(convert_quaternon(0.0, 0.0, current_z, current_w))

        # generating location tag
        current_loc = get_next_location(prev_loc, rows, cols, aisles)
        loc.append(current_loc)
        prev_loc = current_loc

    return points, orientations, loc, m, d

# function to calculate 
def calculate_distance(point1, point2) -> float:
    return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)

# finding perpendicular line
def find_perpendicular(m: float, x: float, y: float) -> tuple[float, float]:
    m_inverse = -1/m
    b = m_inverse*x - y
    return m_inverse, b

# loading the json files
file = open('Python/Pepsico/depo_info.json')
data = json.load(file)
file.close()

file = open('Python/Pepsico/3.json')
locs = json.load(file)
file.close()

# extracting constants
a = jmespath.search("info[0].dimensions.a", data)                  # distance between rows
b = jmespath.search("info[0].dimensions.b", data)                  # distance between initial point and first column
c = jmespath.search("info[0].dimensions.c", data)                  # distance between columns
e = jmespath.search("info[0].dimensions.e", data)                  # horizontal length
h_palette = jmespath.search("info[0].dimensions.h_palette", data)  # horizontal length of palette
v_palette = jmespath.search("info[0].dimensions.v_palette", data)  # vertical length of palette
cols = jmespath.search("info[0].layout.cols", data)                # number of columns
rows = jmespath.search("info[0].layout.rows", data)                # number of rows
aisles = jmespath.search("info[0].layout.aisles", data)            # number of aisles
start_loc = jmespath.search("info[0].layout.start_loc", data)      # the location tag of the first position

# converting all constants to float
a, b, c, e, h_palette, v_palette =  float(a), float(b), float(c), float(e), float(h_palette), float(v_palette)
cols, rows, aisles = int(cols), int(rows), int(aisles)

# initializing storage arrays
positions = []
locations = []
orientations = []
loc = []
ms = []
ds = []
given_points = []

# setting up while loop to iterate through aisles
i, aisle_no = 0, 0
while aisle_no<aisles:

    # extracting initial position info
    start_x = jmespath.search("loc["+str(i)+"].position.x", locs)
    start_y = jmespath.search("loc["+str(i)+"].position.y", locs)
    start_w = jmespath.search("loc["+str(i)+"].orientation.w", locs)
    start_z = jmespath.search("loc["+str(i)+"].orientation.z", locs)

    # extracting middle position info
    middle_x = jmespath.search("loc["+str(i+1)+"].position.x", locs)
    middle_y = jmespath.search("loc["+str(i+1)+"].position.y", locs)
    middle_w = jmespath.search("loc["+str(i+1)+"].orientation.w", locs)
    middle_z = jmespath.search("loc["+str(i+1)+"].orientation.z", locs)

    # extracting final position info
    final_x = jmespath.search("loc["+str(i+2)+"].position.x", locs)
    final_y = jmespath.search("loc["+str(i+2)+"].position.y", locs)
    final_w = jmespath.search("loc["+str(i+2)+"].orientation.w", locs)
    final_z = jmespath.search("loc["+str(i+2)+"].orientation.z", locs)

    # updating i for next iteration
    i = i+3
    aisle_no = aisle_no+1

    # updating the first location ensure the correct aisle is selected
    prev_loc = str(aisle_no) + "-L-01-01" 
    
    # generating points from start and middle positions
    p1, o1, l1, m1, d1 = generate_points(cols, rows, aisles, start_x, middle_x, start_y, middle_y, b, 
                                 h_palette, start_w, start_z, middle_z, middle_w, prev_loc)
    
    prev_loc = get_next_location(l1[-1], rows, cols, aisles)

    # generating points from middle and final positions
    p2, o2, l2, m2, d2 = generate_points(cols, rows, aisles, middle_x, final_x, middle_y, final_y, b,
                                 h_palette, middle_w, middle_z, final_z, final_w, prev_loc)
    
    prev_loc = l2[-1]

    # storing points
    positions = positions + p1 + p2
    orientations = orientations + o1 + o2
    locations = locations + l1 + l2
    ms.append(m1)
    ms.append(m2)
    ds.append(d1)
    ds.append(d2)
    given_points.append([[start_x, start_y], [middle_x, middle_y], [final_x, final_y]])

    # flipping b's sign to make sure the R-L balance is secured
    b = -1 * b

# formatting points for json extraction
for p in range(len(positions)):
    current = {
        "location": locations[p],
        "position": {
            "x": positions[p][0],
            "y": positions[p][1],
            "z": 0.0
        },
        "orientation": {
            "yaw": orientations[p]
        }
    }
    loc.append(current)

# extracting json
extract = {"loc": loc}

with open("Python/Pepsico/output.json", "w") as outfile:
    json.dump(extract, outfile, indent=4)

# extracting excel
df = pd.json_normalize(loc)
excel_file = 'Python/Pepsico/output.xlsx'
df.to_excel(excel_file, index=False)

############################
# extracting txt for GeoGebra
txt_file = open('Python/Pepsico/geoGebra.txt', 'w')

# writing output for every aisle
for i in range(aisles):

    txt_file.write("##############\n# Aisle No: "+str(i+1)+"\n##############\n\n")

    # creating temp variable for position index
    p_idx = i*6

    # extracting values
    p_start = given_points[i][0]
    p_middle = given_points[i][1]
    p_final = given_points[i][2]

    # writing given points in file
    txt_file.write("P_start_"+str(i)+" = Point("+str(p_start[0])+","+str(p_start[1])+")\n")
    txt_file.write("P_middle_"+str(i)+" = Point("+str(p_middle[0])+","+str(p_middle[1])+")\n")
    txt_file.write("P_final_"+str(i)+" = Point("+str(p_final[0])+","+str(p_final[1])+")\n\n")

    # writing generated points in file
    txt_file.write("P"+str(i)+"_1 = Point("+str(positions[p_idx][0])+", "+str(positions[p_idx][1])+")\n")
    txt_file.write("P"+str(i)+"_2 = Point("+str(positions[p_idx+1][0])+", "+str(positions[p_idx+1][1])+")\n")
    txt_file.write("P"+str(i)+"_3 = Point("+str(positions[p_idx+2][0])+", "+str(positions[p_idx+2][1])+")\n")
    txt_file.write("P"+str(i)+"_4 = Point("+str(positions[p_idx+3][0])+", "+str(positions[p_idx+3][1])+")\n")
    txt_file.write("P"+str(i)+"_5 = Point("+str(positions[p_idx+4][0])+", "+str(positions[p_idx+4][1])+")\n")
    txt_file.write("P"+str(i)+"_6 = Point("+str(positions[p_idx+5][0])+", "+str(positions[p_idx+5][1])+")\n\n")

    # generating colors
    given_point_color = str(hex((i+1)*11100)).split("x")[1]
    generated_point_color = str(hex((i+1)*11111)).split("x")[1]

    while len(given_point_color)<6:
        given_point_color = given_point_color + "b"

    while len(generated_point_color)<6:
        generated_point_color = generated_point_color + "b"

    # editing point properties
    txt_file.write("P"+str(i)+"_1.color = '#"+str(generated_point_color)+"'\n")
    txt_file.write("P"+str(i)+"_2.color = '#"+str(generated_point_color)+"'\n")
    txt_file.write("P"+str(i)+"_3.color = '#"+str(generated_point_color)+"'\n")
    txt_file.write("P"+str(i)+"_4.color = '#"+str(generated_point_color)+"'\n")
    txt_file.write("P"+str(i)+"_5.color = '#"+str(generated_point_color)+"'\n")
    txt_file.write("P"+str(i)+"_6.color = '#"+str(generated_point_color)+"'\n\n")

    txt_file.write("P_start_"+str(i)+".color = '#"+str(given_point_color)+"'\n")
    txt_file.write("P_middle_"+str(i)+".color = '#"+str(given_point_color)+"'\n")
    txt_file.write("P_final_"+str(i)+".color = '#"+str(given_point_color)+"'\n\n")

    # generating line segments to represent palettes lines
    txt_file.write("segment_start_middle_"+str(i)+" = Segment(P_start_"+str(i)+", P_middle_"+str(i)+")\n")
    txt_file.write("segment_middle_final_"+str(i)+" = Segment(P_middle_"+str(i)+", P_final_"+str(i)+")\n\n")

    # printing relevant distances
    txt_file.write("print('Distance between start and middle for aisle "+str(i+1)+": ")
    txt_file.write(str(calculate_distance(p_start, p_middle))+" cm')\n")
    txt_file.write("print('Distance between middle and final for aisle "+str(i+1)+": ")
    txt_file.write(str(calculate_distance(p_middle, p_final))+" cm')\n")
    txt_file.write("print()\n\n")

    txt_file.write("##############\n# Printing Palettes\n\n")

    # generating points to represent palettes
    ref_point = [p_start[0]+c, p_start[1]]

    # finding angles of the two sections
    theta = [math.atan2(p_start[1]-p_middle[1], p_start[0]-p_middle[0]), math.atan2(p_middle[1]-p_final[1], p_middle[0]-p_final[0])]

    # iterating through columns
    for col in range(cols):

        colIdx = int(col/3)

        # identifying the lower corners of the palette
        lb_left = [math.sqrt(4*c**2/((ms[colIdx])**2+1))+ref_point[0], math.sqrt(4*c**2/((ms[colIdx]+1))**2)*ms[colIdx]+ref_point[1]]
                
        # finding the line perpendicular to the lower left corner
        m, d = find_perpendicular(ms[colIdx], lb_left[0], lb_left[1])
        
        

        # adding a line through the middle of the palette
        midpoint_x = lb_left[0] + h_palette/2 * math.cos(theta)
        midpoint_y = midpoint_x*ms[colIdx] + ds[colIdx]
        midpoint_lb = [midpoint_x, midpoint_y]
        
        midpoint_x = ub_left[0] + h_palette/2 * math.cos(theta)
        midpoint_y = midpoint_x*ms[colIdx] + ds[colIdx]
        midpoint_ub = [midpoint_x, midpoint_y]

        # creating points for the line segments in the txt output
        txt_file.write("lb_left_"+str(i)+"_"+str(col)+" = Point("+str(lb_left[0])+", "+str(lb_left[1])+")\n")
        txt_file.write("lb_right_"+str(i)+"_"+str(col)+" = Point("+str(lb_right[0])+", "+str(lb_right[1])+")\n")
        txt_file.write("ub_left_"+str(i)+"_"+str(col)+" = Point("+str(ub_left[0])+", "+str(ub_left[1])+")\n")
        txt_file.write("ub_right_"+str(i)+"_"+str(col)+" = Point("+str(ub_right[0])+", "+str(ub_right[1])+")\n\n")
        txt_file.write("lb_middle_"+str(i)+"_"+str(col)+" = Point("+str(midpoint_lb[0])+", "+str(midpoint_lb[1])+")\n")
        txt_file.write("ub_middle_"+str(i)+"_"+str(col)+" = Point("+str(midpoint_ub[0])+", "+str(midpoint_ub[1])+")\n\n")
        
        # creating the line segments
        txt_file.write("palette_"+str(i)+"_"+str(col)+"_top = Segment(ub_right_"+str(i)+"_"+str(col)+", ub_left_"+str(i)+"_"+str(col)+")\n")
        txt_file.write("palette_"+str(i)+"_"+str(col)+"_bottom = Segment(lb_right_"+str(i)+"_"+str(col)+", lb_left_"+str(i)+"_"+str(col)+")\n")
        txt_file.write("palette_"+str(i)+"_"+str(col)+"_left = Segment(lb_left_"+str(i)+"_"+str(col)+", ub_left_"+str(i)+"_"+str(col)+")\n")
        txt_file.write("palette_"+str(i)+"_"+str(col)+"_right = Segment(ub_right_"+str(i)+"_"+str(col)+", lb_right_"+str(i)+"_"+str(col)+")\n\n")
        txt_file.write("palette_"+str(i)+"_"+str(col)+"_mid = Segment(lb_middle_"+str(i)+"_"+str(col)+", ub_middle_"+str(i)+"_"+str(col)+")\n\n")

        # coloring segments
        txt_file.write("palette_"+str(i)+"_"+str(col)+"_mid.color = '#aaaaaa'\n\n")

        ref_point = lb_right if col != (cols/2-1) else [p_middle[0]+c, p_middle[1]]
    

txt_file.close()
############################

print("Extracted " + str(len(orientations)) + " points successfully")