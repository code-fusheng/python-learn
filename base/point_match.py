import csv
from math import radians, sin, cos, sqrt, atan2
import time
import numpy as np
from scipy.interpolate import CubicHermiteSpline

import matplotlib.pyplot as plt
import pandas as pd
from pyproj import Transformer

class PointMathc:

    def __init__(self):
        self.transformer = Transformer.from_crs("epsg:4326", "epsg:32650")
        self.utm_offset_x = 0
        self.utm_offset_y = 0
        pass

    def read_csv_file(self, filename):
        gps_points = []
        with open(filename, 'r') as f:
            csv_reader = csv.reader(f)
            rows = list(csv_reader)
            row_num = len(rows)
            # print("len:", row_num)
            for i in range(5, row_num):
                gps_pose = rows[i]
                # print(gps_pose)
                gps_points.append(gps_pose)
            return gps_points

    def write_csv_file(self, filename, points):
         # 写入CSV文件
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # write trajectory header
            writer.writerow([1])  # id
            writer.writerow([9999])  # length
            writer.writerow([1])  # reverse
            writer.writerow([1])  # pre_node_ids
            writer.writerow([2])  # next_node_ids
            for pst in points:
                pose = [
                    float(pst[0], ),
                    float(pst[1]),
                    float(pst[2]),
                    float(pst[3]),
                    float(pst[4]),
                    float(pst[5]),
                    float(pst[6])
                ]
                writer.writerow(pose)

    def distance_of_two_point_4_gps(self, lat1, lon1, lat2, lon2):
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(float(lat2))
        lon2 = radians(float(lon2))
        # 地球半径（单位：米）
        R = 6371000.0
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return distance

    def search_nearest_point(self, p_lat, p_lon, points):
        start_time = time.time()

        min_distance = float('inf')
        nearest_point = None
        nearest_index = None

        for i, point in enumerate(points):
            # print("point: ", point)
            distance = self.distance_of_two_point_4_gps(p_lat, p_lon, point[0], point[1])
            if distance < min_distance:
                min_distance = distance
                nearest_point = point
                nearest_index = i
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("计算耗时:", elapsed_time, "秒")
        print(nearest_index, nearest_point[0], nearest_point[1] , min_distance)
        return nearest_index, nearest_point, min_distance

    def find_duplicate_points(self, points):
        duplicate_dict = {}
        for i in range(0, len(points)):
            if points[i] == points[i - 1]:
                point_str = str(points[i])
                if point_str not in duplicate_dict:
                    duplicate_dict[point_str] = [i-1, i]
                else:
                    duplicate_dict[point_str].append(i)
        return duplicate_dict

    def interpolate_duplicates(self, points):
        print("points len: ", len(points))
        duplicate_dict = self.find_duplicate_points(points)
        new_points = []
        prev_end_index = -1
        for i, duplicate_indices in enumerate(duplicate_dict.values()):
            # print(duplicate_indices)
            start_index = duplicate_indices[0]
            end_index = duplicate_indices[-1]
            start_point = points[start_index]
            end_point = points[end_index]
            if end_index >= len(points) - 1:
                continue
            first_diff_point = points[end_index + 1]
            # print("start:", start_point)
            # print("diff: ", first_diff_point)
            same_num = end_index - start_index
            # print("len: ", same_num)
            smooth_path = self.slerp_interpolate(start_point, first_diff_point, same_num + 2)
            for i in range(1, same_num + 1):
                points[start_index + i][0] = str(smooth_path[i][0])
                points[start_index + i][1] = str(smooth_path[i][1])
                points[start_index + i][2] = str(smooth_path[i][2])
                points[start_index + i][3] = str(smooth_path[i][3])
                points[start_index + i][4] = str(smooth_path[i][4])
                points[start_index + i][5] = str(smooth_path[i][5])
                points[start_index + i][6] = str(smooth_path[i][6])
        new_points = points
        return new_points

    def slerp_interpolate(self, start_point, end_point, num_points):
        start = np.array(start_point)
        end = np.array(end_point)
        # 插值
        t = np.linspace(0, 1, num_points)
        smooth_path = np.zeros((num_points, len(start)))
        for i in range(len(start)):
            spline = CubicHermiteSpline([0, 1], np.array([start[i], end[i]]), np.array([0, 0]))  # 使用线性切线插值
            smooth_path[:, i] = spline(t)
        return smooth_path

    def show_points(self, points):
        df = pd.DataFrame(points, columns=['lat', 'lon', 'alt', 'x', 'y', 'z', 'w'])
        lats = df['lat'].tolist()
        lons = df['lon'].tolist()
        # 创建一个新的图形
        plt.figure()
        # 绘制散点图，其中x坐标对应x_points，y坐标对应y_points
        plt.scatter(lats, lons, color='blue', marker='o')  # 可以调整颜色和标记形状
        plt.title('path')
        plt.xlabel('lat')
        plt.ylabel('lon')
        # 显示图形
        plt.show()

    def trans_points(self, points):
        result_points = []
        for p in points:
            x, y = self.transformer.transform(p[0], p[1])
            if self.utm_offset_x == 0 or self.utm_offset_y == 0:
                self.utm_offset_x = x
                self.utm_offset_y = y
            # 减去偏移
            x -= self.utm_offset_x
            y -= self.utm_offset_y
            p[0] = x
            p[1] = y
            result_points.append(p)
        return result_points

if __name__ == '__main__':
    app = PointMathc()
    gps_points = app.read_csv_file("gps_lane_1.csv")
    # current_x = 39.134603665
    # current_y = 117.35763397
    # app.search_nearest_point(current_x, current_y, gps_points)
    # duplicate_dict = app.find_duplicate_points(gps_points)
    # for point, indices in duplicate_dict.items():
    #     print(f"{point} : {indices}")
    interpolated_points = app.interpolate_duplicates(gps_points)
    for point in interpolated_points:
        print(point)
        pass
    # print(len(interpolated_points))
    # app.write_csv_file("gps_lane_1_x.csv", interpolated_points)
    t_points = app.trans_points(interpolated_points)
    app.show_points(t_points[0:3000])



