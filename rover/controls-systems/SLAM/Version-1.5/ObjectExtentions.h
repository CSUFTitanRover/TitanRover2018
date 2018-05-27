#pragma once
#include "Headers.h"

#pragma region Global_Data_Objects

int flag_tennis = 0;
int flag_obs    = 0;

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

#pragma endregion Global_Data_Objects

