#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pip install filterpy

import pandas as pd
import numpy as np
import open3d as o3d
from filterpy.kalman import ExtendedKalmanFilter

class TestLaneTools:

    def __init__(self) -> None:
        self.lane_file_dir = "/Users/fusheng/Desktop/steer_10230142/lidar_mode/pathes/"
        self.gps_file_path = self.lane_file_dir + "gps_lane_1.csv"
        self.topology_lines_count = 5  # 拓扑关系行的数量

    def run(self):
        pass

    def load_lane_data(self, path):
        try:
            with open(path, 'r') as file:
                lines = file.readlines()
            # 拓扑关系部分保持不变
            topology_lines = lines[:self.topology_lines_count]
            # 剩余部分是轨迹数据
            trajectory_lines = lines[self.topology_lines_count:]
            trajectory_data = pd.DataFrame([list(map(float, line.replace(',', '').split())) for line in trajectory_lines])
            # 提取 x 和 y 坐标
            # trajectory_points = trajectory_data[[0, 1]].values
            trajectory_points = trajectory_data[[0, 1, 2]].values
            # 为缺少的 z 坐标添加默认值 0，扩展为 (x, y, z)
            # z_values = np.zeros((trajectory_points.shape[0], 1))
            # trajectory_points_3d = np.hstack((trajectory_points, z_values))
            # 提取四元数，假设它们在第三到第六列
            quaternion_data = trajectory_data.iloc[:, 2:6].values
            return trajectory_points, quaternion_data
        except Exception as e:
            print(f"Error load lane: {e}")

    def smooth_lane(self, lane_data):
        pass


