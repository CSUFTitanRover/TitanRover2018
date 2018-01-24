// SLAM-Basic-Maze.cpp : Defines the entry point for the console application.
//

#include "GL\glew.h"
#include "GL\freeglut.h"
#include <string>
#include <iomanip>
#include <iostream>
#include <conio.h>
#include <vector>

// angle of rotation for the camera direction
float angle = 0.0f;
// actual vector representing the camera's direction
float lx = 0.0f, lz = -1.0f, ly = 0.0f;
// XZ position of the camera
float x = 0.0f, z = 5.0f, y = 1.75f;

// the key states. These variables will be zero
//when no key is being presses
float deltaAngle = 0.0f;
float deltaMove = 0;
int xOrigin = -1;

// width and height of the window
int h, w;

// variables to compute frames per second
int frame;
long timebase;
char s[50];

// variables to hold window identifiers
int mainWindow, PovWindow, TopDownWindow, SideViewWindow;
//border between subwindows
int border = 6;

std::vector<double> past_x;
std::vector<double> past_z;

void setProjection(int w1, int h1)
{
	float ratio;
	// Prevent a divide by zero, when window is too short
	// (you cant make a window of zero width).
	ratio = 1.0f * w1 / h1;
	// Reset the coordinate system before modifying
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();

	// Set the viewport to be the entire window
	glViewport(0, 0, w1, h1);

	// Set the clipping volume
	gluPerspective(45, ratio, 0.1, 1000);
	glMatrixMode(GL_MODELVIEW);
}

void changeSize(int w1, int h1) 
{
	if (h1 == 0){ h1 = 1; }
		
	// we're keeping these values cause we'll need them latter
	w = w1;
	h = h1;

	// set subwindow 2 as the active window
	glutSetWindow(TopDownWindow);
	// resize and reposition the sub window
	glutPositionWindow(border, (h + border) / 2);
	glutReshapeWindow(w / 2 - border * 3 / 2, h / 2 - border * 3 / 2);
	setProjection(w / 2 - border * 3 / 2, h / 2 - border * 3 / 2);
}
//---------------------------------------------------------------------------------

// --------------------------------------------------------------------------------
//       STATIC RENDERING OBJECTS
// --------------------------------------------------------------------------------
//Static Drawcube object for rendering.
void drawCircle()
{
	glColor3f(1.0, 0.0, 1.0); // Color Purple

	//Circle
	glTranslatef(0.0f, 0.75f, 0.0f);
	glutSolidSphere(0.15f, 20, 20);
}

//Static Drawcube object for rendering.
void drawCube() 
{

	//Generic cube size
	double cube_size = 0.6;

	// White side - BACK
	glBegin(GL_POLYGON);
	glColor3f(1.0, 1.0, 1.0); // Color representation of the polygon section.
	glVertex3f(cube_size, -cube_size, cube_size);
	glVertex3f(cube_size, cube_size, cube_size);
	glVertex3f(-cube_size, cube_size, cube_size);
	glVertex3f(-cube_size, -cube_size, cube_size);
	glEnd();

	// Purple side - RIGHT
	glBegin(GL_POLYGON);
	glColor3f(1.0, 0.0, 1.0);
	glVertex3f(cube_size, -cube_size, -cube_size);
	glVertex3f(cube_size, cube_size, -cube_size);
	glVertex3f(cube_size, cube_size, cube_size);
	glVertex3f(cube_size, -cube_size, cube_size);
	glEnd();

	// Green side - LEFT
	glBegin(GL_POLYGON);
	glColor3f(0.0, 1.0, 0.0);
	glVertex3f(-cube_size, -cube_size, cube_size);
	glVertex3f(-cube_size, cube_size, cube_size);
	glVertex3f(-cube_size, cube_size, -cube_size);
	glVertex3f(-cube_size, -cube_size, -cube_size);
	glEnd();

	// Blue side - TOP
	glBegin(GL_POLYGON);
	glColor3f(0.0, 0.0, 1.0);
	glVertex3f(cube_size, cube_size, cube_size);
	glVertex3f(cube_size, cube_size, -cube_size);
	glVertex3f(-cube_size, cube_size, -cube_size);
	glVertex3f(-cube_size, cube_size, cube_size);
	glEnd();

	// Red side - BOTTOM
	glBegin(GL_POLYGON);
	glColor3f(1.0, 0.0, 0.0);
	glVertex3f(cube_size, -cube_size, -cube_size);
	glVertex3f(cube_size, -cube_size, cube_size);
	glVertex3f(-cube_size, -cube_size, cube_size);
	glVertex3f(-cube_size, -cube_size, -cube_size);
	glEnd();
}
//END OF DRAW CUBE
//----------------------------------------------------------------------------------

void renderBitmapString(
	float x,
	float y,
	float z,
	void *font,
	char *string) 
{

	char *c;
	glRasterPos3f(x, y, z);
	for (c = string; *c != '\0'; c++) {
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

void setOrthographicProjection() {

	// switch to projection mode
	glMatrixMode(GL_PROJECTION);

	// save previous matrix which contains the
	//settings for the perspective projection
	glPushMatrix();

	// reset matrix
	glLoadIdentity();

	// set a 2D orthographic projection
	gluOrtho2D(0, w, h, 0);

	// switch back to modelview mode
	glMatrixMode(GL_MODELVIEW);
}

void computePos(float deltaMove) 
{

	x += deltaMove * lx * 0.1f;
	z += deltaMove * lz * 0.1f;

	past_x.push_back(x);
	past_z.push_back(z);

	std::cout << "x pos = " << x << std::endl;
	std::cout << "z pos = " << z << std::endl;
}

void computeDir(float deltaAngle) 
{

	angle += deltaAngle;
	lx = sin(angle);
	lz = -cos(angle);

	std::cout << "angle = " << angle << std::endl;
	std::cout << "lx = " << lx << std::endl;
	std::cout << "lz = " << lz << std::endl;
}

// Common Render Items for all subwindows
void renderSubWindowScene() 
{

	double plain_size   = 100.0f;
	double ground_level = 0.0f;

	// Draw ground
	glColor3f(0.9f, 0.9f, 0.9f); // Gray-White
	glBegin(GL_QUADS);
	glVertex3f(-plain_size, ground_level, -plain_size);
	glVertex3f(-plain_size, ground_level, plain_size);
	glVertex3f(plain_size, ground_level, plain_size);
	glVertex3f(plain_size, ground_level, -plain_size);
	glEnd();

	// Draw and placement.
	double object_pos = 10.0f;

	for (int i = -3; i < 3; i++)
	{
		for (int j = -3; j < 3; j++)
		{
			glPushMatrix();
			glTranslatef(i * object_pos, 0.0f, j * object_pos);
			drawCube();
			drawCircle();
			glPopMatrix();
		}
	}

	// Draw and placement.
	double cube_pos = 5.0f;
	for (int i = -3; i < 3; i++)
	{
		for (int j = -3; j < 3; j++)
		{
			glPushMatrix();
			glTranslatef(i * cube_pos, 0.0f, j * cube_pos);
			drawCube();
			glPopMatrix();
		}
	}

}

// Display function for main window.
void renderScene() 
{
	glutSetWindow(mainWindow);
	glClear(GL_COLOR_BUFFER_BIT);
	glutSwapBuffers();
}

// Display function for top-down view
void renderTopDownScene() 
{

	glutSetWindow(TopDownWindow);

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	glLoadIdentity();

	//Main Camera Position, starting position for top down view.
	gluLookAt(x, y + 15, z, x, y - 1, z, lx, 0, lz);

	// Draw red cone at the location of the main camera.
	glPushMatrix();
	glColor3f(1.0, 0.0, 0.0);
	glTranslatef(x, y, z);
	glRotatef(180 - (angle + deltaAngle)*180.0 / 3.14, 0.0, 1.0, 0.0);
	glutSolidCone(0.2, 0.8f, 4, 4);
	glPopMatrix();

	for (int i = 0; i < past_x.size(); i++)
	{
		if (i % 2 == 0)
		{
			glPushMatrix();
			glTranslatef(past_x[i], 0.0f, past_z[i]);
			drawCircle();
			glPopMatrix();
			// limit the display trail and pass it to another tracking function.
		}

	}

	//TEST
	if (!past_x.empty() && !past_z.empty())
	{
		glPushMatrix();
		glTranslatef(x*2, 0.0f, z*2);
		drawCube();
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
	if (deltaMove) 
	{
		computePos(deltaMove);
		glutSetWindow(mainWindow);
		glutPostRedisplay();
	}

	// Left right movement reference check.
	if (deltaAngle)
	{
		computeDir(deltaAngle);
		glutSetWindow(mainWindow);
		glutPostRedisplay();
	}
	renderScene();

	//Sub-Render Scenes with multi-view camera angles.
	renderTopDownScene();
}

// --------------------------------------------------------------------------------
//             KEYBOARD SECTION
// --------------------------------------------------------------------------------

void processNormalKeys(unsigned char key, int xx, int yy) {

	if (key == 27) {
		glutDestroyWindow(mainWindow);
		exit(0);
	}
}

void pressKey(int key, int xx, int yy) 
{

	switch (key) 
	{
		case GLUT_KEY_LEFT: deltaAngle = -0.01f; break;
		case GLUT_KEY_RIGHT: deltaAngle = 0.01f; break;
		case GLUT_KEY_UP: deltaMove = 0.5f; break;
		case GLUT_KEY_DOWN: deltaMove = -0.5f; break;
	}

	glutSetWindow(mainWindow);
	glutPostRedisplay();

}

void releaseKey(int key, int x, int y) 
{

	switch (key) 
	{
		case GLUT_KEY_LEFT: std::cout << "Left Key Pressed" << std::endl; break;
		case GLUT_KEY_RIGHT: std::cout << "Right Key Pressed" << std::endl; deltaAngle = 0.0f; break;
		case GLUT_KEY_UP: std::cout << "Up Key Pressed" << std::endl; break;
		case GLUT_KEY_DOWN: std::cout << "Down Key Pressed" << std::endl; deltaMove = 0; break;
	}
}

// --------------------------------------------------------------------------------
//             MOUSE INPUT SECTION
// --------------------------------------------------------------------------------

void mouseMove(int x, int y) {

	// this will only be true when the left button is down
	if (xOrigin >= 0) {

		// update deltaAngle
		deltaAngle = (x - xOrigin) * 0.001f;

		// update camera's direction
		lx = sin(angle + deltaAngle);
		lz = -cos(angle + deltaAngle);

		glutSetWindow(mainWindow);
		glutPostRedisplay();
	}
}

void mouseButton(int button, int state, int x, int y) {

	// only start motion if the left button is pressed
	if (button == GLUT_LEFT_BUTTON) 
	{

		// when the button is released
		if (state == GLUT_UP) 
		{
			angle += deltaAngle;
			deltaAngle = 0.0f;
			xOrigin = -1;
		}
		else 
		{
			xOrigin = x;
		}
	}
}

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
	glutMouseFunc(mouseButton);
	glutMotionFunc(mouseMove);
}

int main(int argc, char **argv) {

	// Init of GLUT and main window creation.
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
	glutInitWindowPosition(100, 100);
	glutInitWindowSize(800, 800);
	mainWindow = glutCreateWindow("SLAM MAZE");

	//Callback processing for rendering all scenes.
	//These scenes will include sub-set window views.
	glutDisplayFunc(renderSceneAll);
	glutReshapeFunc(changeSize);

	init();


	//-----------------------------------------------------------------------------
	//Top down view window decleration.
	std::cout << "Registering callbacks for Top Down started..." << std::endl;
	TopDownWindow = glutCreateSubWindow(mainWindow, border, (h + border) / 2, w / 2 - border * 3 / 2, h / 2 - border * 3 / 2);
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
