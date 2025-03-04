import open3d as o3d
import ezdxf
import numpy as np

class PCDToDXFConverter:
    def __init__(self, pcd_file):
        self.pcd_file = pcd_file

    def load_pcd(self):
        """加载 PCD 点云文件"""
        pcd = o3d.io.read_point_cloud(self.pcd_file)
        return pcd

    def extract_plane_boundary(self, pcd, distance_threshold=0.05):
        """提取平面上的边界点（最外层轮廓）"""
        # 使用Voxel Grid 降采样
        pcd_down = pcd.voxel_down_sample(voxel_size=0.1)
        
        # 使用RANSAC平面模型提取平面上的点
        plane_model, inlier_indices = pcd_down.segment_plane(distance_threshold=distance_threshold, ransac_n=3, num_iterations=1000)
        inlier_cloud = pcd_down.select_by_index(inlier_indices)
        
        # 将平面上的点提取出来
        inlier_points = np.asarray(inlier_cloud.points)
        
        return inlier_points

    def create_dxf(self, points, output_file="output.dxf"):
        """根据点云创建一个 DXF 文件"""
        # 创建 DXF 文档
        doc = ezdxf.new()
        msp = doc.modelspace()

        # 将点转换为 DXF 中的线段（假设点是顺序排列的）
        for i in range(len(points) - 1):
            start_point = points[i]
            end_point = points[i + 1]
            msp.add_line(start=start_point[:2], end=end_point[:2])

        # 保存 DXF 文件
        doc.saveas(output_file)
        print(f"DXF 文件已保存：{output_file}")

    def convert(self):
        """将 PCD 转换为 DXF 格式"""
        pcd = self.load_pcd()

        # 提取平面上的点
        points_on_plane = self.extract_plane_boundary(pcd)

        # 创建并保存 DXF 文件
        self.create_dxf(points_on_plane)

if __name__ == "__main__":
    pcd_file = "static_whthjc_fwzht_0110.pcd"  # 替换为你的 PCD 文件路径
    converter = PCDToDXFConverter(pcd_file)
    converter.convert()
