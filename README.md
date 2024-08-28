# Point Generator Repository ReadME
The repository consists of a point generator algorithm for three different warehouses and one for general application. This repository was written for Bottobo Robotics.

The common logic in all of them consists of generating equidistant locations given a certain amount of locations that are collected manually and are given in a json file. All versions of the code outputs the relevant locations into a separate json file and other formats as necessary.

## Specifications of the Different Algorithms
### General
This version inputs any number of points and fills in the locations between with points based on the SAP Location format. Each pair of adjacent points are taken and the line between is calculated. Then the x-values are updated based on the number of points between the two points and the generated x-values are then used to generate the y-values using the formula of the line. Finally, the orientation values are updated linearly without particular attention as the orientations change linearly. The orientations are then returned as yaw.

The General folder contains 3 files:
1. 2.json: contains the input information.
2. generator.py: is the main Python code file. There are *two instances* labelled with a comment starting with *TODO* that requires changing with respect to the system setup.
3. sample.json: is the output file in which the code writes the given and generated files in order.
   
### Arvato
### Pepsico
### Konya
