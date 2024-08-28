import json
import jmespath
import math
import numpy as np

# Function to convert quaternion to yaw
def convert_quaternion(x: float, y: float, z: float, w: float) -> float:
    return math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))

# Load JSON function
def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to calculate distance between two points
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Function to generate equidistant points on a parallel line
def generate_parallel_points(start_x, start_y, final_x, final_y, palette_num, vertical_dist, buffer, h_palette):

    # Calculate the direction vector (from start to final)
    dx = final_x - start_x
    dy = final_y - start_y
    line_length = math.sqrt(dx ** 2 + dy ** 2)
    
    # Unit vector of the line
    ux = dx / line_length
    uy = dy / line_length
    
    # Normal vector (perpendicular to the line)
    normal_x = -uy
    normal_y = ux
    
    # Adjust normal vector by vertical_dist (accounting for positive or negative)
    offset_x = normal_x * abs(vertical_dist) * (-1 if vertical_dist < 0 else 1)
    offset_y = normal_y * abs(vertical_dist) * (-1 if vertical_dist < 0 else 1)
    
    # First and last points considering buffer and h_palette/2
    initial_point = (
        start_x + buffer * ux + (h_palette / 2) * ux + offset_x,
        start_y + buffer * uy + (h_palette / 2) * uy + offset_y
    )
    final_point = (
        final_x - buffer * ux - (h_palette / 2) * ux + offset_x,
        final_y - buffer * uy - (h_palette / 2) * uy + offset_y
    )
    
    # Distance between initial and final points
    total_dist = calculate_distance(initial_point[0], initial_point[1], final_point[0], final_point[1])
    
    # Calculate the space between each point
    space = total_dist / (palette_num - 1)
    
    points = []
    for i in range(palette_num):
        
        # Calculate each point's position along the parallel line
        point_x = initial_point[0] + i * space * ux
        point_y = initial_point[1] + i * space * uy
        points.append((point_x, point_y))
    
    return points

# Main function to generate points and save them to a JSON file
def main():

    # Load JSON files
    data = load_json('Python/Konya/depo_info.json') #TODO: change with respect to system setup
    locs = load_json('Python/Konya/2.json')         #TODO: change with respect to system setup

    # Extracting constants from JSON
    vertical_dist = float(jmespath.search("info[0].dimensions.vertical_dist", data))  # distance at which the robot will stop
    buffer = float(jmespath.search("info[0].dimensions.buffer", data))                # buffer for the initial and final points
    h_palette = float(jmespath.search("info[0].dimensions.h_palette", data))          # horizontal length of palette (cm)
    palette_num = int(jmespath.search("info[0].layout.palette_num", data))            # number of palettes

    # Extracting initial and final position info from JSON
    start_x = float(jmespath.search("loc[0].position.x", locs))
    start_y = float(jmespath.search("loc[0].position.y", locs))
    start_z = float(jmespath.search("loc[0].orientation.z", locs))
    start_w = float(jmespath.search("loc[0].orientation.w", locs))

    final_x = float(jmespath.search("loc[1].position.x", locs))
    final_y = float(jmespath.search("loc[1].position.y", locs))
    final_z = float(jmespath.search("loc[1].orientation.z", locs))
    final_w = float(jmespath.search("loc[1].orientation.w", locs))

    # Generate the points
    points = generate_parallel_points(start_x, start_y, final_x, final_y, palette_num, vertical_dist, buffer, h_palette)
    
    # Calculate the increments for z and w
    z_inc = (final_z - start_z) / (palette_num - 1)
    w_inc = (final_w - start_w) / (palette_num - 1)

    # Check if there is enough space to fit the palettes
    min_space = (palette_num - 1) * h_palette + (palette_num - 2) * buffer
    actual_space = calculate_distance(points[0][0], points[0][1], points[-1][0], points[-1][1])
    
    if actual_space < min_space:
        print("Not enough space to fit palettes")
        print(f"Distance required: {min_space} cm")
        print(f"Distance available: {actual_space} cm")
        return

    # Prepare the data for JSON output
    loc = []
    current_z = start_z
    current_w = start_w

    for point in points:

        yaw = convert_quaternion(0.0, 0.0, current_z, current_w)
        current = {
            "position": {
                "x": point[0],
                "y": point[1],
                "z": 0.0  # Assuming z-coordinate is 0.0 as in your previous setup
            },
            "orientation": {
                "yaw": yaw
            }
        }
        loc.append(current)
        
        # Update current_z and current_w for the next point
        current_z += z_inc
        current_w += w_inc

    extract = {"loc": loc}

    # Save to JSON file
    with open("Python/Konya/output.json", "w") as outfile: #TODO: change with respect to system setup
        json.dump(extract, outfile, indent=4)

    print(f"Extracted {len(points)} points successfully.")

    ############################
    
    # Extracting txt for GeoGebra
    txt_file = open('Python/Konya/geoGebra.txt', 'w')  #TODO: change with respect to system setup

    # Printing given points
    txt_file.write("P_start = Point("+str(start_x)+", "+str(start_y)+")\n")
    txt_file.write("P_final = Point("+str(final_x)+", "+str(final_y)+")\n\n")

    # Printing each point into txt
    for i in range(palette_num):
        txt_file.write("P_"+str(i)+" = Point("+str(points[i][0])+", "+str(points[i][1])+")\n")

    # Printing segments between given points
    txt_file.write("\nsegment = Segment(P_start, P_final)\n\n")

    txt_file.write("P_midpoint = Point("+str((start_x+final_x)/2)+", "+str((start_y+final_y)/2)+")\n\n")
    
    # Printing the distance between P_midpoint and P_1
    midpoint = ((start_x + final_x) / 2, (start_y + final_y) / 2)
    dist_to_p1 = calculate_distance(midpoint[0], midpoint[1], points[1][0], points[1][1])
    txt_file.write("segment_midpoint_to_P1 = Segment(P_midpoint, P_1)\n\n")
    txt_file.write(f"print('Distance_midpoint_to_P1 = {dist_to_p1} cm')\n")

    txt_file.close()
    
    ############################

# Run the main function
main()