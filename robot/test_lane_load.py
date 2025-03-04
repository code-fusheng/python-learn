#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pip install open3d pandas numpy scipy

import pandas as pd
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from filterpy.kalman import KalmanFilter
from scipy.interpolate import splprep, splev


class TestLaneLoad:
    def __init__(self):
        self.data_dir = "/Users/fusheng/WorkSpace/CompanyWork/work-fusheng/robot-pro/htcbot_online_ws/test/data/"
        self.lane_file_dir = self.data_dir + "hkgc/steer_10230142/lidar_mode/pathes/"
        self.gps_file_path = self.lane_file_dir + "lane_1_trans.csv"
        self.topology_lines_count = 5  # 拓扑关系行的数量
        self.show_method = "matplotlib"  # 选择显示方式 matplotlib | open3d
        self.curvature_threshold = 0.05  # 曲率阈值，用于判断直线与弯道

    def load_lane_data(self, path):
        try:
            with open(path, 'r') as file:
                lines = file.readlines()
            # 保持拓扑关系部分不变
            topology_lines = lines[:self.topology_lines_count]
            # 剩余部分是轨迹数据
            trajectory_lines = lines[self.topology_lines_count:]
            trajectory_data = pd.DataFrame(
                [list(map(float, line.replace(',', '').split())) for line in trajectory_lines])
            # 提取 x 和 y 坐标
            trajectory_points = trajectory_data[[0, 1]].values
            # 为缺少的 z 坐标添加默认值 0，扩展为 (x, y, z)
            z_values = np.zeros((trajectory_points.shape[0], 1))
            trajectory_points_3d = np.hstack((trajectory_points, z_values))
            return trajectory_points_3d
        except Exception as e:
            print(f"Error loading lane: {e}")

    def calculate_curvature(self, trajectory):
        # 计算曲率
        dx = np.gradient(trajectory[:, 0])
        dy = np.gradient(trajectory[:, 1])
        ddx = np.gradient(dx)
        ddy = np.gradient(dy)
        curvature = np.abs(dx * ddy - dy * ddx) / (dx ** 2 + dy ** 2) ** 1.5
        return curvature

    def plot_with_matplotlib(self, trajectory_points):
        curvature = self.calculate_curvature(trajectory_points)

        plt.figure()
        for i in range(len(curvature) - 1):
            start_point = trajectory_points[i]
            end_point = trajectory_points[i + 1]
            if curvature[i] < self.curvature_threshold:
                # 直线段，绘制为绿色
                plt.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='green')
            else:
                # 弯道，绘制为红色
                plt.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='red')

        plt.title("Trajectory Visualization with Curvature-Based Coloring")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)
        plt.axis('equal')  # 确保比例相等
        plt.show()

    def run(self):
        trajectory_points = self.load_lane_data(self.gps_file_path)

        if self.show_method == "matplotlib":
            self.plot_with_matplotlib(trajectory_points)
        else:
            # 原始轨迹
            origin_lane = self.convert_lane_visualize_data(trajectory_points, [0, 1, 0])
            o3d.visualization.draw_geometries([origin_lane], window_name="Trajectory Visualization")

if __name__ == "__main__":
    tester = TestLaneLoad()
    tester.run()
