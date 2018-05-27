#pragma once
#include "ObjectExtensions.h"

#pragma region Static_Render

void setProjection(GLint w1, GLint h1)
{
	omp_lock_t mtxLock;
	omp_init_lock(&mtxLock);

	omp_set_lock(&mtxLock);
	GLfloat ratio;
	// Prevent a divide by zero, when window is too short
	// (you cant make a window of zero width).
	#pragma omp atomic write
	ratio = (1.0f * w1 / h1);
	// Reset the coordinate system before modifying
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();

	// Set the viewport to be the entire window
	glViewport(0, 0, w1, h1);

	// Set the clipping volume
	gluPerspective(45, ratio, 0.1, 1000);
	glMatrixMode(GL_MODELVIEW);

	omp_unset_lock(&mtxLock);
	omp_destroy_lock(&mtxLock);
}

void changeSize(GLint w1, GLint h1)
{
	if (h1 == 0) { h1 = 1; }

	#pragma omp atomic write
	_openGLMV_.width  = w1;
	#pragma omp atomic write
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
	#pragma omp atomic write
	GLfloat pi_short  = 3.14159f;
	#pragma omp atomic write
	GLfloat rad_short = 1000.0;

	glBegin(GL_POINTS);
		#pragma omp parallel for ordered schedule(dynamic)
		for (int i = 0; i < (int)rad_short; ++i)
		{
			glVertex3f(cos(pi_short*i / rad_short), 0.0, sin(pi_short*i / rad_short));
		}
	glEnd();
}

void drawCircle()
{
	omp_lock_t mtxLock;
	omp_init_lock(&mtxLock);

	omp_set_lock(&mtxLock);
	glColor3f(0.0, 1.0, 0.0); // <R,G,B>

							  //Circle
	glTranslatef(0.0f, 0.75f, 0.0f);
	glutSolidSphere(0.10f, 10, 10);
	omp_unset_lock(&mtxLock);
	omp_destroy_lock(&mtxLock);
}

void drawTennisBall()
{
	//Circle
	glTranslatef(1.6f, 0.0f, 2.6f);
	glutSolidSphere(0.10f, 5, 5);
}

//Static Drawcube object for rendering.
void drawRock()
{
	omp_lock_t mtxLock;

	omp_init_lock(&mtxLock);
	omp_set_lock(&mtxLock);
	
	//Generic cube size
	GLdouble cube_size;
	
	#pragma omp atomic write
	cube_size = 0.20;
	omp_unset_lock(&mtxLock);

	// Red side - TOP
	omp_set_lock(&mtxLock);
	glBegin(GL_POLYGON);
		glVertex3f(cube_size, cube_size, cube_size);
		glVertex3f(cube_size, cube_size, -cube_size);
		glVertex3f(-cube_size, cube_size, -cube_size);
		glVertex3f(-cube_size, cube_size, cube_size);
	glEnd();
	omp_unset_lock(&mtxLock);
	omp_destroy_lock(&mtxLock);
}

#pragma endregion Static_Objects

//END OF STATIC OBJECTS
//----------------------------------------------------------------------------------
