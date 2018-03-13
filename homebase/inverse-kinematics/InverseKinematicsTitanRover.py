from numpy import *
from itertools import *
import time

#This program is intended for calculating the inverse kinematics for a robotic arm with one azimuthal degree of freedom
#And 3  effectors that do not rotate at a wrist.
#First we set the lengths of each arm in our assemblage, then we set the constraints of each arm.
#We only care about the angles of the arm after it has reached its target location, so we assume that its
#initial conditions are "straight in the air".
#The program asks for a target location in x,y,z space. It then tries every combination of discrete,
#but small, angles (theta steos) that the arm could possibly achieve, If the discrete movements put the end effector closer
#to the target, we update the current angles to the "test angles"
#this continues until the end effector is within 2 mm of the target, which for all intents and purposes we regard as
#"being at the target"

length1 = 0.775957
length2 = 0.3683
length3 = 0.3723

length = [length1,length2,length3]

number_of_joints = len(length)

#Define our effector angle constraints
theta1lowerbound = 0.3
theta1upperbound = pi/2

theta2lowerbound = 0
theta2upperbound = pi/2

theta3lowerbound = -pi/2
theta3upperbound = pi/2

#Define angle step
thetastep = 0.001

#Use our angular bounds and effector lengths to determine possible x,y,z points that our arm can reach
mindist = sqrt((length[0] - length[2]) ** 2 + length[1] ** 2)
maxdist = length[0] + length[1] + length[2]


#Wrap into arrays
theta0initial = 0

theta1initial = pi/2.

theta2initial = 0

theta3initial = 0

currentthetas = [theta0initial, theta1initial, theta2initial, theta3initial]


#Input your target x,y,z
def positioninput():
    global xtarget
    global ytarget
    global ztarget

    running = False

    xtarget = float(input("please input target x:"))

    ytarget = float(input("please input target y:"))

    ztarget = float(input("please input target z:"))

    while not running:
        if sqrt(xtarget ** 2 + ytarget ** 2 + ztarget ** 2) > mindist\
        and sqrt(xtarget ** 2 + ytarget ** 2 + ztarget ** 2) < maxdist:
            running = not running
        else:
            print("x,y,z out of range, must be between", mindist, "&", maxdist)
            positioninput()

    return xtarget, ytarget, ztarget

#the "arm" functions give us the x,y,z location of the end of each effector by converting from spherical coords
#to cartesian coords
def xarm(joint_number, theta0, theta1, theta2, theta3):
    return float(joint_number * cos(theta1 - theta2 + theta3) * cos(theta0))


def yarm(joint_number,theta0, theta1, theta2, theta3):
    return float(joint_number * cos(theta1 - theta2 + theta3) * sin(theta0))


def zarm(joint_number,theta1, theta2, theta3):
    return float(joint_number * sin(theta1 - theta2 + theta3))

#this function calculates the final asimuthal angle from our target coords using inverse trig functions
def azimuthalcalculation():
    global xtarget
    global ytarget
    global ztarget
    global currentthetas

    if xtarget == 0 and ytarget != 0:
        currentthetas[0] = arcsin(ytarget / r)
    elif xtarget < 0:
        currentthetas[0] = arctan(ytarget / xtarget) + pi
    else:
        currentthetas[0] = arctan(ytarget / xtarget)

    return currentthetas[0]

#this function calculates the distance between the end effector arm and the target location. This is the variable
#that we are seeking to minimize
def distancefunc():
    global distance
    global currentthetas

    xcurrent = xarm(length[0],currentthetas[0], currentthetas[1],0,0) + xarm(length[1],currentthetas[0], currentthetas[1], currentthetas[2],currentthetas[3]) + xarm(length[2],currentthetas[0], currentthetas[1], currentthetas[2], currentthetas[3])

    ycurrent = yarm(length[0],currentthetas[0],currentthetas[2],0,0) + yarm(length[1],currentthetas[0],currentthetas[1],currentthetas[2],0) + yarm(length[2],currentthetas[0],currentthetas[1],currentthetas[2],currentthetas[3])

    zcurrent = zarm(length[0],currentthetas[1], 0, 0) + zarm(length[1],currentthetas[1], currentthetas[2], 0) + zarm(length[2],currentthetas[1], currentthetas[2], currentthetas[3])

    distance = sqrt((xcurrent - xtarget) ** 2 + (ycurrent - ytarget) ** 2 + (zcurrent - ztarget) ** 2)

    return xcurrent, ycurrent, zcurrent, distance

#this function takes the discrete jump possibilities for each arm as an input (positive step, negative step, or no step)
#and updates the arms angles if the new orientation brings it closer to its target
def angletest(theta1step,theta2step,theta3step):

    global currentthetas
    global distance
    global xtarget
    global ytarget
    global ztarget

    theta1test = currentthetas[1] + theta1step
    theta2test = currentthetas[2] + theta2step
    theta3test = currentthetas[3] + theta3step

    xtest = xarm(length[0], currentthetas[0], theta1test,0,0)\
            + xarm(length[1], currentthetas[0], theta1test, theta2test,0)\
            + xarm(length[2],currentthetas[0],theta1test,theta2test,theta3test)
    ytest = yarm(length[0], currentthetas[0], theta1test,0,0) + yarm(length[1], currentthetas[0], theta1test, theta2test,0)\
            + yarm(length[2],currentthetas[0],theta1test,theta2test,theta3test)
    ztest = zarm(length[0], theta1test, 0, 0) + zarm(length[1], theta1test, theta2test, 0)\
            + zarm(length[2], theta1test, theta2test, theta3test)

    distancetest = sqrt((xtest - xtarget) ** 2 + (ytest - ytarget) ** 2 + (ztest - ztarget) ** 2)

    #This is where we enforce the angular constraints; we only update effector angles for achievable orientations
    if distancetest < distance and theta1lowerbound <= theta1test <= theta1upperbound and theta2lowerbound <= theta2test <= theta2upperbound and theta3lowerbound <= theta3test <= theta3upperbound:
        distance = distancetest
        currentthetas[1] = theta1test
        currentthetas[2] = theta2test
        currentthetas[3] = theta3test

    #print("distance test; this value should be going down", distance)

    return distance, currentthetas[1], currentthetas[2], currentthetas[3]

#this function generates a list with every possible combination of positive, negative, and no steps
def possibility():
    global number_of_joints
    global angle_options
    possibility=[]
    for i in range(number_of_joints - 1):
        possibility.append(thetastep)
        possibility.append(-thetastep)
        possibility.append(0)
    angle_options = list(set(permutations(possibility, 3)))
    return angle_options

#this function cycles through every possible combination of inputs and keeps updating the effector angles until
#the end effector is within 2mm of the target point. The initial angles combined with the discrete changes gives us
#the final angle values for each arm
def inversekinematicfunction():
    global currentthetas
    global currentthetas
    global distance

    possibility()
    # Now we check all possibilities for the arm and choose the output that brings the end effector closer to the goal
    #itertools permutation update
    while distance > 0.002:
        i = 0
        while i < len(angle_options):
            angletest(angle_options[i][0],angle_options[i][1],angle_options[i][2])
            i+=1

#Now lets run each program, and time it

positioninput()

starttime = time.time()

distancefunc()

azimuthalcalculation()

inversekinematicfunction()

endtime = time.time()

print ("distance =", distance)
print ("theta0final =", round(currentthetas[0],3))
print ("theta1final = ", round(currentthetas[1],3))
print ("theta2final = ", round(currentthetas[2],3))
print ("theta3final = ", round(currentthetas[3],3))
print ("Time to compute =", round(endtime - starttime, 3),"s")
