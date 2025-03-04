import json
import gzip

def compress_json(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)  # 从文件中加载JSON数据
    json_data = json.dumps(data)  # 将数据转换为JSON字符串
    compressed_data = gzip.compress(json_data.encode('utf-8'))  # 使用gzip进行压缩
    with open(output_file, 'wb') as file:
        file.write(compressed_data)  # 将压缩后的数据写入新文件

def decompress_json(file_path):
    with open(file_path, 'rb') as file:
        compressed_data = file.read()  # 从文件中读取压缩数据
    decompressed_data = gzip.decompress(compressed_data)  # 使用gzip进行解压缩
    json_data = decompressed_data.decode('utf-8')  # 将解压缩后的数据转换为字符串
    data = json.loads(json_data)  # 将字符串转换为Python对象
    return data

# 示例用法
input_file_path = 'base64.json'
output_file_path = 'compressed_base64.json.gz'
compress_json(input_file_path, output_file_path)
decompressed_data = decompress_json(output_file_path)
print(decompressed_data)