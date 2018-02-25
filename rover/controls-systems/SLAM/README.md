# SLAM CONCEPT STRUCTURE

### REQUIRED DOWNLOADS
The required download for openGL structure is Glew and FreeGlut to compliment the openGL system with assistance. These openGL extensions can be downloaded within visual studio’s manage packet segment or can be downloaded via Internet. Simplified required downloads annotation is listed below:

Glew
FreeGlut

### REQUIRED HEADINGS
The required headings are on par with the required installation segments.
The required headings have to be in order for it to work properly with openGL. The heading order is demonstrated below with the required downloaded assistance.
#include "GL\glew.h"
#include "GL\freeglut.h"

### OPENGL DRAWING CONCEPT(S)

OpenGL uses polygon and vertex rendering to apply triangle shapes to compute complex objects as a drawn or rendered model(s). These concepts require additional knowledge of calculus and physics to demonstrate a 3D plain that involves <x,y,z> with optimal addition to t as time if needed.

### DYNAMIC RENDERING

Dynamic rendering will be a concept of visually placing static objects into the vertex grid to align with the incoming lidar data. The rendering of the dynamic structure or rather shape is coherent at its early stages as initial scale and accuracy is more abstract to follow. The dynamic rendering will be presented with variety of functions that will make up with original data rendering possible.
###### Example function:
vector<size_t>dynamic_render(size_t x, size_t y);
vector<size_t>dynamic_scale(size_t x, size_t y);

###### Complimentary function:
void static_object(int object_index);

As the dynamic rendering inherits more complexity, the overall rendering performance would need to be simplified. The hardware power and performance can also affect the outcome of the rending and the mapping of the plane.

### STATIC OBJECTS

Static objects are pre-rendered mesh objects that will speed up abstract display of the data that will be presented by the lidar. At initial construction, the simpler the object is the better accuracy of scale distance can be measured. These can be very helpful as a solid measurement point with vertex points to read accurate data off. 
Another concept addition to static object mesh rendering is the pixilation and the hardware concurrency towards the performance and viability of the overall structure. As an early stage prototype, less scaled pixel meshed objects are more desirable to view as an initial stage correlation to build upon the structure itself.
OpenGL functions with vertex points and eventually a triangle is a basis of all the static objects. A predetermined object relations can be researched further and development into production, but as a suggestion simple shapes will lead to better performance and accuracy.

### SCALE ACCURACY AND RENDERING

Scale accuracy and rendering would need to be discussed and measured throughout the testing of the data. Additional suggestion of the scaling would be a top-down 2-D manifested environment that can be created in a suggested paradigm.
Rendering in OpenGL can be active and translated through active files or pipelining of data from one source to another. Further research is required for drawing and rending active post-data rendering. Current additional rendering can be static and rough with initial prototype paradigm.

### MAZE CONCEPT

Initial concept suggestion of maze generation algorithm with additional maze solving algorithms. Since the environment will most likely generate a maze-like paradigm, similar solutions of solving the problem can be inherited through substitution.


### Suggested Algorithms:

Dijkstra's Algorithm
Prim-Jarnik Algorithm
BFS-DFS Algorithm
A-Star Algorithm
Additional Reading Material:
http://www.astrolog.org/labyrnth/algrithm.htm

### Notes:

viewFrustrumClipping; -Speed up rendering/camera
Jetson TX2- Model
Jetson TX2 – Has pascal architecture (research needed)
Schematics for NVIDIA – Under schematics in github  for 2018

