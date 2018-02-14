// SLAM-Basic-Maze.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "GL\glew.h"
#include "GL\freeglut.h"
#include <string>
#include <iomanip>
#include <iostream>
#include <conio.h>
#include <vector>
#include <atomic>
#include <mutex>
#define WINVER 0x0500
#include <windows.h>

#pragma region Global_Data_Objects

std::mutex mtx;

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
	GLfloat deltaMove  = 0;
	GLint xOrigin      = -1;
}_openGLKS_;


struct _openGL_MAINWINDOW_VALUES_
{
	// width and height of the window
	GLint height;
	GLint width;
	// variables to hold window identifiers
	GLint mainWindow;
	GLint TopDownWindow;
	//border between subwindows
	GLint border = 6;
}_openGLMV_;


struct _openGL_ROVER_TRACKING_
{
	std::vector<double> past_x;
	std::vector<double> past_z;
}_openGLRT_;

struct _openGL_ROVER_LINE_TRACKING_
{
	std::vector<double> line_x;
	std::vector<double> line_z;
}_openGLRLT_;

#pragma endregion Global_Data_Objects


std::vector<GLfloat> past_x;
std::vector<GLfloat> past_y;
std::vector<GLfloat> past_z;

void setProjection(GLint w1, GLint h1)
{
	mtx.lock();
	std::atomic<GLfloat> ratio;
	ratio.store(0, std::memory_order_release);
	// Prevent a divide by zero, when window is too short
	// (you cant make a window of zero width).
	ratio.store((1.0f * w1 / h1),std::memory_order_relaxed);
	// Reset the coordinate system before modifying
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();

	// Set the viewport to be the entire window
	glViewport(0, 0, w1, h1);

	// Set the clipping volume
	gluPerspective(45, ratio.load(), 0.1, 1000);
	glMatrixMode(GL_MODELVIEW);
	mtx.unlock();
}

void changeSize(GLint w1, GLint h1) 
{
	if (h1 == 0){ h1 = 1; }
		
	// we're keeping these values cause we'll need them latter
	_openGLMV_.width  = w1;
	_openGLMV_.height = h1;

	// set topdownWindow as the active window
	glutSetWindow(_openGLMV_.TopDownWindow);
	// resize and reposition the sub window
	glutPositionWindow(_openGLMV_.border, (_openGLMV_.height + _openGLMV_.border) / 8);
	//glutReshapeWindow(_openGLMV_.width / 2 - _openGLMV_.border * 3 / 2, _openGLMV_.height / 2 - _openGLMV_.border * 3 / 2);
	glutReshapeWindow(_openGLMV_.width-20, _openGLMV_.height-20);
	setProjection(_openGLMV_.width / 2 - _openGLMV_.border * 3 / 2, _openGLMV_.height / 2 - _openGLMV_.border * 3 / 2);
}
//---------------------------------------------------------------------------------

// --------------------------------------------------------------------------------
//       STATIC RENDERING OBJECTS
// --------------------------------------------------------------------------------
//Static Drawcube object for rendering.
#pragma region Static_Objects

void drawCircle()
{
	mtx.lock();
	glColor3f(0.0, 1.0, 0.0); // <R,G,B>

	//Circle
	glTranslatef(0.0f, 0.75f, 0.0f);
	glutSolidSphere(0.15f, 10, 10);
	mtx.unlock();
}

void drawTennisBall()
{
	mtx.lock();
	glColor3f(1.0, 1.0, 0.0); // <R,G,B>

	//Circle
	glTranslatef(0.0f, 0.75f, 0.0f);
	glutSolidSphere(0.10f, 5, 5);
	mtx.unlock();
}

//Static Drawcube object for rendering.
void drawCube() 
{
	//Generic cube size
	mtx.lock();
	std::atomic<GLdouble> cube_size;
	cube_size.store(0.10,std::memory_order_relaxed);
	mtx.unlock();

	// Red side - TOP
	mtx.lock();
	glBegin(GL_POLYGON);
	glVertex3f(cube_size.load(), cube_size.load(), cube_size.load());
	glVertex3f(cube_size, cube_size, -cube_size);
	glVertex3f(-cube_size, cube_size, -cube_size);
	glVertex3f(-cube_size, cube_size, cube_size);
	glEnd();
	mtx.unlock();
}

#pragma endregion Static_Objects

//END OF STATIC OBJECTS
//----------------------------------------------------------------------------------

void renderBitmapString(
	GLfloat x,
	GLfloat y,
	GLfloat z,
	void *font,
	char *string) 
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
	mtx.lock();
	std::atomic<GLdouble> plain_size;
	std::atomic<GLdouble> ground_level;
	std::atomic<GLdouble> object_pos;

	plain_size.store(100.0f, std::memory_order_relaxed);
	ground_level.store(0.0f, std::memory_order_relaxed);
	object_pos.store(10.0f, std::memory_order_relaxed);
	mtx.unlock();

	// Draw ground
	mtx.lock();
	glColor3f(0.647059f, 0.164706f, 0.164706f); //<R,G,B>

	GLuint tex;
	glGenTextures(1, &tex);

	glBegin(GL_QUADS);
	glVertex3f(-plain_size, ground_level, -plain_size);
	glVertex3f(-plain_size, ground_level, plain_size);
	glVertex3f(plain_size, ground_level, plain_size);
	glVertex3f(plain_size, ground_level, -plain_size);
	glEnd();
	mtx.unlock();

	// Draw and placement.
	std::atomic<int> i;
	#pragma omp parrallel
	{
		for (i.store(-3, std::memory_order_relaxed); i.load() < 3; i++)
		{
			#pragma omp for
			for (std::atomic<int> j = -3; j.load() < 3; j++)
			{
				glPushMatrix();
				glColor3f(1.0, 0.0, 0.0); //<R,G,B>
				glTranslatef(i.load() * object_pos.load(), 0.0f, j.load() * object_pos.load());
				drawCube();
				glPopMatrix();
			}
		}
	}

}

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
	_openGLCV_.lx = sin(_openGLCV_.angle);
	_openGLCV_.lz = -cos(_openGLCV_.angle);

	std::cout << "angle = " << _openGLCV_.angle << std::endl;
	std::cout << "lx = " << _openGLCV_.lx << std::endl;
	std::cout << "lz = " << _openGLCV_.lz << std::endl;
}

// Display function for main window.
void renderScene() 
{
	glutSetWindow(_openGLMV_.mainWindow);
	glClear(GL_COLOR_BUFFER_BIT);
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

	// Draw red cone at the location of the main camera.
	glPushMatrix();
	glColor3f(0.0, 0.0, 1.0); //<R,G,B>
	glTranslatef(_openGLCV_.x, _openGLCV_.y, _openGLCV_.z);
	glRotatef(180 - (_openGLCV_.angle + _openGLKS_.deltaAngle)*180.0 / 3.14, 0.0, 1.0, 0.0);
	glutSolidCone(0.2, 0.5f, 2, 2);
	glPopMatrix();

	//Grabs the Current location of the main object.
	GLfloat matrixMV[16];
	glGetFloatv(GL_MODELVIEW_MATRIX, matrixMV);
	GLdouble xCenterTriangle = matrixMV[12];
	GLdouble yCenterTriangle = matrixMV[13];
	GLdouble zCenterTriangle = matrixMV[14];

	//Renders a static tennis ball
	glPushMatrix();
	glTranslatef(1.6, 0.0f, -1.6);
	past_x.push_back(1.6);
	past_y.push_back(0.0f);
	past_z.push_back(-1.6);

	if(!_openGLRT_.past_x.empty())
		//glTranslatef(_openGLCV_.x, _openGLCV_.y, _openGLCV_.z);
	glColor3f(1.0, 1.0, 0.0); //<R,G,B>
	drawTennisBall();

	std::string temp_x = " Tennis Ball";
	char *cstr_x = &temp_x[0u];
	renderBitmapString(1.6, 0.0f, -1.6, GLUT_BITMAP_HELVETICA_12, cstr_x);
	glPopMatrix();

	for (int i = 0; i < _openGLRT_.past_x.size(); i++)
	{
		if (i % 15 == 0)
		{
			_openGLRLT_.line_x.push_back(_openGLRT_.past_x[i]);
			_openGLRLT_.line_z.push_back(_openGLRT_.past_z[i]);

			glPushMatrix();
			glTranslatef(_openGLRT_.past_x[i], 0.0f, _openGLRT_.past_z[i]);
			glColor3f(1.0, 0.0, 0.0); //<R,G,B>
			std::string temp_x = " x: " + std::to_string(_openGLRT_.past_x[i]) + " y: " + std::to_string(_openGLRT_.past_z[i]);
			char *cstr_x = &temp_x[0u];
			renderBitmapString(0, 0.0f, 0, GLUT_BITMAP_HELVETICA_12, cstr_x);
			
			drawCircle();
			glPopMatrix();
			// limit the display trail and pass it to another tracking function.
		}
	}

	//Draws the tracer red-line from the first point of view.
	//Needs a better rework of the y direction calculation between matrices.
	for (int i = 1; i < _openGLRLT_.line_x.size(); i++)
	{
		glPushMatrix();
		glLineWidth(1.0);
		glColor3f(1.0, 0.0, 0.0); //<R,G,B>
		glBegin(GL_LINES);
		glVertex3f(_openGLRLT_.line_x[i-1], 0.0f, _openGLRLT_.line_z[i-1]);
		glColor3f(0.0, 0.0, 1.0); //<R,G,B>
		glVertex3f(_openGLRLT_.line_x[i], 0.0f, _openGLRLT_.line_z[i]);
		glEnd();
		glPopMatrix();
	}

	renderSubWindowScene();
	glutSwapBuffers();
}

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

	//Sub-Render Scenes with multi-view camera angles.
	renderTopDownScene();
}

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
}

void pressKey(GLint key, GLint xx, GLint yy) 
{

	switch (key) 
	{
		case GLUT_KEY_LEFT: _openGLKS_.deltaAngle  = -0.01f; break;
		case GLUT_KEY_RIGHT: _openGLKS_.deltaAngle = 0.01f; break;
		case GLUT_KEY_UP: _openGLKS_.deltaMove     = 0.5f; break;
		case GLUT_KEY_DOWN: _openGLKS_.deltaMove   = -0.5f; break;
	}

	glutSetWindow(_openGLMV_.mainWindow);
	glutPostRedisplay();
}

void simulate_automation()
{
	// input event.
	INPUT ip;

	// Set up a generic keyboard event.
	ip.type = INPUT_KEYBOARD;
	ip.ki.wScan = 0; // hardware scan code for key
	ip.ki.time = 0;
	ip.ki.dwExtraInfo = 0;

	if (!past_x.empty())
	{
		if (_openGLCV_.z > past_z[0])
		{
			// Press the "Up" key
			ip.ki.wVk = 0x26; // virtual-key code for the "Up" key
			ip.ki.dwFlags = 0; // 0 for key press
			SendInput(1, &ip, sizeof(INPUT));
		}

		if (_openGLCV_.z < past_z[0])
		{
			// Press the "Up" key
			ip.ki.wVk = 0x28; // virtual-key code for the "Up" key
			ip.ki.dwFlags = 0; // 0 for key press
			SendInput(1, &ip, sizeof(INPUT));
		}

		if (_openGLCV_.x > past_x[0])
		{
			// Press the "Up" key
			ip.ki.wVk = 0x25; // virtual-key code for the "Up" key
			ip.ki.dwFlags = 0; // 0 for key press
			SendInput(1, &ip, sizeof(INPUT));

		}

		if (_openGLCV_.x < past_x[0])
		{
			// Press the "Up" key
			ip.ki.wVk = 0x27; // virtual-key code for the "Up" key
			ip.ki.dwFlags = 0; // 0 for key press
			SendInput(1, &ip, sizeof(INPUT));
		}
	}


}

void releaseKey(int key, int x, int y) 
{
	switch (key) 
	{
		case GLUT_KEY_LEFT: std::cout << "Left Key Pressed" << std::endl; break;
		case GLUT_KEY_RIGHT: std::cout << "Right Key Pressed" << std::endl; _openGLKS_.deltaAngle = 0.0f; break;
		case GLUT_KEY_UP: std::cout << "Up Key Pressed" << std::endl; break;
		case GLUT_KEY_DOWN: std::cout << "Down Key Pressed" << std::endl; _openGLKS_.deltaMove = 0; break;
	}

	//Can automate the guidance cycle here:
	//
	//---------
	//simulate_automation();
}

#pragma endregion Keyboard_Section

// --------------------------------------------------------------------------------
//             MOUSE INPUT SECTION
// --------------------------------------------------------------------------------
#pragma region Mouse_Section

void physicalCameraMove(int x, int y)
{
	// this will only be true when the left button is down
	if (_openGLKS_.xOrigin >= 0)
	{
		// update deltaAngle
		_openGLKS_.deltaAngle = (x - _openGLKS_.xOrigin) * 0.001f;

		// update camera's direction
		_openGLCV_.lx = sin(_openGLCV_.angle + _openGLKS_.deltaAngle);
		_openGLCV_.lz = -cos(_openGLCV_.angle + _openGLKS_.deltaAngle);

		glutSetWindow(_openGLMV_.mainWindow);
		glutPostRedisplay();
	}
}

// Will emulate physical camera switch to enable the physical movement of the
// embedded camera.
void mouseButton(int button, int state, int x, int y) 
{
	// only start motion if the left button is pressed
	if (button == GLUT_LEFT_BUTTON) 
	{
		// when the button is released
		if (state == GLUT_UP) 
		{
			_openGLCV_.angle += _openGLKS_.deltaAngle;
			_openGLKS_.deltaAngle = 0.0f;
			_openGLKS_.xOrigin = -1;
		}
		else 
		{
			_openGLKS_.xOrigin = x;
		}
	}
}

#pragma endregion Mouse_Section

// --------------------------------------------------------------------------------
//             MAIN and INIT
// --------------------------------------------------------------------------------

void init() 
{
	glClearColor(0.0, 0.0, 0.0, 0.0);
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_CULL_FACE);

	// register callbacks
	glutKeyboardFunc(processNormalKeys);
	glutSpecialFunc(pressKey);
	glutIgnoreKeyRepeat(1);
	glutSpecialUpFunc(releaseKey);
	
	//Physical Camera Movement functions;
	glutMouseFunc(mouseButton);
	glutMotionFunc(physicalCameraMove);
}

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

	init();

	//-----------------------------------------------------------------------------
	//Top down view window decleration.
	std::cout << "Registering callbacks for Top Down started..." << std::endl;
	_openGLMV_.TopDownWindow = glutCreateSubWindow(_openGLMV_.mainWindow, 10, 10, 350, 350);
	glutDisplayFunc(renderTopDownScene);

	init();

	std::cout << "All callbacks have been initialized..." << std::endl;
	std::cout << "--------------------------------------" << std::endl;
	std::cout << "Main Loop Starting..." << std::endl;
	// Glut loop event cycle.
	glutMainLoop();

	//Anything beyond this point is disregarded.
	//-----------------------------------------------------------------------------

	return 1;
}
