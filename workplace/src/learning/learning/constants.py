'''
>   author: whf
>   date: 2024-05-23
>   all constants should be modified in this class and only called in other modules.
    usage:
        from .constants import C
        print(C.NAME)
'''
class C():
    GATE = [-0.25,8.75]               # (x,y)
    DIST = 1.0                     # get_goal_coords() distance to the ball (m)
    ERROR = 0.3                     # error for location.in_place (m)
    NAME = 'az'                    # dog_name
    COLOR = 0                       # 0 FOR RED, 1 FOR BLACK, 2 FOR WHITE
    UPPER_IP = '10.0.0.144' 
    UPPER_PORT = 40000
    FREQUENCY = 0.3
    MAX_SPEED_X = 0.54
    MAX_SPEED_Y = 1.58
    MAX_SPEED_Z = 2.4                 # frequency of updating status for move.goto()
    MARGIN = [[-2.35,8.25],[1.85,2.25]]
    SAFE_DIST = 0.5
    START_POINT = [-0.2,4.4-DIST]   # 每次射门成功后恢复到一个有利点位
    MOTION_ID = 305
    GATE_RANGE = [-1.5,1.5]                 # 球门左右边界
    STEP_HEIGHT = [0.01,0.01]
    INFO_DELAY = 0.3                # threshold for determing a data is to dated to use.
    AVOID_DIST = 0.5
    TRANSLATE_TIMEOUT = 5.
    DIST_TO_TARGET_THRESHOLD = 4.
    TRANSLATE_SPEED = 0.2
    