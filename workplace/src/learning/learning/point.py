import math

def get_goal_coords(ball_coords,dog_coords,gate_coords,dist):
    # 计算球门和球之间的直线斜率
    slope = (gate_coords[1] - ball_coords[1]) / (gate_coords[0] - ball_coords[0])
    # p是便于计算最终坐标的系数
    if slope>0:
        p=-1;
    else:
        p=1;
    dist_y=dist*(p*slope/sqrt(1+slope*slope))
    dist_x=dist*(p/sqrt(1+slope*slope))
    goal_coords_x=ball_coords[0]+dist_x;
    goal_coords_y=ball_coords[1]+dist_y;
    return goal_coords_x,goal_coords_y;

def get_routine(ball_coords,dog_coords,goal_coords):
    