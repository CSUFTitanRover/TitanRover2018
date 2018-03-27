from numpy import *
from itertools import *
from collections import *
import time

#   This program is intended for calculating the inverse kinematics for a robotic arm with one azimuthal degree of freedom
#   And 3  effectors that do not rotate at a wrist.
#   First we set the lengths of each arm in our assemblage, then we set the constraints of each arm.
#   We only care about the angles of the arm after it has reached its target location, so we assume that its
#   initial conditions are "straight in the air".
#   The program asks for a target location in x,y,z space. It then tries every combination of discrete,
#   but small, angles (theta steps) that the arm could possibly achieve, If the discrete movements put the end effector closer
#   to the target, we update the current angles to the "test angles"
#   this continues until the end effector is within 2 mm of the target, which for all intents and purposes we regard as
#   "being at the target"


#   Here's how to read the final angles:
#   The azimuthal angle assumes "x" is the forward direction
#   J2 Base angle is read as the angle between the rover chassis and the arm
#   J3 Base Angle is the angle between the line defined by J2 & J3. 0 radians being J2 & J3 are inline with eachother
#   J4 Base Angle is the angle between the line defined by J3 & J4, 0 radians being J3 & J4 are inline with eachother

#   First, lets define some tuples to store our arm parameters and call them later
Lengths = namedtuple('Lengths', ['length1', 'length2', 'length3'])
Target  = namedtuple('Target', ['x', 'y', 'z'])


length1 = 0.775957
length2 = 0.3683
length3 = 0.3723

lengths = Lengths(length1, length2, length3)

number_of_joints = len(lengths)

#   Define our effector angle constraints
theta1_lower_bound = 0.3
theta1_upper_bound = pi/2.0

theta2_lower_bound = 0
theta2_upper_bound = pi/2.0

theta3_lower_bound = -pi/2.0
theta3_upper_bound = pi/2.0

#   Here we define one angle step
thetastep = 0.001

#   Here we define the distance the end of the arm needs to be from its target for us to consider the arm "at the point".
error_tolerance = 0.002

#   Use our angular bounds and effector lengths to determine possible x,y,z points that our arm can reach
mindist = sqrt((lengths.length1 - lengths.length3) ** 2 + lengths.length2 ** 2)
maxdist = lengths.length1 + lengths.length2 + lengths.length3


#   Wrap into arrays
theta0initial = 0

theta1initial = pi/2.0

theta2initial = 0

theta3initial = 0

currentthetas = [theta0initial, theta1initial, theta2initial, theta3initial]


#   Input your target x,y,z
def get_position_input():
    running = False
    xtarget = float(input("please input target x:"))
    ytarget = float(input("please input target y:"))
    ztarget = float(input("please input target z:"))

    while not running:
        if mindist < (sqrt(xtarget ** 2 + ytarget ** 2 + ztarget ** 2)) < maxdist:
            running = not running
        else:
            print(f'x,y,z out of range, must be between {round(mindist ** 2, 2)} m & {round(maxdist ** 2, 3)} m, yours is {round(xtarget ** 2 + ytarget ** 2 + ztarget ** 2, 2)} m')
            get_position_input()
    target = Target(xtarget, ytarget, ztarget)

    return target


#   the "arm" functions give us the x,y,z location of the end of each effector by converting from spherical coords
#   to cartesian coords
def xarm(joint_number, theta0, theta1, theta2, theta3):
    return float(joint_number * cos(theta1 - theta2 + theta3) * cos(theta0))


def yarm(joint_number,theta0, theta1, theta2, theta3):
    return float(joint_number * cos(theta1 - theta2 + theta3) * sin(theta0))


def zarm(joint_number,theta1, theta2, theta3):
    return float(joint_number * sin(theta1 - theta2 + theta3))


#   this function calculates the final asimuthal angle from our target coords using inverse trig functions
def azimuthalcalculation(target, currentthetas):

    if target.x == 0 and target.y != 0:
        currentthetas[0] = arcsin(target.y / r)
    elif target.x < 0:
        currentthetas[0] = arctan(target.y / target.x) + pi
    else:
        currentthetas[0] = arctan(target.y / target.x)
    if currentthetas[0] > pi:
        currentthetas[0] = currentthetas[0] - 2*pi
    if currentthetas[0] < -pi:
        currenthetas[0] = currentthetas[0] + 2*pi

    return currentthetas[0]


#   this function calculates the distance between the end effector arm and the target location. This is the variable
#   that we are seeking to minimize
def get_distance(currentthetas, target):


    x_position_1 = xarm(lengths.length1, currentthetas[0], currentthetas[1], 0, 0)
    x_position_2 = xarm(lengths.length2, currentthetas[0], currentthetas[1], currentthetas[2], 0)
    x_position_3 = xarm(lengths.length3, currentthetas[0], currentthetas[1], currentthetas[2], currentthetas[3])

    y_position_1 = yarm(lengths.length1, currentthetas[0], currentthetas[1], 0, 0)
    y_position_2 = yarm(lengths.length2, currentthetas[0], currentthetas[1], currentthetas[2], 0)
    y_position_3 = yarm(lengths.length3, currentthetas[0], currentthetas[1], currentthetas[2], currentthetas[3])

    z_position_1 = zarm(lengths.length1, currentthetas[1], 0, 0)
    z_position_2 = zarm(lengths.length2, currentthetas[1], currentthetas[2], 0)
    z_position_3 = zarm(lengths.length3, currentthetas[1], currentthetas[2], currentthetas[3])

    xcurrent = x_position_1 + x_position_2 + x_position_3
    ycurrent = y_position_1 + y_position_2 + y_position_3
    zcurrent = z_position_1 + z_position_2 + z_position_3

    distance = sqrt((xcurrent - target.x) ** 2 + (ycurrent - target.y) ** 2 + (zcurrent - target.z) ** 2)

    return distance


#   this function takes the discrete jump possibilities for each arm as an input (positive step, negative step, or no step)
#   and updates the arms angles if the new orientation brings it closer to its target
def calculate_next_step(theta1step, theta2step, theta3step, target, currentthetas, distance):

    theta1test = currentthetas[1] + theta1step
    theta2test = currentthetas[2] + theta2step
    theta3test = currentthetas[3] + theta3step

    xtest = xarm(lengths.length1, currentthetas[0], theta1test, 0, 0) + xarm(lengths.length2, currentthetas[0], theta1test, theta2test, 0) + xarm(lengths.length3, currentthetas[0], theta1test, theta2test, theta3test)
    ytest = yarm(lengths.length1, currentthetas[0], theta1test, 0, 0) + yarm(lengths.length2, currentthetas[0], theta1test, theta2test, 0) + yarm(lengths.length3, currentthetas[0], theta1test, theta2test, theta3test)
    ztest = zarm(lengths.length1, theta1test, 0, 0) + zarm(lengths.length2, theta1test, theta2test, 0) + zarm(lengths.length3, theta1test, theta2test, theta3test)

    distancetest = sqrt((xtest - target.x) ** 2 + (ytest - target.y) ** 2 + (ztest - target.z) ** 2)

    #   This is where we enforce the angular constraints; we only update effector angles for achievable orientations
    if distancetest < distance and theta1_lower_bound <= theta1test <= theta1_upper_bound and theta2_lower_bound <= theta2test <= theta2_upper_bound and theta3_lower_bound <= theta3test <= theta3_upper_bound:
        distance = distancetest
        currentthetas[1] = theta1test
        currentthetas[2] = theta2test
        currentthetas[3] = theta3test


    return distance, currentthetas


#   this function generates a list with every possible combination of positive, negative, and no steps
def generate_possible_combinations(thetastep):
    global number_of_joints
    global angle_options
    possibilities=[]
    for i in range(number_of_joints - 1):
        possibilities.append(thetastep)
        possibilities.append(-thetastep)
        possibilities.append(0)
    angle_options = list(set(permutations(possibilities, 3)))
    return angle_options


#   this function cycles through every possible combination of inputs and keeps updating the effector angles until
#   the end effector is within 2mm of the target point. The initial angles combined with the discrete changes gives us
#   the final angle values for each arm
def solve(currentthetas, target, angle_options):

    distance = get_distance(currentthetas, target)
    #   Now we check all possibilities for the arm and choose the output that brings the end effector closer to the goal]
    while distance > error_tolerance:
        i = 0
        while i < len(angle_options):
            distance, currentthetas = calculate_next_step(angle_options[i][0],angle_options[i][1],angle_options[i][2], target, currentthetas, distance)
            i += 1

#   Now lets run each program, and time it
def main():
    target = get_position_input()

    starttime = time.time()

    currentthetas[0] = azimuthalcalculation(target, currentthetas)

    angle_options = generate_possible_combinations(thetastep)

    solve(currentthetas, target, angle_options)

    endtime = time.time()

    print (f'Azimuthal Angle =  {round(currentthetas[0],3)} Radians')
    print (f'J2 Base Angle   =  {round(currentthetas[1],3)} Radians')
    print (f'J3 Base Angle   =  {round(currentthetas[2],3)} Radians')
    print (f'J4 Base Angle   =  {round(currentthetas[3],3)} Radians')


if __name__ == "__main__":
    main()