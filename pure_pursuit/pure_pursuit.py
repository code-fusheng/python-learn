import numpy as np
import math

k = 0.1  # 预瞄距离系数
Lfc = 3.0  # 初始预瞄距离

class TargetCourse:

    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.old_nearest_point_index = None

    def search_target_index(self, vehicle):

        if self.old_nearest_point_index is None:
            # 搜索距离车辆最近的点
            dx = [vehicle.x - icx for icx in self.cx]
            dy = [vehicle.y - icy for icy in self.cy]
            d = np.hypot(dx, dy)
            ind = np.argmin(d)
            self.old_nearest_point_index = ind
        else:
            ind = self.old_nearest_point_index
            distance_this_index = math.hypot(self.cx[ind] - vehicle.x, self.cy[ind] - vehicle.y)
            while True:
                distance_next_index = math.hypot(self.cx[ind+1] - vehicle.x, self.cy[ind+1] - vehicle.y)
                if distance_this_index < distance_next_index:
                    break
                ind = ind + 1 if (ind + 1) < len(self.cx) else ind
                distance_this_index = distance_next_index
            self.old_nearest_point_index = ind

        Lf = k * vehicle.v + Lfc  # 根据速度更新预瞄距离

        # 搜索预瞄点索引
        while Lf > math.hypot(self.cx[ind] - vehicle.x, self.cy[ind] - vehicle.y):
            if (ind + 1) >= len(self.cx):
                break
            ind += 1

        return ind, Lf


def pure_pursuit_steer_control(vehicle, trajectory, pind):
    ind, Lf = trajectory.search_target_index(vehicle)

    if pind >= ind:
        ind = pind

    if ind < len(trajectory.cx):
        tx = trajectory.cx[ind]
        ty = trajectory.cy[ind]
    else:  # toward goal
        tx = trajectory.cx[-1]
        ty = trajectory.cy[-1]
        ind = len(trajectory.cx) - 1

    alpha = math.atan2(ty - vehicle.y, tx - vehicle.x) - vehicle.yaw
    delta = math.atan2(2.0 * vehicle.L * math.sin(alpha) , Lf)

    return delta, ind