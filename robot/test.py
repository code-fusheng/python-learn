#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pip install open3d pandas numpy scipy

import pandas as pd
import numpy as np
import open3d as o3d
from filterpy.kalman import KalmanFilter
from scipy.interpolate import splprep, splev

class Test:
    def __init__(self):
        self.lane_file_dir = "/Users/fusheng/Desktop/steer_10230142/lidar_mode/pathes/"
        self.gps_file_path = self.lane_file_dir + "gps_lane_1.csv"
        self.topology_lines_count = 5  # 拓扑关系行的数量

    def load_lane_data(self, path):
        try:
            with open(path, 'r') as file:
                lines = file.readlines()
            # 保持拓扑关系部分不变
            topology_lines = lines[:self.topology_lines_count]
            # 剩余部分是轨迹数据
            trajectory_lines = lines[self.topology_lines_count:]
            trajectory_data = pd.DataFrame([list(map(float, line.replace(',', '').split())) for line in trajectory_lines])
            # 提取 x, y, z 坐标
            # trajectory_points = trajectory_data[[0, 1, 2]].values
            # 提取 x 和 y 坐标
            trajectory_points = trajectory_data[[0, 1]].values
            # 为缺少的 z 坐标添加默认值 0，扩展为 (x, y, z)
            z_values = np.zeros((trajectory_points.shape[0], 1))
            trajectory_points_3d = np.hstack((trajectory_points, z_values))
            # 提取四元数（假设它们在第3到第6列）
            quaternion_data = trajectory_data.iloc[:, 2:6].values
            return trajectory_points_3d, quaternion_data
        except Exception as e:
            print(f"Error loading lane: {e}")

    def convert_lane_visualize_data(self, data, color):
        # 将轨迹点转换为Open3D中的点云对象
        pcd_data = o3d.geometry.PointCloud()
        pcd_data.points = o3d.utility.Vector3dVector(data)
        # 设置轨迹点的颜色（这里设置为红色）
        pcd_data.paint_uniform_color(color)  # 红色
        return pcd_data

    def smooth_lane(self, lane_data, method="moving_average"):
        if method == "moving_average":
            # 使用移动平均进行平滑
            window_size = 50
            smoothed_points = np.convolve(lane_data[:, 0], np.ones(window_size)/window_size, mode='valid')
            for i in range(1, lane_data.shape[1]):
                smoothed_column = np.convolve(lane_data[:, i], np.ones(window_size)/window_size, mode='valid')
                smoothed_points = np.column_stack((smoothed_points, smoothed_column))
            return smoothed_points

        # 还行
        elif method == "weighted_moving_average":
            window_size = 25
            weights = np.linspace(1, 0.5, window_size)  # 更近的点权重更高
            weights = weights / weights.sum()  # 归一化权重
            smoothed_points = []
            for i in range(len(lane_data)):
                start = max(i - window_size // 2, 0)
                end = min(i + window_size // 2 + 1, len(lane_data))
                window = lane_data[start:end]
                window_weights = weights[:end - start]
                smoothed_point = np.average(window, axis=0, weights=window_weights)
                smoothed_points.append(smoothed_point)
            smoothed_points = np.array(smoothed_points)
            return smoothed_points

        elif method == "spline":
            # 使用 B 样条插值
            tck, u = splprep(lane_data.T, s=5)  # s 控制平滑程度
            smoothed_points = np.array(splev(np.linspace(0, 1, len(lane_data)), tck)).T
            return smoothed_points
        
        elif method == "kalman":
            return self.kalman_filter_smoothing(lane_data)
        
        else:
            print("Unknown smoothing method specified.")
            return lane_data

    def kalman_filter_smoothing(self, points):
        # 定义卡尔曼滤波器的参数
        kf = KalmanFilter(dim_x=6, dim_z=3)
        dt = 1.0  # 假设时间步长为 1
        # 状态转移矩阵 F
        kf.F = np.array([[1, dt, 0, 0, 0, 0],
                         [0, 1, 0, 0, 0, 0],
                         [0, 0, 1, dt, 0, 0],
                         [0, 0, 0, 1, 0, 0],
                         [0, 0, 0, 0, 1, dt],
                         [0, 0, 0, 0, 0, 1]])
        # 观测矩阵 H
        kf.H = np.array([[1, 0, 0, 0, 0, 0],
                         [0, 0, 1, 0, 0, 0],
                         [0, 0, 0, 0, 1, 0]])
        # 初始化噪声和误差协方差矩阵
        kf.R *= 0.1  # 观测噪声协方差
        kf.Q *= 0.01  # 过程噪声协方差
        kf.P *= 10.0  # 初始状态协方差
        # 初始状态
        smoothed_points = []
        kf.x[:3] = points[0, :3].reshape(-1, 1)  # 初始位置
        for point in points:
            # 更新观测值
            kf.predict()
            kf.update(point[:3])
            smoothed_points.append(kf.x[:3].flatten())
        return np.array(smoothed_points)

    def run(self):
        trajectory_points, quaternion_data = self.load_lane_data(self.gps_file_path)
        
        # 原始轨迹 
        origin_lane = self.convert_lane_visualize_data(trajectory_points, [0, 1, 0])
        # 平滑轨迹
        smoothed_points = self.smooth_lane(trajectory_points, method="kalman")
        moving_average_lane = self.convert_lane_visualize_data(smoothed_points, [1, 0, 0])
        o3d.visualization.draw_geometries([origin_lane, moving_average_lane], window_name="Trajectory Visualization")

if __name__ == "__main__":
    tester = Test()
    tester.run()
