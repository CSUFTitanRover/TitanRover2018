# Inverse Kinematics 

Inverse kinematics makes use of kinematics equations to determine the joint parameters that provide a desired position
for a robot's end-effector. Essentially, we should be able to give a desired point (x, y, z) we want to reach for and our IK process will
return the correct solution that each joint needs to be angled at. 

## Usage

The IK solver is a python process that will run on the homebase computer. This is done for two reasons:

- Alleviate the processing time from the rover to the homebase
- We can preview a solution on our UI before sending over the solution to the rover

It is still to be decided how we will communicate with it from the UI since it's a python process. An idea is to run a Node process that registers
a RPC with Deepstream and when that RPC is sent a request for IK it can call this python script.
