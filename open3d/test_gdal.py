# pip install gdal open3d numpy

# export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"
# export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git"
# export HOMEBREW_INSTALL_FROM_API=1
# brew update


# sudo apt update
# sudo apt install -y gdal-bin libgdal-dev
# sudo apt install -y python3 python3-pip
# pip3 install GDAL

from osgeo import gdal, ogr
import json
print("导入成功！")

class TestGdal:

    def __init__(self):
        pass

    def parse_dxf(self, file_path):
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

        return ds

    def read_layer(self, dxf_ds):
        # 读取图层要素
        layer = dxf_ds.GetLayer()
        features = []
        # 特征集合
        for feature in layer:
            geometry = feature.GetGeometryRef()
            geometry_json = json.loads(geometry.ExportToJson())
            print(geometry_json)
            # 属性(拓展信息)
            properties = {}
            for i in range(feature.GetFieldCount()):
                # 属性字段
                field_name = layer.GetLayerDefn().GetFieldDefn(i).GetName()
                # 属性值
                field_value = feature.GetField(i)
                properties[field_name] = field_value
            features.append({"type": "Feature", "geometry": geometry_json, "properties": properties})
        geojson = {"type": "FeatureCollection", "features": features}
        return geojson
    
    def save_geojson(self, dxf_json, output_file):
        """
        将 GeoJSON 数据保存到文件。

        :param dxf_json: GeoJSON 格式的字典。
        :param output_file: 输出文件路径。
        """
        try:
            # 将 GeoJSON 数据写入文件
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(dxf_json, f, indent=4, ensure_ascii=False)
            print(f"GeoJSON 文件已保存: {output_file}")
        except Exception as e:
            print(f"保存 GeoJSON 文件失败: {e}")
            raise

if __name__ == "__main__":
    t = TestGdal()
    dxf_path = "/Users/fusheng/htcbot_online_ws/src/test/WHTHJC_ZHT_B1.dxf"
    output_file = "t.json"
    dxf_ds = t.parse_dxf(dxf_path)
    dxf_json = t.read_layer(dxf_ds)
    t.save_geojson(dxf_json, output_file)
