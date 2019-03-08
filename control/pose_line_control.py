from math import *
from control_utils import *

orientation = 1
def pose_line_control(robot):
    global orientation
    relative_target = convertTargetPositions(robot)

    if relative_target[1] > 0:
        orientation = 1
    else:
        orientation = -1

    error_angle = calculateErrorAngle(relative_target,orientation)
    error_magnitude = calculateDistance(relative_target)
    tolerance_radius = 0.05

    u = robot.kp_u*error_magnitude*orientation
    w = robot.kp_w*error_angle

    if error_magnitude < tolerance_radius:
        k_angular=.5
        u = 0
        w = k_angular*angdiff(robot.th, pi/2)

    return u, w