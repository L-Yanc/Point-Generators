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

The Pepsico folder contains 9 files:
1. 1.json, 3.json, 4.json: are the input files containing different variations to try. 1.json and 4.json contain 1 aisle and 3.json contains 4 aisles.
2. depo_info.json: is also an input file where the warehouse specifications are made. The explanations of the parameters passed through here can be found inside the pepsico_generator.py and pepsico_generator_no_palette.py files as comments where the parameters are extracted from json. *Important note*: the code will run as many aisles and columns specified here, regardless of whether the input json file contains more points. Hence it is important to ensure the data here matches the location inputs.
3. geoGebra.txt: is the GeoGebra output. This is a text file that can directly be copied and pasted into "https://geogebra.org/python/index.html" to visualize the output of the code.
4. output.json: is the output file in which the code writes the generated points in order.
5. output.xlsx: is also an output file where the points can be seen with all of their parameters in a spreadsheet format.
6. pepsico_generator_no_palette.py: **This is the most updated version of the Pepsico code** and only generates the points into all of the output formats. There are **five instances** labelled with a comment starting with **TODO** that requires changing with respect to the system setup.
7. pepsico_generator.py: This is a separate attempt file that works in the same principle and works the same as the no_palette version barring some small fixes. However, this version tries to output the shapes of the palettes for better visualization into GeoGebra and is yet to be completed.

### Konya
The final version is prepared for a demonstration in Konya and is also a general version. This version is also for the palette robot and generates points at a distance from the main line provided. This version also only generates one aisle. This one works by taking the initial points and generating the start and finish locations for the robot by shifting them as specified by the buffer and the horizontal length of the palette. Then the intermediate points are generated by dividing the space into equidistant pieces, similar to the General and Arvato versions. The points are then output to json and geoGebra, as in prior versions.

The Konya folder contains 6 files:
1. 2.json, 5.json: are input files with different variations. 2.json contains actual coordinates from a warehouse and 5.json is a trial version.
2. depo_info.json: is also an input file where the warehouse specifications are made. The explanations of the parameters passed through here can be found inside the pepsico_generator.py and pepsico_generator_no_palette.py files as comments where the parameters are extracted from json.
3. geoGebra.txt: is the GeoGebra output. This is a text file that can directly be copied and pasted into "https://geogebra.org/python/index.html" to visualize the output of the code.
4. konya_generator.py: is the main Python code file. There are **four instances** labelled with a comment starting with **TODO** that requires changing with respect to the system setup.
5. output.json: is the output file in which the code writes the generated points in order.

