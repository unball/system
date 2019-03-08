import math as m
from control_options import *
import planar
from math import sqrt, fabs
old_coordinates = []
def goalkeeper(robot,ball):
    x = -ball.side*0.65
    y_limit = 0.325
    distance2ball = sqrt((robot.x-ball.x)**2 + (robot.y - ball.y)**2)
    distance2goal = sqrt((robot.x - robot.dx)**2 + (robot.y - robot.dy)**2)
    old_coordinates.append(ball.x)
    old_coordinates.append(ball.y)

    try:
        vel_x = ball.x - old_coordinates[0]
        vel_y = ball.y - old_coordinates[1]
        walls_x, walls_y = walls_estimation(vel_x, vel_y, ball)
    except:
        walls_x = ball.x
        walls_y = ball.y

    if False:
    #if fabs(vel_y) > 100 or fabs(vel_x) > 100:
        if (walls_y > y_limit):
            y = y_limit
        elif (walls_y < -y_limit):
            y = -y_limit
        else:
            y = walls_y
    else:
        if (ball.y > y_limit):
            y = y_limit
        elif (ball.y < -y_limit):
            y = -y_limit
        else:
            y = ball.y

    if fabs(vel_y) > 0.00001 or fabs(vel_x) > 0.00001:
        if (walls_y > y_limit):
            y = y_limit
        elif (walls_y < -y_limit):
            y = -y_limit
        else:
            y = walls_y
    else:
        if (ball.y > y_limit):
            y = y_limit
        elif (ball.y < -y_limit):
            y = -y_limit
        else:
            y = ball.y

    control = control_options.poseLine

    if distance2ball <= 0.08:
        if (ball.side == -1 and ballUpRobot(ball,robot)) or (ball.side == 1 and not(ballUpRobot(ball,robot))):
            control = control_options.spinCCW
        else:
            control = control_options.spinCW

    

    th = m.pi/2
    return control, x, y, th

def ballUpRobot(robot,ball):
    return (robot.y>ball.y)

def walls_estimation(vel_x, vel_y, ball):
    speed_vector = planar.Vec2(vel_x,vel_y)
    speed_vector = planar.Vec2.normalized(speed_vector)
    ball_position = planar.Vec2(ball.x,ball.y)

    if (speed_vector.x != 0) and (speed_vector.y != 0):
        t_x_pos = (0.65 - ball_position.x)/speed_vector.x
        t_y_pos = (0.75 - ball_position.y)/speed_vector.y
        t_x_neg = (-0.65 - ball_position.x)/speed_vector.x
        t_y_neg = (-0.75 - ball_position.y)/speed_vector.y

        time_list = [(t_x_pos),(t_y_pos),(t_x_neg),(t_y_neg)]
        time = min([i for i in time_list if i>0])

        walls_y = speed_vector.y * time + ball_position.y
        walls_x = speed_vector.x * time + ball_position.x

    elif speed_vector.x != 0:
        t_x_pos = (0.65 - ball_position.x)/speed_vector.x
        t_x_neg = (-0.65 - ball_position.x)/speed_vector.x

        time_list = [(t_x_pos),(t_x_neg)]
        time = min([i for i in time_list if i>0])
        walls_y = ball_position.y
        walls_x = ball_position.x + speed_vector.y * time

    elif speed_vector.y != 0:
        t_y_pos = (0.75 - ball_position.x)/speed_vector.x
        t_y_neg = (-0.75 - ball_position.x)/speed_vector.x

        time_list = [(t_y_pos),(t_y_neg)]
        time = min([i for i in time_list if i>0])
        walls_x = ball_position.x
        walls_y = ball_position.y + speed_vector.y * time
    else:
        walls_x = 0
        walls_y = 0

    return walls_x,walls_y
