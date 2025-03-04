import numpy as np
import pandas as pd

def read_vectors_from_file(file_path, start_line, end_line, sample_interval):
    # 读取CSV文件并跳过开始的行
    df = pd.read_csv(file_path, header=None, skiprows=start_line)
    # 选取指定范围内的行并按照采样间隔进行采样
    df = df.iloc[:end_line - start_line + 1:sample_interval]
    vectors = df[[0, 1]].values
    return vectors

def calculate_average_rotation_angle(vectors1, vectors2):
    if vectors1.shape != vectors2.shape:
        raise ValueError("The size of the two vector lists does not match.")

    total_angle = 0.0
    total_radians = 0.0
    total_weight = 0.0
    count = 0

    for i in range(len(vectors1)):
        vector_before = vectors1[i]
        vector_after = vectors2[i]

        norm_vector_before = vector_before / np.linalg.norm(vector_before)
        norm_vector_after = vector_after / np.linalg.norm(vector_after)

        dot_product = np.dot(norm_vector_before, norm_vector_after)
        cos_angle = np.clip(dot_product, -1.0, 1.0)
        angle_radians = np.arccos(cos_angle)
        angle_degrees = np.degrees(angle_radians)

        tenth_percent = int(len(vectors1) * 0.15)
        weight = 0.8 if i < tenth_percent else 1.0

        total_angle += angle_degrees * weight
        total_radians += angle_radians * weight
        total_weight += weight
        count += 1

    average_angle = (total_angle / total_weight) if total_weight > 0 else 0.0
    average_radians = (total_radians / total_weight) if total_weight > 0 else 0.0

    rotation_matrix = np.array([[np.cos(average_radians), -np.sin(average_radians)],
                                [np.sin(average_radians), np.cos(average_radians)]])

    return rotation_matrix, average_angle

if __name__ == "__main__":
    file_path1 = "pathes/gps_lane_1.csv"
    file_path2 = "pathes/lane_1.csv"
    sample_interval = 1
    vectors1 = read_vectors_from_file(file_path1, 10, 1400, sample_interval)
    vectors2 = read_vectors_from_file(file_path2, 10, 1400, sample_interval)

    rotation_matrix, average_angle = calculate_average_rotation_angle(vectors1, vectors2)

    print("Rotation Matrix:")
    print(rotation_matrix)
    print("Average Rotation Angle: {:.2f} degrees".format(average_angle))
