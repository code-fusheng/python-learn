import open3d as o3d
import numpy as np

# 加载 PCD 文件
pcd = o3d.io.read_point_cloud("static_whthjc_fwzht_0110.pcd")

# 将点云保存为 XYZ 文件
o3d.io.write_point_cloud("output.xyz", pcd)