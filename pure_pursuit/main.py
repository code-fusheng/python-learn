from bicycle_model import Vehicle, VehicleInfo, draw_trailer
from pure_pursuit import pure_pursuit_steer_control, TargetCourse
import numpy as np
import matplotlib.pyplot as plt
import math
import imageio

MAX_SIMULATION_TIME = 200.0  # 程序最大运行时间200*dt

def NormalizeAngle(angle):
    a = math.fmod(angle + np.pi, 2 * np.pi)
    if a < 0.0:
        a += (2.0 * np.pi)
    return a - np.pi

# 计算距离车辆最近的参考点索引，用于计算横向误差
def calNearestPointIndex(vehicle, ref_path):
    dx = [vehicle.x - icx for icx in ref_path[:, 0]]
    dy = [vehicle.y - icy for icy in ref_path[:, 1]]
    d = np.hypot(dx, dy)
    index = np.argmin(d)
    return index
def main():
    # 设置跟踪轨迹
    ref_path = np.zeros((1000, 2))
    ref_path[:, 0] = np.linspace(0, 50, 1000)  # x坐标
    ref_path[:, 1] = 10 * np.sin(ref_path[:, 0] / 20.0)  # y坐标
    ref = TargetCourse(ref_path[:, 0], ref_path[:, 1])
    # 假设车辆初始位置为（0，0），航向角yaw=pi/2，速度为2m/s，时间周期dt为0.1秒
    vehicle = Vehicle(x=0.0,
                      y=0.0,
                      yaw=np.pi/2,
                      v=2.0,
                      dt=0.1,
                      l=VehicleInfo.L)

    ind, target_ind = ref.search_target_index(vehicle)
    time = 0.0  # 初始时间

    # 记录车辆轨迹
    trajectory_x = []
    trajectory_y = []
    lat_err = []  # 记录横向误差

    i = 0
    image_list = []  # 存储图片
    plt.figure(1)

    last_idx = ref_path.shape[0] - 1  # 跟踪轨迹的最后一个点的索引
    while MAX_SIMULATION_TIME >= time and last_idx > target_ind:
        time += vehicle.dt  # 累加一次时间周期

        # 纯跟踪
        delta_f, target_ind = pure_pursuit_steer_control(vehicle, ref, target_ind)

        # 横向误差计算
        nearest_index = calNearestPointIndex(vehicle, ref_path)
        vehicle_positon = np.zeros(2)
        vehicle_positon[0] = vehicle.x
        vehicle_positon[1] = vehicle.y
        alpha = math.atan2(
            ref_path[nearest_index, 1] - vehicle_positon[1], ref_path[nearest_index, 0] - vehicle_positon[0])
        l_d = np.linalg.norm(ref_path[nearest_index] - vehicle_positon)  # 最近点与车定位点距离l_d

        theta_e = NormalizeAngle(alpha - vehicle.yaw)
        e_y = l_d * math.sin(theta_e)  # 计算实际误差，0为目标距离
        lat_err.append(e_y)

        # 更新车辆状态
        vehicle.update(0.0, delta_f, np.pi / 10)  # 由于假设纵向匀速运动，所以加速度a=0.0
        trajectory_x.append(vehicle.x)
        trajectory_y.append(vehicle.y)

        # 显示动图
        plt.cla()
        plt.plot(ref_path[:, 0], ref_path[:, 1], '-.b', linewidth=1.0)
        draw_trailer(vehicle.x, vehicle.y, vehicle.yaw, vehicle.steer, plt)

        plt.plot(trajectory_x, trajectory_y, "-r", label="trajectory")
        plt.plot(ref_path[target_ind, 0], ref_path[target_ind, 1], "go", label="target")
        plt.axis("equal")
        plt.grid(True)
        plt.pause(0.001)
    #     plt.savefig("temp.png")
    #     i += 1
    #     if (i % 50) > 0:
    #         image_list.append(imageio.imread("temp.png"))
    #
    # imageio.mimsave("display.gif", image_list, duration=0.1)

    plt.figure(2)
    plt.subplot(2, 1, 1)
    plt.plot(ref_path[:, 0], ref_path[:, 1], '-.b', linewidth=1.0)
    plt.plot(trajectory_x, trajectory_y, 'r')
    plt.title("actual tracking effect")

    plt.subplot(2, 1, 2)
    plt.plot(lat_err)
    plt.title("lateral error")
    plt.show()


if __name__ == '__main__':
    main()