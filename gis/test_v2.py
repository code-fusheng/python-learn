import pandas as pd
import numpy as np
from scipy.optimize import least_squares

# 设置要读取的行数和跳过的行数
nrows = 1000  # 读取的总行数
skiprows = lambda i: (i < 5) or ((i - 5) % 800 != 0 and i != nrows - 1)  # 要跳过的行数

# 从CSV文件中读取数据，只读取前三个字段，无列名
gps_df = pd.read_csv("gps_lane_1.csv", skiprows=skiprows, header=None, usecols=[0, 1, 2])
base_df = pd.read_csv("lane_1.csv", skiprows=skiprows, header=None, usecols=[0, 1, 2])

# 提取数据为numpy数组
point_cloud1 = gps_df.to_numpy()
point_cloud2 = base_df.to_numpy()

# 定义坐标转换函数
def transform(params, xyz):
    # 参数格式：[平移量_x, 平移量_y, 平移量_z]
    tx, ty, tz = params
    # 应用平移
    xyz_translated = xyz + [tx, ty, tz]
    return xyz_translated

# 定义误差函数
def error_func(params, xyz1, xyz2):
    xyz_transformed = transform(params, xyz1)
    return np.ravel(xyz_transformed - xyz2)

# 初始化参数估计值
initial_params = np.zeros(3)

# 使用最小二乘法拟合参数
result = least_squares(error_func, initial_params, args=(point_cloud1, point_cloud2))

# 获取估计的参数
estimated_params = result.x

# 打印估计的参数
print("Estimated Translation Parameters (x, y, z):", estimated_params)

# 测试转换函数
test_point_cloud_point = np.random.rand(3)  # 测试用的点云坐标
transformed_point = transform(estimated_params, test_point_cloud_point)
print("Transformed Point:", transformed_point)
