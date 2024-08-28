# Point Generator Repository ReadME
The repository consists of a point generator algorithm for three different warehouses and one for general application. This repository was written for Bottobo Robotics.

The common logic in all of them consists of generating equidistant locations given a certain amount of locations that are collected manually and are given in a json file. All versions of the code outputs the relevant locations into a separate json file and other formats as necessary.

## How To Use
The code should work in any system setup after the following steps:
- Ensuring Python 3 is installed and is updated.
- Ensuring the "json", "jmespath", "numpy", "math" and "pandas" packages are downloaded and are useable.
- Ensuring Microsoft Excel or equivalent is downloaded and usable (this is not necessary for the code to run but is necessary to view the generated .xlsx files)
- Changing the lines marked with "**TODO**" in .py files are changed to the correct path according to the system setup.

## Specifications of the Different Algorithms
### General
This version inputs any number of points and fills in the locations between with points based on the SAP Location format. Each pair of adjacent points are taken and the line between is calculated. Then the x-values are updated based on the number of points between the two points and the generated x-values are then used to generate the y-values using the formula of the line. Finally, the orientation values are updated linearly without particular attention as the orientations change linearly. The orientations are then returned as yaw.

The General folder contains 3 files:
1. 2.json: contains the input information.
2. generator.py: is the main Python code file. There are **two instances** labelled with a comment starting with **TODO** that requires changing with respect to the system setup.
3. sample.json: is the output file in which the code writes the given and generated points in order.
   
### Arvato
The Arvato version is a modified version of the general code. The division principle is the same to generate a certain amount of points between two given points, however this version only generates one aisle that is divided into sections. The number of modules, the location tag of the initial and final shelves, and the aisle number are taken from the user. Then the amount of points is calculated based on the start and end shelf numbers and are grouped to have as many distinct locations as dictated by the number of modules. The generated points are then output to json and a GeoGebra python format for visualization.

The Arvato folder contains 5 files:
1. 14_complete.json: contains the actual full location list taken from the warehouse for testing of the code. Is otherwise not used within the code.
2. 14.json: the input locations for the 14th aisle as used by the code.
3. arvato_generator.py: is the main Python code file. There are **four instances** labelled with a comment starting with **TODO** that requires changing with respect to the system setup.
4. geoGebra.txt: is the GeoGebra output. This is a text file that can directly be copied and pasted into "https://geogebra.org/python/index.html" to visualize the output of the code.
5. output.json:  is the output file in which the code writes the generated points in order.

### Pepsico
This version of the code is for the robot that can carry palettes and is hence generating points that are at a certain distance from the initial points given. This version uses the desired spacing of the palettes taken from the depo_info.json file to generate the points at the distance required. It takes three points per aisle and divides it into two sections and outputs the desired number of columns (which is the number of palettes). Unlike the previous versions, the generated points depend on their distance from the initial point and the desired space between the palettes, making the output slightly askew as the points do not depend on both points.

The Pepsico version contains 

### Konya
