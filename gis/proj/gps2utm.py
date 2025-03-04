from pyproj import Transformer

# 参数1：WGS84地理坐标系统 对应 4326
# 参数2：坐标系WKID 广州市 WGS_1984_UTM_Zone_49N 对应 32649
# 天津市 WGS_1984_UTM_Zone_50N
transformer = Transformer.from_crs("epsg:4326", "epsg:32650")

lat = 39.134670952691
lon = 117.363634982639

x, y = transformer.transform(lat, lon)
print("x:", x, "y:", y)