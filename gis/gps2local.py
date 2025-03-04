import numpy as np
from scipy.optimize import least_squares
from pyproj import Transformer
import pandas as pd

# 定义坐标转换函数

def transform(params, xyz):
    # 参数格式：[平移量_x, 平移量_y, 平移量_z]
    tx, ty, tz = params
    # 应用平移
    xyz_translated = xyz + [tx, ty, tz]
    return xyz_translated

# 定义误差函数
def error_func(params, xyz, gps):
    xyz_transformed = transform(params, xyz)
    gps_reshaped = gps[:, :2]  # 仅考虑经度和纬度
    return np.ravel(xyz_transformed[:, :2] - gps_reshaped)

# 定义点云坐标转换为GPS坐标的函数
def point_cloud_to_gps(point_cloud_point, estimated_params):
    # 使用估计的平移参数进行坐标转换
    transformed_point = transform(estimated_params, point_cloud_point)
    return transformed_point

# 定义将GPS坐标转换为UTM坐标的函数
def gps_to_utm(gps_coords):
    transformer = Transformer.from_crs("epsg:4326", "epsg:32650")
    utm_coords = np.array([transformer.transform(lat, lon) for lat, lon, _ in gps_coords])
    return utm_coords

# 定义将UTM坐标转换为GPS坐标的函数
def utm_to_gps(utm_x, utm_y):
    transformer = Transformer.from_crs("epsg:32650", "epsg:4326")
    gps_lon, gps_lat = transformer.transform(utm_x, utm_y)
    return gps_lat, gps_lon

nrows = 1000  # 读取的总行数
skiprows = lambda i: (i < 5) or ((i - 5) % 800 != 0 and i != nrows - 1)  # 要跳过的行数

# 从CSV文件中读取数据，只读取前三个字段，无列名
point_cloud_df = pd.read_csv("lane_1.csv", skiprows=skiprows, header=None, usecols=[0, 1, 2])
gps_df = pd.read_csv("gps_lane_1.csv", skiprows=skiprows, header=None, usecols=[0, 1, 2])

# 提取数据为numpy数组
point_cloud_coords = point_cloud_df.to_numpy()
gps_coords = gps_df.to_numpy()

# 已知的点云坐标
# point_cloud_coords = np.array([[-0.0074727, -0.0132872, -0.0213171],
#                                [63.7246323, 27.9634151, 3.4437842],
#                                [2.3992057, 30.3776798, -0.4356784]])
#
# # 对应的GPS坐标
# gps_coords = np.array([[30.7697428, 114.2050211, 17.9484],
#                        [30.7696065, 114.2057313, 17.45],
#                        [30.7699494, 114.2052249, 18.7824]])

# 将GPS坐标转换为UTM坐标
utm_coords = gps_to_utm(gps_coords)

# 初始化参数估计值
initial_params = np.zeros(3)

# 使用最小二乘法拟合参数
result = least_squares(error_func, initial_params, args=(point_cloud_coords, utm_coords))

# 获取估计的参数
estimated_params = result.x

# 打印估计的参数
print("Estimated Translation Parameters (x, y, z):", estimated_params)

# 测试转换函数
test_point_cloud_point = np.array([42.5664024, 14.8798342, 2.0328827])
transformed_gps_point = point_cloud_to_gps(test_point_cloud_point, estimated_params)
print("Transformed GPS Coordinate:", transformed_gps_point)

# 测试UTM坐标转换为GPS坐标函数
test_utm_x, test_utm_y = transformed_gps_point[0], transformed_gps_point[1]
gps_lat, gps_lon = utm_to_gps(test_utm_x, test_utm_y)
print("GPS Coordinate:", test_utm_x, test_utm_y)

transformer = Transformer.from_crs("epsg:4326", "epsg:32650")
x, y = transformer.transform(30.769622, 114.2054672)
print("x", x, y)

# 114.20554121015978 30.769729699535475
# 114.2054672        30.769622
