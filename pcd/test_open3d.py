import os
import time

import open3d as o3d
import numpy as np

def load_dynamic_map():
    # 加载 PCD 文件目录
    pcd_folder = "/Users/fusheng/WorkSpace/CompanyWork/work-fusheng/learn-pro/python-learning/pcd/dynamic_map"
    frame_delay = 0.2   # 每一帧的延迟时间(s)

    # 获取所有PCD文件路径
    pcd_files = sorted([f for f in os.listdir(pcd_folder) if f.endswith(".pcd")])

    for pcd_file in pcd_files:
        # 构建完整的PCD文件路径
        pcd_path = os.path.join(pcd_folder, pcd_file)
        # 加载PCD文件
        point_cloud = o3d.io.read_point_cloud(pcd_path)
        # 可视化点云
        o3d.visualization.draw_geometries([point_cloud])
        # 等待延迟时间
        time.sleep(frame_delay)

def load_dynamic_map_agg():
    # 加载 PCD 文件目录
    pcd_folder = "/Users/fusheng/WorkSpace/CompanyWork/work-fusheng/learn-pro/python-learning/pcd/dynamic_map"
    frame_delay = 0.2   # 每一帧的延迟时间(s)

    # 获取所有PCD文件路径
    pcd_files = sorted([os.path.join(pcd_folder, f) for f in os.listdir(pcd_folder) if f.endswith(".pcd")])

    # 创建一个空点云对象
    merged_point_cloud = o3d.geometry.PointCloud()

    # 可视化窗口
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    for pcd_file in pcd_files:
        # 构建完整的PCD文件路径
        point_cloud = o3d.io.read_point_cloud(pcd_file)
        # 聚合到整体点云中
        merged_point_cloud += point_cloud

    # 可视化聚合后的点云
    o3d.visualization.draw_geometries([merged_point_cloud])

def load_static_map():
    # 加载 PCD 文件
    pcd_file = "pcd/origin.pcd"
    # pcd_file = "/Users/fusheng/WorkSpace/CompanyWork/work-fusheng/learn-pro/python-learning/pcd/e2zb/static.pcd"
    point_cloud = o3d.io.read_point_cloud(pcd_file)

    # 可视化点云
    o3d.visualization.draw_geometries([point_cloud])

def rotation_pcd_map():
    file_path = "pcd/origin.pcd"
    output_file_path = "pcd/transformed.pcd"
    rotation_angle_degrees = 37.8536
    # 加载点云
    original_pcd = o3d.io.read_point_cloud(file_path)

    # 复制原始点云以进行变换
    transformed_pcd = original_pcd.voxel_down_sample(voxel_size=0.02).translate((0, 0, 0))
    # transformed_pcd = original_pcd

    # 创建旋转矩阵
    rotation_angle_radians = np.deg2rad(rotation_angle_degrees)
    rotation_matrix = transformed_pcd.get_rotation_matrix_from_axis_angle([0, 0, rotation_angle_radians])

    # 应用旋转变换
    transformed_pcd = transformed_pcd.rotate(rotation_matrix, center=(0, 0, 0))

    o3d.io.write_point_cloud(output_file_path, transformed_pcd)

    # 创建两个可视化窗口
    original_pcd.paint_uniform_color([1, 0, 0])  # 原始点云显示为红色
    transformed_pcd.paint_uniform_color([0, 1, 0])  # 变换后的点云显示为绿色

    # 可视化原始点云和变换后的点云
    # o3d.visualization.draw_geometries([original_pcd], window_name="Original Point Cloud Viewer")
    # o3d.visualization.draw_geometries([transformed_pcd], window_name="Transformed Point Cloud Viewer")

    # 可视化原始点云和变换后的点云
    o3d.visualization.draw_geometries([original_pcd, transformed_pcd], window_name="Original and Transformed Point Cloud Viewer")

if __name__ == '__main__':
    rotation_pcd_map()