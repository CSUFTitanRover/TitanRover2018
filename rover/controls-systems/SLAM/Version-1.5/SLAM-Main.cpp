// SLAM-Basic-Maze.cpp : Defines the entry point for the console application.
//
#include "stdafx.h"
#include "StaticRendering.h"
//---------------------------------------------------------------------------------

void renderBitmapString(GLfloat x, GLfloat y, GLfloat z,
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
	omp_lock_t mtxLock;
	omp_init_lock(&mtxLock);

	omp_set_lock(&mtxLock);
	GLdouble plain_size;
	GLdouble ground_level;
	GLdouble object_pos;

	plain_size   = 200.0f;
	ground_level = 0.0f;
	object_pos   = 10.0f;
	omp_unset_lock(&mtxLock);

	// Draw ground
	omp_set_lock(&mtxLock);

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
	omp_unset_lock(&mtxLock);
}

#pragma region Position_Computation

void computePos(GLfloat deltaMove)
{
	#pragma omp parallel num_threads(2)
	{
		#pragma omp sections
		{
			#pragma omp section
			{
				_openGLCV_.x += deltaMove * _openGLCV_.lx * 0.1f;
				
			}
			#pragma omp section
			{
				_openGLCV_.z += deltaMove * _openGLCV_.lz * 0.1f;
			}
		}
		#pragma omp barrier
	}

	#pragma omp parallel num_threads(2)
	{
		#pragma omp sections
		{
			#pragma omp section
			{
				_openGLRT_.past_x.push_back(_openGLCV_.x);
			}
			#pragma omp section
			{
				_openGLRT_.past_z.push_back(_openGLCV_.z);
			}
		}
		#pragma omp barrier
	}

	std::cout << "x pos = " << _openGLCV_.x << std::endl;
	std::cout << "z pos = " << _openGLCV_.z << std::endl;
}

void computeDir(GLfloat deltaAngle)
{
	_openGLCV_.angle += deltaAngle;
	//Angle calculation is required to move forward.
	#pragma omp parallel num_threads(2)
	{
		#pragma omp sections
		{
			#pragma omp section
			{
				_openGLCV_.lx = sin(_openGLCV_.angle);
			}
			#pragma omp section
			{
				_openGLCV_.lz = -cos(_openGLCV_.angle);
			}
		}
		#pragma omp barrier //
	}

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

	#pragma omp parallel // starts a new team
	{
		#pragma omp sections // divides the team into sections
		{
			#pragma omp section
			{
				// Main object, main camera.
				glPushMatrix();
					glColor3f(0.0, 0.0, 1.0); //<R,G,B>
					glTranslatef(_openGLCV_.x, _openGLCV_.y, _openGLCV_.z);
					glRotatef(180 - (_openGLCV_.angle + _openGLKS_.deltaAngle)*180.0 / 3.14, 0.0, 1.0, 0.0);
					glutSolidCone(0.2, 0.5f, 2, 2);
					drawRadCircle();
				glPopMatrix();
			}
		}
		#pragma omp barrier
	}

	//Only register points in 15 intervals
	//display using glbegin()glend()
	//glflush or glpopmatrix();
	
	#pragma omp parallel for ordered schedule(static) private(i)
	for (int i = 0; i < _openGLRT_.past_x.size(); i++)
	{
		#pragma omp ordered
		{
			if (i % 15 == 0)
			{
				#pragma omp parallel
				{
					#pragma omp sections
					{
						#pragma omp section
						{
							_openGLRLT_.line_x.push_back(_openGLRT_.past_x[i]);
						}
						#pragma omp section
						{
							_openGLRLT_.line_z.push_back(_openGLRT_.past_z[i]);
						}
					}
					#pragma omp barrier
				}
				
				#pragma omp parallel
				{
					#pragma omp sections
					{
						#pragma omp section
						{
							_openGLRT_.past_track_x.push_back(_openGLRT_.past_x[i]);
						}
						#pragma omp section
						{
							_openGLRT_.past_track_z.push_back(_openGLRT_.past_z[i]);
						}
					}
					#pragma omp barrier
				}
			}
		}//Pragma End

		 //create a square overlay to establish gps data etc...
		 //glClear(GL_DEPTH_BUFFER_BIT);
		 //glPushMatrix();
		 //	glTranslatef(0,0,0);
		 //	glColor3f(1.0, 0.0, 0.0);

		 //	std::string temp_x = " x: " + std::to_string(_openGLRT_.past_x[i]) + " y: " + std::to_string(_openGLRT_.past_z[i]);
		 //	char *cstr_x = &temp_x[0u];
		 //	renderBitmapString(0, 0.0f, 0, GLUT_BITMAP_HELVETICA_12, cstr_x);
		 //glPopMatrix();


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
		#pragma omp parallel for ordered schedule(static)
		for (int i = 1; i < _openGLRLT_.line_x.size(); i++)
		{
			glVertex3f(_openGLRLT_.line_x[i], 0.0f, _openGLRLT_.line_z[i]);
		}
	glEnd();

	glPointSize(1);
	glLineWidth(1.0);
	
	glColor3f(0.0, 0.0, 0.8); //<R,G,B>
	glBegin(GL_LINE_STRIP);
		#pragma omp parallel for ordered schedule(static)
		for (int i = 1; i < _openGLRLT_.line_x.size(); i++)
		{
			glVertex3f(_openGLRLT_.line_x[i], 0.0f, _openGLRLT_.line_z[i]);
		}
	glEnd();
	glFlush();
	
	glColor3f(1.0, 0.0, 0.8); //<R,G,B>
	glBegin(GL_TRIANGLE_FAN);
		#pragma omp parallel for ordered schedule(static)
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
}

void pressKey(GLint key, GLint xx, GLint yy) 
{

	switch (key) 
	{
		case GLUT_KEY_LEFT:  _openGLKS_.deltaAngle  = -0.01f; break;
		case GLUT_KEY_RIGHT: _openGLKS_.deltaAngle  = 0.01f; break;
		case GLUT_KEY_UP:    _openGLKS_.deltaMove   = 0.2f; break;
		case GLUT_KEY_DOWN:  _openGLKS_.deltaMove   = -0.2f; break;
		case GLUT_KEY_SHIFT_L: flag_tennis = -1; break;
		case GLUT_KEY_SHIFT_R: flag_obs    = -1; break;
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
		case GLUT_KEY_SHIFT_L:
							//std::cout << "Shift Key Pressed" << std::endl;
							break;
	}
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

	#pragma omp parallel num_threads(2) // starts a new team
	{
		#pragma omp sections
		{
			#pragma omp section
			{
				// register callbacks
				glutKeyboardFunc(processNormalKeys);
				glutSpecialFunc(pressKey);
				glutIgnoreKeyRepeat(1);
				glutSpecialUpFunc(releaseKey);
			}
			#pragma omp section
			{
				//Physical Camera Movement functions;
				glutMouseFunc(mouseButton);
				glutMotionFunc(physicalCameraMove);
			}
		}
		#pragma omp barrier
	}
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
	_openGLMV_.TopDownWindow = glutCreateSubWindow(_openGLMV_.mainWindow, 10, 10, 400, 400);
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
