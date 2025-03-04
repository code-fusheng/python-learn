import numpy as np
from scipy.interpolate import CubicHermiteSpline

# 解析起始点和终止点
start = np.array([39.13385307516667, 117.35775030416667, 0.0, 0.0, 0.0, 0.5730113720946396, 0.8195474162305794], dtype=float)
diff = np.array([39.13386344883333, 117.35775574983333, 0.0, 0.0, 0.0, 0.5591133064170194, 0.8290912558864845], dtype=float)

# 指定生成的点数
num_points = 10

# 插值
t = np.linspace(0, 1, num_points)
smooth_path = np.zeros((num_points, len(start)))
for i in range(len(start)):
    spline = CubicHermiteSpline([0, 1], np.array([start[i], diff[i]]), np.array([0, 0]))  # 使用线性切线插值
    smooth_path[:, i] = spline(t)

for point in smooth_path:
    print(point)
