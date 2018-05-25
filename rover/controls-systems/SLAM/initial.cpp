// SLAM-Basic-Maze.cpp : Defines the entry point for the console application.
//
//export CPLUS_INCLUDE_PATH="$CPLUS_INCLUDE_PATH:/usr/include/python2.7/"
//g++ initial.cpp -o testgl -lGL -lglut -lglfw -lGLEW -lGLU -std=c++11 -lboost_python -lpython2.7 -lboost_system -lboost_thread -lpthread
//export DISPLAY=localhost:0.0
//
#ifdef __APPLE_CC__
#include <GLUT/glut.h>
#else
#include <GL/glut.h>
#endif
#include <algorithm>
#include <omp.h>
#include <string>
#include <iomanip>
#include <iostream>
#include <vector>
#include <atomic>
#include <mutex>
#include <math.h>
#include <sstream>
#include <chrono>
#include <boost/python.hpp>

using namespace std;
using namespace boost::python;

int flag_tennis = 0;
int flag_obs    = 0;
bool auto_path  = false;

#define earthRadiusKm 6371.0
std::vector<double> _lat_incoming; //Incoming lat GPS coordinates
std::vector<double> _lon_incoming; //Incoming lon GPS coordinates
size_t incoming_index = 0;

std::vector<double> _distance_vector;

std::vector<double> _distance_x;
std::vector<double> _distance_z;

vector<double> _lat_outgoing;//Outgoing GPS coordinates
vector<double> _lon_outgoing;//Outgoing GPS coordinates
size_t outgoing_index = 0;

//CSUF test coordinates
double lat_points[4] = {33.88239, 33.882513, 33.882434, 33.88245};
double lon_points[4] = {-117.883568, -117.88607751, -117.8835028, -117.883660};

double _angle_; // Global Calculations
double _distance_; // Global Calculations

/* @param temp_lat
 * 		the latitudinal points coming in from deepstream
 */
void set_lat(double temp_lat)
{
	_lat_incoming.push_back(temp_lat);  	
}

/* @param temp_lon
 * 		the longitudinal points coming from deepstream 
 */
void set_lon(double temp_lon)
{
	_lon_incoming.push_back(temp_lon);
}

// This function converts decimal degrees to radians
double deg2rad(double deg) 
{
  return (deg * M_PI / 180);
}

//  This function converts radians to decimal degrees
double rad2deg(double rad) 
{
  return (rad * 180 / M_PI);
}

/**
 * Returns the distance between two points on the Earth.
 * Direct translation from http://en.wikipedia.org/wiki/Haversine_formula
 * @param lat1d Latitude of the first point in degrees
 * @param lon1d Longitude of the first point in degrees
 * @param lat2d Latitude of the second point in degrees
 * @param lon2d Longitude of the second point in degrees
 * @return The distance between the two points in kilometers
 */
double distanceEarth(double lat1d, double lon1d, double lat2d, double lon2d) 
{
	double lat1r, lon1r, lat2r, lon2r, u, v;
	lat1r = deg2rad(lat1d);
	lon1r = deg2rad(lon1d);
	lat2r = deg2rad(lat2d);
	lon2r = deg2rad(lon2d);
	u = sin((lat2r - lat1r)/2);
	v = sin((lon2r - lon1r)/2);
	return 2.0 * earthRadiusKm * asin(sqrt(u * u + cos(lat1r) * cos(lat2r) * v * v));
}

//As latitude and longitude are usually expressed in degrees, do not forget to convert them to radians before using this function
double angleFromCoordinate(double lat1, double long1, double lat2,
        double long2) 
{
  
    double dLon = (long2 - long1);

    double y = sin(dLon) * cos(lat2);
    double x = cos(lat1) * sin(lat2) - sin(lat1)
             * cos(lat2) * cos(dLon);

    double brng = atan2(y, x);
    brng = rad2deg(brng);
    brng = fmod((brng + 360), 360);  
    brng = 360 - brng; // count degrees counter-clockwise - remove to make clockwise

    return brng;
}

struct _openGL_CAMERA_VALUES_
{
	// angle of rotation for the camera direction
	GLfloat angle = 0.0f;
	// actual vector representing the camera's direction
	GLfloat lx = 0.0f, lz = -1.0f, ly = 0.0f;
	// XZ position of the camera
	GLfloat x = 0.0f, z = 5.0f, y = 1.75f;
}_openGLCV_;


struct _openGL_KEY_STATES_
{
	// the key states. These variables will be zero
	//when no key is being presses
	GLfloat deltaAngle = 0.0f;
	GLfloat deltaMove = 0;
	GLint xOrigin = -1;
}_openGLKS_;


struct _openGL_MAINWINDOW_VALUES_
{
	// width and height of the window
	GLint height;
	GLint width;
	// variables to hold window identifiers
	GLint mainWindow;
	GLint TopDownWindow;
	GLint TopPanelWindow;
	//border between subwindows
	GLint border = 6;
}_openGLMV_;


struct _openGL_ROVER_TRACKING_
{
	std::vector<double> past_x;
	std::vector<double> past_z;

	std::vector<double> past_track_x;
	std::vector<double> past_track_z;

}_openGLRT_;

struct _openGL_ROVER_LINE_TRACKING_
{
	std::vector<double> line_x;
	std::vector<double> line_z;
}_openGLRLT_;

std::vector<GLfloat> past_x;
std::vector<GLfloat> past_y;
std::vector<GLfloat> past_z;

void setProjection(GLint w1, GLint h1)
{
	GLfloat ratio;
	// Prevent a divide by zero, when window is too short
	// (you cant make a window of zero width).
	ratio = (1.0f * w1 / h1);
	// Reset the coordinate system before modifying
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();

	// Set the viewport to be the entire window
	glViewport(0, 0, w1, h1);

	// Set the clipping volume
	gluPerspective(45, ratio, 0.1, 1000);
	glMatrixMode(GL_MODELVIEW);

}

void changeSize(GLint w1, GLint h1)
{
	if (h1 == 0) { h1 = 1; }

	_openGLMV_.width  = w1;
	_openGLMV_.height = h1;

	// set topdownWindow as the active window
	glutSetWindow(_openGLMV_.TopDownWindow);
	// resize and reposition the sub window
	glutPositionWindow(_openGLMV_.border, (_openGLMV_.height + _openGLMV_.border) / 40);
	glutReshapeWindow(_openGLMV_.width - 20, _openGLMV_.height - 20);
	setProjection(_openGLMV_.width / 2 - _openGLMV_.border * 3 / 2, _openGLMV_.height / 2 - _openGLMV_.border * 3 / 2);
}

#pragma endregion Static_Render


// --------------------------------------------------------------------------------
//       STATIC RENDERING OBJECTS
// --------------------------------------------------------------------------------
//Static Drawcube object for rendering.
#pragma region Static_Objects

//Parallelize
void drawRadCircle()
{
	GLfloat pi_short  = 3.14159f;
	GLfloat rad_short = 1000.0;

	glBegin(GL_POINTS);

		for (int i = 0; i < (int)rad_short; ++i)
		{
			glVertex3f(cos(pi_short*i / rad_short), 0.0, sin(pi_short*i / rad_short));
		}
		
	glEnd();
}

void drawCircle()
{

	glColor3f(0.0, 1.0, 0.0); // <R,G,B>

	//Circle
	glTranslatef(0.0f, 0.75f, 0.0f);
	glutSolidSphere(0.10f, 10, 10);
}

void drawTennisBall()
{
	//Circle
	glTranslatef(1.6f, 0.0f, 2.6f);
	glutSolidSphere(0.10f, 5, 5);
}

//Static Drawcube object for rendering.
void drawCubeObject()
{
	//Generic cube size
	GLdouble cube_size;
	
	cube_size = 0.20;
	// Red side - TOP
	glBegin(GL_POLYGON);
		glVertex3f(cube_size, cube_size, cube_size);
		glVertex3f(cube_size, cube_size, -cube_size);
		glVertex3f(-cube_size, cube_size, -cube_size);
		glVertex3f(-cube_size, cube_size, cube_size);
	glEnd();
}

void drawPoint()
{
	//Handle the next gps cordination.
	//Generic cube size
	GLdouble cube_size;
	
	cube_size = 0.20;
	// Red side - TOP
	glColor3f(0.0, 0.0, 1.0); // <R,G,B>
	glBegin(GL_POLYGON);
		glVertex3f(cube_size, cube_size, cube_size);
		glVertex3f(cube_size, cube_size, -cube_size);
		glVertex3f(-cube_size, cube_size, -cube_size);
		glVertex3f(-cube_size, cube_size, cube_size);
	glEnd();
}

#pragma endregion Static_Objects

//END OF STATIC OBJECTS
//----------------------------------------------------------------------------------

//Preliminary description for the error
// x range assumptions for the data


//---------------------------------------------------------------------------------

void renderBitmapString(GLfloat x, GLfloat y, GLfloat z, void *font, char *string) 
{
	char *c;
	glRasterPos2i(x, y);
	for (c = string; *c != '\0'; c++)
	{
		glutBitmapCharacter(font, *c);
	}
}

void restorePerspectiveProjection() 
{
	glMatrixMode(GL_PROJECTION);
	// restore previous projection matrix
	glPopMatrix();

	// get back to modelview mode
	glMatrixMode(GL_MODELVIEW);
}

void setOrthographicProjection() 
{
	// switch to projection mode
	glMatrixMode(GL_PROJECTION);

	// save previous matrix which contains the
	//settings for the perspective projection
	glPushMatrix();

	// reset matrix
	glLoadIdentity();

	// set a 2D orthographic projection
	gluOrtho2D(0, _openGLMV_.width, _openGLMV_.height, 0);

	// switch back to modelview mode
	glMatrixMode(GL_MODELVIEW);
}

// Common Render Items for all subwindows
void renderSubWindowScene() 
{
	GLdouble plain_size;
	GLdouble ground_level;
	GLdouble object_pos;

	plain_size   = 200.0f;
	ground_level = 0.0f;
	object_pos   = 10.0f;

	// Draw ground
	GLuint tex;
	glGenTextures(1, &tex);

	glColor3f(0.184, 0.310, 0.310); //<R,G,B>
	glBegin(GL_QUADS);
		glVertex3f(-plain_size, ground_level, -plain_size);
		glVertex3f(-plain_size, ground_level, plain_size);
		glVertex3f(plain_size, ground_level, plain_size);
		glVertex3f(plain_size, ground_level, -plain_size);
	glEnd();

	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
	glEnable(GL_BLEND);
	glBlendFunc(GL_ONE, GL_ONE);
	glColor3f(0.545, 0.000, 0.545); //<R,G,B>
	glutSolidSphere(10.0f, 20, 10);

	glColor3f(0.294, 0.000, 0.510);
	glRotatef(100 - (_openGLCV_.angle + _openGLKS_.deltaAngle)*180.0 / 3.14, 0.0, 1.0, 0.0);
	glutSolidSphere(10.0f, 20, 5);
  
	glEnd();
}

#pragma region Position_Computation

void computePos(GLfloat deltaMove)
{
	_openGLCV_.x += deltaMove * _openGLCV_.lx * 0.1f;		
	_openGLCV_.z += deltaMove * _openGLCV_.lz * 0.1f;
	
	_openGLRT_.past_x.push_back(_openGLCV_.x);		
	_openGLRT_.past_z.push_back(_openGLCV_.z);
	
	std::cout << "x pos = " << _openGLCV_.x << std::endl;
	std::cout << "z pos = " << _openGLCV_.z << std::endl;
}

void computeDir(GLfloat deltaAngle)
{
	_openGLCV_.angle += deltaAngle;
	//Angle calculation is required to move forward.

	_openGLCV_.lx = sin(_openGLCV_.angle);
	_openGLCV_.lz = -cos(_openGLCV_.angle);

	std::cout << "angle = " << _openGLCV_.angle << std::endl;
	std::cout << "lx = " << _openGLCV_.lx << std::endl;
	std::cout << "lz = " << _openGLCV_.lz << std::endl;
}
#pragma endregion Position_Computation


#pragma region Scene_Render
// Display function for main window.
void renderScene() 
{
	glutSetWindow(_openGLMV_.mainWindow);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glutSwapBuffers();
}

// Display function for top-down view
void renderTopDownScene() 
{
	glutSetWindow(_openGLMV_.TopDownWindow);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glLoadIdentity();

	std::atomic<int> index;
	index.store(0,std::memory_order_relaxed);
  
	//Main Camera Position, starting position for top down view.
	gluLookAt(_openGLCV_.x, _openGLCV_.y + 15, _openGLCV_.z, _openGLCV_.x,
		_openGLCV_.y - 1, _openGLCV_.z, _openGLCV_.lx, 0, _openGLCV_.lz);

			// Main object, main camera.
			glPushMatrix();
				glColor3f(0.0, 0.0, 1.0); //<R,G,B>
				glTranslatef(_openGLCV_.x, _openGLCV_.y, _openGLCV_.z);
				glRotatef(180 - (_openGLCV_.angle + _openGLKS_.deltaAngle)*180.0 / 3.14, 0.0, 1.0, 0.0);
				glutSolidCone(0.2, 0.5f, 2, 2);
				drawRadCircle();
			glPopMatrix();
				
	
			// TEST
			for(int i = 0; i <_distance_vector.size();i++)
			{
				glPushMatrix();
					glColor3f(0.0, 0.0, 1.0); //<R,G,B>
					glTranslatef(_distance_x[i] + _distance_vector[i], _openGLCV_.y, _distance_z[i] + _distance_vector[i]);
					glRotatef(180 - (_openGLCV_.angle + _openGLKS_.deltaAngle)*180.0 / 3.14, 0.0, 1.0, 0.0);
					drawCubeObject();
				glPopMatrix();
			}
			
	//Only register points in 15 intervals	
	for (int i = 0; i < _openGLRT_.past_x.size(); i++)
	{
			if (i % 15 == 0)
			{
				_openGLRLT_.line_x.push_back(_openGLRT_.past_x[i]);
				_openGLRLT_.line_z.push_back(_openGLRT_.past_z[i]);
				
				_openGLRT_.past_track_x.push_back(_openGLRT_.past_x[i]);		
				_openGLRT_.past_track_z.push_back(_openGLRT_.past_z[i]);
						
			}

		glPushMatrix();
			glColor3f(1.0, 1.0, 1.0); //<R,G,B>
			glPolygonMode(GL_FRONT_AND_BACK, GL_POINT);
			glTranslatef(_openGLRT_.past_x[i], 0.0f, _openGLRT_.past_z[i]);
			glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
		glPopMatrix();
	}

	
	//Draws the tracer red-line from the first point of view.
	//Needs a better rework of the y direction calculation between matrices.
	// Draw the interpolated points second.
	glColor3f(0.0f, 0.0f, 0.0f); // Draw points in black
	glPointSize(5);
	glBegin(GL_POINTS);
		for (int i = 1; i < _openGLRLT_.line_x.size(); i++)
		{
			glVertex3f(_openGLRLT_.line_x[i], 0.0f, _openGLRLT_.line_z[i]);
		}
	glEnd();

	glPointSize(1);
	glLineWidth(1.0);
	
	glColor3f(0.0, 0.0, 0.8); //<R,G,B>
	glBegin(GL_LINE_STRIP);
		for (int i = 1; i < _openGLRLT_.line_x.size(); i++)
		{
			glVertex3f(_openGLRLT_.line_x[i], 0.0f, _openGLRLT_.line_z[i]);
		}
	glEnd();
	glFlush();
	
	glColor3f(1.0, 0.0, 0.8); //<R,G,B>
	glBegin(GL_TRIANGLE_FAN);
		for (int i = 1; i < _openGLRLT_.line_x.size(); i++)
		{
			glVertex3f(_openGLRLT_.line_x[i], 0.0f, _openGLRLT_.line_z[i]);
			_openGLRLT_.line_x.pop_back();
			_openGLRLT_.line_z.pop_back();
		}
	glEnd();
	
	glFlush();

	//Render Area
	renderSubWindowScene();
	glutSwapBuffers();
}

int render_index = 0;
int gps_index    = 0;
// Global render func
void renderSceneAll() 
{
	// check for keyboard movement
	// Up down movement reference check.
	if (_openGLKS_.deltaMove)
	{
		computePos(_openGLKS_.deltaMove);
		glutSetWindow(_openGLMV_.mainWindow);
		glutPostRedisplay();
	}

	// Left right movement reference check.
	if (_openGLKS_.deltaAngle)
	{
		computeDir(_openGLKS_.deltaAngle);
		glutSetWindow(_openGLMV_.mainWindow);
		glutPostRedisplay();
	}
	renderScene();
	
	//Create Lidar Connection and grab information from lidar.
	render_index++;
	if(render_index > 10)
	{
		try
		{
			object main_module ((handle<>(borrowed(PyImport_AddModule("__main__")))));
			object main_namespace = main_module.attr("__dict__");
			object ignored = exec("import socket", main_namespace);
			ignored = exec("import sys", main_namespace);
			ignored = exec("from binascii import hexlify, unhexlify, a2b_hex, b2a_hex, b2a_qp, a2b_qp", main_namespace);
			ignored = exec("g = bytearray(b\' \x02\x73\x52\x4e\x20\x4c\x4d\x44\x73\x63\x61\x6e\x64\x61\x74\x61\x03\')", main_namespace);
			ignored = exec("s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)", main_namespace);
			ignored = exec("print \"Socket successfully created\"",main_namespace);
			
			ignored = exec("port = 2111",main_namespace);
			ignored = exec("host_ip = socket.gethostbyname('192.168.1.25')", main_namespace);
			ignored = exec("s.connect((host_ip, port))", main_namespace);
			ignored = exec("print 'Received', host_ip", main_namespace);
			ignored = exec("degree = 90", main_namespace);
			ignored = exec("distance = []", main_namespace);
			
			ignored = exec("s.send(g)", main_namespace);
			ignored = exec("d = s.recv(4096)", main_namespace);
			ignored = exec("print d", main_namespace);
			
			string return_value = py::extract<std::string>("d");
			
			//Test
			//std::string msg("Hello, Python");
			//boost::python::object py_msg = msg;
			//https://sixty-north.com/blog/how-to-write-boost-python-type-converters.html
			
			ignored = exec("data = d.split(\" \")", main_namespace);
			ignored = exec("dataPoints = int(\"0x\" + str(data[25]), 16)", main_namespace);
			ignored = exec("print(dataPoints)", main_namespace);
			
		}
		catch(error_already_set)
		{
			PyErr_Print();
		}
		
		render_index = 0; //Reset lidar render index.
	}
	
	
	//Create GPS connection
	gps_index++;
	if(gps_index > 5)
	{
		try
		{
			object main_module ((handle<>(borrowed(PyImport_AddModule("__main__")))));
			object main_namespace = main_module.attr("__dict__");
			object ignored = exec("import socket", main_namespace);
			ignored = exec("import sys", main_namespace);
			ignored = exec("s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)", main_namespace);
			ignored = exec("print \"Socket successfully created\"",main_namespace);
			ignored = exec("port = 2111",main_namespace);
			ignored = exec("host_ip = socket.gethostbyname('192.168.1.25')", main_namespace);
			ignored = exec("s.connect((host_ip, port))", main_namespace);
			
			//Test
			//std::string msg("Hello, Python");
			//boost::python::object py_msg = msg;
			//https://sixty-north.com/blog/how-to-write-boost-python-type-converters.html
			
		}
		catch(error_already_set)
		{
			PyErr_Print();
		}
		
		gps_index = 0; //Reset lidar render index.
	}
	
	//Display Current GPS
	
	
	//Calculate Distance
	for(int i =0; i < 4;i++) //Example forloop
	{
		set_lat(lat_points[i]);
		set_lon(lon_points[i]);
	}
	
	for(int i = 1; i < 4; i++)
	{
		cout << setprecision(10) << distanceEarth(_lat_incoming[i],_lat_incoming[i-1],_lon_incoming[i],_lon_incoming[i-1]) * 0.0001 << endl;
		_distance_vector.push_back(distanceEarth(_lat_incoming[i],_lat_incoming[i-1],_lon_incoming[i],_lon_incoming[i-1]) * 0.0001);
		_distance_x.push_back(_openGLCV_.x);
		_distance_z.push_back(_openGLCV_.z);
	}

	//Calculate Pathing

	//Send Back to the server - Only if there is an obstacle in the path.
	bool send_back = false;
	if(send_back)
	{
		try
		{
			object main_module ((handle<>(borrowed(PyImport_AddModule("__main__")))));
			object main_namespace = main_module.attr("__dict__");
			object ignored = exec("import socket", main_namespace);
			ignored = exec("import sys", main_namespace);
			ignored = exec("s_back = socket.socket(socket.AF_INET, socket.SOCK_STREAM)", main_namespace);
			ignored = exec("print \"Socket successfully created\"",main_namespace);
			
			ignored = exec("port = 2111",main_namespace);
			ignored = exec("host_ip = socket.gethostbyname('192.168.1.25')", main_namespace);
			ignored = exec("s_back.connect((host_ip, port))", main_namespace);
			ignored = exec("print 'Received', host_ip", main_namespace);
			
			//Send the GPS data back to the server;
			//ignored = exec("s.send("")", main_namespace);
		}
		catch(error_already_set)
		{
			PyErr_Print();
		}
	}
	

	//Sub-Render Scenes with multi-view camera angles.
	renderTopDownScene();
}
#pragma endregion Scene_Render



// --------------------------------------------------------------------------------
//             KEYBOARD SECTION
// --------------------------------------------------------------------------------
#pragma region Keyboard_Section

void processNormalKeys(unsigned char key, GLint xx, GLint yy) {

	if (key == 27)
	{
		glutDestroyWindow(_openGLMV_.mainWindow);
		exit(0);
	}
	else if(key == 'a')
	{
		if(auto_path == false)
		{
			auto_path = true;
		}
		else if(auto_path)
		{
			auto_path = false;
		}
		
	}
}

void pressKey(GLint key, GLint xx, GLint yy) 
{

	switch (key) 
	{
		case GLUT_KEY_LEFT:  _openGLKS_.deltaAngle  = -0.01f; break;
		case GLUT_KEY_RIGHT: _openGLKS_.deltaAngle  = 0.01f; break;
		case GLUT_KEY_UP:    _openGLKS_.deltaMove   = 0.2f; break;
		case GLUT_KEY_DOWN:  _openGLKS_.deltaMove   = -0.2f; break;
	}

	glutSetWindow(_openGLMV_.mainWindow);
	glutPostRedisplay();
}

void releaseKey(int key, int x, int y) 
{
	switch (key) 
	{
		case GLUT_KEY_LEFT: 
							//std::cout << "Left Key Pressed" << std::endl;
							break;
		case GLUT_KEY_RIGHT: 
							//std::cout << "Right Key Pressed" << std::endl; 
							_openGLKS_.deltaAngle = 0.0f; 
							break;
		case GLUT_KEY_UP: 
							//std::cout << "Up Key Pressed" << std::endl; 
							break;
		case GLUT_KEY_DOWN: 
							//std::cout << "Down Key Pressed" << std::endl;
							_openGLKS_.deltaMove = 0; 
							break;
	}
}

#pragma endregion Keyboard_Section

// --------------------------------------------------------------------------------
//             MOUSE INPUT SECTION
// --------------------------------------------------------------------------------
#pragma region Mouse_Section

#pragma endregion Mouse_Section

// --------------------------------------------------------------------------------
//             MAIN and INIT
// --------------------------------------------------------------------------------
int main(int argc, char **argv) 
{
	// Init of GLUT and main window creation.
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
	glutInitWindowPosition(100, 100);
	glutInitWindowSize(400, 400);
	_openGLMV_.mainWindow = glutCreateWindow("SLAM MAZE");

	// Callback processing for rendering all scenes.
	// These scenes will include sub-set window views.
	glutDisplayFunc(renderSceneAll);
	glutReshapeFunc(changeSize);

	glClearColor(0.0, 0.0, 0.0, 0.0);
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_CULL_FACE);
	
	// register callbacks
	glutKeyboardFunc(processNormalKeys);
	glutSpecialFunc(pressKey);
	glutIgnoreKeyRepeat(1);
	glutSpecialUpFunc(releaseKey);
	
	
	//-----------------------------------------------------------------------------
	//Top down view window decleration.
	std::cout << "Registering callbacks for Top Down started..." << std::endl;
	_openGLMV_.TopDownWindow = glutCreateSubWindow(_openGLMV_.mainWindow, 10, 10, 400, 400);
	glutDisplayFunc(renderTopDownScene);
	
	glClearColor(0.0, 0.0, 0.0, 0.0);
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_CULL_FACE);
	
	// register callbacks
	glutKeyboardFunc(processNormalKeys);
	glutSpecialFunc(pressKey);
	glutIgnoreKeyRepeat(1);
	glutSpecialUpFunc(releaseKey);
	
	try
	{
		cout << "Python Module Starting..." << endl;
		cout << "-------------------------" << endl;
		Py_Initialize();
		cout << "Python Module Initialized..." << endl;
	}
	catch(error_already_set)
	{
		PyErr_Print();
	}

	std::cout << "All callbacks have been initialized..." << std::endl;
	std::cout << "--------------------------------------" << std::endl;
	std::cout << "Main Loop Starting..." << std::endl;
	// Glut loop event cycle.
	glutMainLoop();

	//Anything beyond this point is disregarded.
	//-----------------------------------------------------------------------------

	return 1;
}
