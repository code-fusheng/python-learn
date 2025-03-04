#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pip install onnx
# pip install open3d

import os
import open3d as o3d
from osgeo import gdal, ogr
import json
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QDoubleValidator
import numpy as np
import sys
import copy

cur_dir = os.path.dirname(os.path.abspath(__file__))

class Open3DVisualizer(QThread):

    # 自定义信号，用于通知主线程可视化已经启动
    visualization_started = pyqtSignal()

    def __init__(self):
        super().__init__()
        print("cur_dir: " + cur_dir)
        # parent_directory = os.path.dirname(cur_dir)
        self.pcd_file_path = os.path.join(cur_dir, "static_whthjc_fwzht_0110.pcd")
        self.geojson_file_path = os.path.join(cur_dir, "static_whthjc_fwzht_0110.json")
        self.dxf_file_path = os.path.join(cur_dir, "static_whthjc_fwzht_0110-.dxf")

        self.show_cad = True  # 默认显示 CAD 图纸
        # self.translation = np.array([5.35, -50.0, 0.0])  # 初始平移
        self.translation = np.array([-4.5, -45.0, 0.0])  # 初始平移
        # 输入角度（单位：度）
        roll_deg = 0  # 绕X轴旋转 10度
        pitch_deg = 0   # 绕Y轴旋转 20度
        yaw_deg = 2  # 绕Z轴旋转 30度

        # 转换为弧度
        roll = self.deg_to_rad(roll_deg)
        pitch = self.deg_to_rad(pitch_deg)
        yaw = self.deg_to_rad(yaw_deg)
        # 计算最终的旋转矩阵
        self.rotation = np.dot(self.rotation_matrix_z(yaw), np.dot(self.rotation_matrix_y(pitch), self.rotation_matrix_x(roll)))

        print("Rotation Matrix:")
        print(self.rotation)

        # self.rotation = np.eye(3)  # 初始旋转矩阵（单位矩阵）
        self.scale_factor = 2.05  # 初始缩放因子

        self.cad_center = {}
        self.pcd_center = {}

        self.ori_dxf_data = None
        self.ori_pcd_data = None

    # 角度转换为弧度
    def deg_to_rad(self, degrees):
        return degrees * np.pi / 180.0

    # 绕X轴旋转矩阵
    def rotation_matrix_x(self, roll):
        return np.array([
            [1, 0, 0],
            [0, np.cos(roll), -np.sin(roll)],
            [0, np.sin(roll), np.cos(roll)]
        ])

    # 绕Y轴旋转矩阵
    def rotation_matrix_y(self, pitch):
        return np.array([
            [np.cos(pitch), 0, np.sin(pitch)],
            [0, 1, 0],
            [-np.sin(pitch), 0, np.cos(pitch)]
        ])

    # 绕Z轴旋转矩阵
    def rotation_matrix_z(self, yaw):
        return np.array([
            [np.cos(yaw), -np.sin(yaw), 0],
            [np.sin(yaw), np.cos(yaw), 0],
            [0, 0, 1]
        ])

    def load_point_cloud(self, pcd_file):
        """从 PCD 文件加载点云数据."""
        point_cloud = o3d.io.read_point_cloud(pcd_file)
        return point_cloud
    
    def load_dxf(self, file_path):
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
        gdal.SetConfigOption("SHAPE_ENCODING", "")
        gdal.SetConfigOption("DXF_ENCODING", "ASCII")  # 设置DXF缺省编码
        # 打开 DXF 文件
        ds = ogr.Open(file_path)
        if ds is None:
            raise ValueError("无法打开 DXF 文件")
        # 获取图层
        layer = ds.GetLayer()
        # 获取图层边界
        extent = layer.GetExtent()
        center_x = (extent[0] + extent[1]) / 2
        center_y = (extent[2] + extent[3]) / 2
        print(f"extent: {extent[0]} {extent[1]} {extent[2]} {extent[3]}")
        print(f"center: ({center_x}, {center_y})")

        geometries = []
        # 遍历图层中的每个要素
        POINT_COUNT = 0
        LINESTRING_COUNT = 0
        MULTILINESTRING_COUNT = 0
        UNKNOWN_COUNT = 0
        for feature in layer:
            geometry = feature.GetGeometryRef()
            if geometry.GetGeometryName() == "LINESTRING":
                for i in range(feature.GetFieldCount()):
                    # 属性字段
                    field_name = layer.GetLayerDefn().GetFieldDefn(i).GetName()
                    # 属性值
                    field_value = feature.GetField(i)
                    if field_name == "Layer" and field_value == "HTC-外轮廓":
                        print(f"field_name: {field_name} field_value: {field_value}")
                        LINESTRING_COUNT += 1
                        # continue
                        # 如果是 LINESTRING 类型，提取坐标点
                        points = [(geometry.GetX(i), geometry.GetY(i), 0) for i in range(geometry.GetPointCount())]
                        line_set = o3d.geometry.LineSet()
                        line_set.points = o3d.utility.Vector3dVector(points)
                        lines = [(i, i + 1) for i in range(len(points) - 1)]  # 生成线的索引
                        line_set.lines = o3d.utility.Vector2iVector(lines)
                        geometries.append(line_set)
            elif geometry.GetGeometryName() == "POINT":
                POINT_COUNT += 1
                continue
                # 如果是 POINT 类型，提取坐标点并创建点云
                points = [(geometry.GetX(), geometry.GetY(), 0)]
                point_cloud = o3d.geometry.PointCloud()
                point_cloud.points = o3d.utility.Vector3dVector(points)
                geometries.append(point_cloud)
            elif geometry.GetGeometryName() == "MULTILINESTRING":
                # 
                MULTILINESTRING_COUNT += 1
                # continue
                # 如果是 MULTILINESTRING 类型，处理每个子线段
                for i in range(geometry.GetGeometryCount()):
                    sub_geometry = geometry.GetGeometryRef(i)
                    points = [(sub_geometry.GetX(j), sub_geometry.GetY(j), 0) for j in range(sub_geometry.GetPointCount())]
                    line_set = o3d.geometry.LineSet()
                    line_set.points = o3d.utility.Vector3dVector(points)
                    lines = [(j, j + 1) for j in range(len(points) - 1)]  # 生成子线段的线索引
                    line_set.lines = o3d.utility.Vector2iVector(lines)
                    geometries.append(line_set)
            else: 
                print(geometry.GetGeometryName())
                UNKNOWN_COUNT += 1
        print(f"元素统计")
        print(f"Point: {POINT_COUNT}")
        print(f"LineString: {LINESTRING_COUNT}")
        print(f"MultiLineString: {MULTILINESTRING_COUNT}")
        print(f"Unknown: {UNKNOWN_COUNT}")

        return geometries
    
    def trans_geometries(self, geometries):
        geometries_t = []
        for geometry in geometries:
            geometry_t = self.apply_transformation(geometry)
            geometries_t.append(geometry_t)
        return geometries_t
    
    def apply_transformation(self, geometry):
        """应用平移、旋转、缩放变换"""
        # 应用平移
        geometry.points = o3d.utility.Vector3dVector(np.asarray(geometry.points) + self.translation)
        # 应用旋转
        points = np.asarray(geometry.points)
        geometry.points = o3d.utility.Vector3dVector(np.dot(points, self.rotation.T))
        # 应用缩放
        geometry.points = o3d.utility.Vector3dVector(np.asarray(geometry.points) * self.scale_factor)
        return geometry

    def debug_point_cloud(self, point_cloud):
        # 输出所有的属性和方法
        print("PointCloud 对象的所有属性和方法:")
        for attr in dir(point_cloud):
            print(attr)
        # 输出点云的基本属性
        print("点云的基本属性:")
        print(f"点云中点的数量: {len(point_cloud.points)}")
        print(f"点云的类型: {point_cloud.Type}")  # 如果存在颜色信息
        print(f"点云的法线: {point_cloud.normals}")  # 如果存在法线信息
        # 获取点云的最小和最大边界
        min_bound = point_cloud.get_min_bound()
        max_bound = point_cloud.get_max_bound()
        center = (min_bound + max_bound) / 2
        print(f"Min Bound: {min_bound}")
        print(f"Max Bound: {max_bound}")
        print(f"Center: {center}")
    
    def visualize_point_cloud(self, cloud=None, clouds=None):
        """可视化点云数据."""
        vis = o3d.visualization.Visualizer()
        vis.create_window(window_name="PCD Point Cloud", width=800, height=600)
        # 设置点的大小
        opt = vis.get_render_option()
        opt.point_size = 1.0
        # 添加点云并启动可视化
        vis.add_geometry(cloud)
        if clouds is not None:
            for cloud in clouds:
                vis.add_geometry(cloud)

        # 获取视图控制对象
        view_control = vis.get_view_control()
        # lookat = np.array([0, 0, 0])  # 视角目标 (比如场景中心)
        # front = np.array([0, 0, -1])  # 视角朝向 Z 轴负方向
        # up = np.array([0, 1, 0])      # 上方向为 Y 轴正方向
        # view_control.set_lookat(lookat)
        # view_control.set_front(front)
        # view_control.set_up(up)

        # 自动调整视图，确保点云能完全显示
        vis.poll_events()
        vis.update_renderer()

        vis.run()
        vis.destroy_window()
        # 当可视化结束时，发出信号
        self.visualization_started.emit()

    def run(self):
        point_cloud = self.load_point_cloud(self.pcd_file_path)
        self.debug_point_cloud(point_cloud)
        self.ori_pcd_data = point_cloud
        downsampled_pcd = point_cloud.voxel_down_sample(1.0)

        # dxf_data = self.load_dxf(self.dxf_file_path)
        # self.ori_dxf_data = copy.deepcopy(dxf_data)
        # dxf_data_t = self.trans_geometries(dxf_data)
        # print(dxf_data)

        # empty_cloud = o3d.geometry.PointCloud()
        # empty_cloud.points = o3d.utility.Vector3dVector([])

        # self.visualize_point_cloud(cloud=point_cloud, clouds=dxf_data)
        self.visualize_point_cloud(cloud=downsampled_pcd, clouds=None)

    def refresh(self):
        print("...")
        dxf_data = copy.deepcopy(self.ori_dxf_data)
        dxf_data_t = self.trans_geometries(dxf_data)
        self.visualize_point_cloud(cloud=self.ori_pcd_data, clouds=dxf_data_t)

class GUIApp(QWidget):
    def __init__(self, visualizer):
        super().__init__()
        self.visualizer = visualizer
        self.setWindowTitle("Param Tools")
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()

        # 添加启动按钮
        self.start_button = QPushButton("Start Visualization", self)
        self.start_button.clicked.connect(self.start_visualization)
        layout.addWidget(self.start_button)

        # 添加平移输入框
        self.translation_x_input = QLineEdit(self)
        self.translation_x_input.setPlaceholderText("Translation X")
        self.translation_x_input.setText("2.0")
        layout.addWidget(QLabel("Translation X:"))
        layout.addWidget(self.translation_x_input)

        self.translation_y_input = QLineEdit(self)
        self.translation_y_input.setPlaceholderText("Translation Y")
        self.translation_y_input.setText("-45.0")
        layout.addWidget(QLabel("Translation Y:"))
        layout.addWidget(self.translation_y_input)

        self.translation_z_input = QLineEdit(self)
        self.translation_z_input.setPlaceholderText("Translation Z")
        self.translation_z_input.setText("10.0")
        layout.addWidget(QLabel("Translation Z:"))
        layout.addWidget(self.translation_z_input)

        # 添加旋转输入框
        self.rotation_input = QLineEdit(self)
        self.rotation_input.setPlaceholderText("Rotation (1x3 matrix as string)")
        '''
        [[ 0.9961947  -0.08715574  0.        ]
        [ 0.08715574  0.9961947   0.        ]
        [ 0.          0.          1.        ]]
        '''
        self.rotation_input.setText("1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0")
        layout.addWidget(QLabel("Rotation Matrix (flattened):"))
        layout.addWidget(self.rotation_input)

        # 添加缩放输入框
        self.scale_input = QLineEdit(self)
        self.scale_input.setPlaceholderText("Scale Factor")
        self.scale_input.setText("2.0")
        layout.addWidget(QLabel("Scale Factor:"))
        layout.addWidget(self.scale_input)

        # 添加刷新按钮
        self.refresh_button = QPushButton("Refresh Visualization", self)
        self.refresh_button.clicked.connect(self.refresh_visualization)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)

        # 启动 Open3D 可视化线程
        self.visualizer.visualization_started.connect(self.on_visualization_started)

    def start_visualization(self):
        """点击按钮启动 Open3D 可视化."""
        # 文件路径
        # self.visualizer = Open3DVisualizer()
        # 启动线程
        self.visualizer.start()

    def refresh_visualization(self):
        print("Refresh")
        translation = np.array([
            float(self.translation_x_input.text()),
            float(self.translation_y_input.text()),
            float(self.translation_z_input.text())
        ])
        rotation_values = list(map(float, self.rotation_input.text().split(',')))
        rotation = np.array(rotation_values).reshape((3, 3))
        scale_factor = float(self.scale_input.text())

        self.visualizer.translation = translation
        self.visualizer.rotation = rotation
        self.visualizer.scale_factor = scale_factor

        self.visualizer.refresh()

    def on_visualization_started(self):
        """可视化开始后执行的回调."""
        print("Open3D visualization started")

if __name__ == "__main__":
    # visualizer = Open3DVisualizer()
    # app = QApplication(sys.argv)
    # gui = GUIApp(visualizer)
    # gui.show()
    # sys.exit(app.exec_())

    visualizer = Open3DVisualizer()
    visualizer.run()

