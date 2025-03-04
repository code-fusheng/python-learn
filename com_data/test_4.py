import serial
import struct
import crcmod

# 串口设置
SERIAL_PORT = '/dev/cu.usbserial-B0019JD8'  # 串口设备路径，根据你的系统配置而定
BAUDRATE = 9600  # 波特率
PARITY = 'N'  # 校验位：None (N), Even (E), Odd (O)
STOPBITS = 1  # 停止位
BYTESIZE = 8  # 数据位

# 设备地址
DEVICE_ADDRESS = 0x01

# 计算CRC16
def calculate_crc16(data):
    crc16 = crcmod.predefined.Crc('modbus')
    crc16.update(data)
    crc_value = crc16.crcValue
    # 将 CRC 校验值的字节顺序反转
    crc_bytes = crc_value.to_bytes(2, byteorder='big')
    crc_bytes_reversed = crc_bytes[::-1]
    return crc_bytes_reversed

# 打开串口
ser = serial.Serial(
    port=SERIAL_PORT,
    baudrate=BAUDRATE,
    parity=PARITY,
    stopbits=STOPBITS,
    bytesize=BYTESIZE,
    timeout=1
)

try:
    if ser.isOpen():
        # 构造要发送的数据
        # 01 03 01 06 00 04 A5 F4
        command = struct.pack('>BBHH', DEVICE_ADDRESS, 0x03, 0x0106, 0x0004)  # 主机发送的命令
        crc = calculate_crc16(command)
        data_to_send = command + crc  # 添加CRC校验值

        print(data_to_send)

        # 将要发送的数据转换为十六进制字符串并打印
        hex_data = ' '.join(format(byte, '02X') for byte in data_to_send)
        print("发送的数据:", hex_data)

        # 发送数据
        ser.write(data_to_send)

        # 读取从机响应数据
        response = ser.read(13)  # 读取从机响应数据
        hex_response = ' '.join(format(byte, '02X') for byte in response)
        print("接收到的响应数据:", hex_response)

        # 提取探头数量
        num_sensors = response[2] // 2  # 除以2是因为每个测量值占两个字节

        # 提取每个探头的测量值
        for i in range(num_sensors):
            # 提取测量值的起始索引
            start_index = 3 + i * 2
            # 提取测量值的高位字节和低位字节
            high_byte = response[start_index]
            low_byte = response[start_index + 1]
            # 计算测量值
            measurement_value = (high_byte << 8) | low_byte
            print(f"探头{i + 1}测量值:", measurement_value, "mm")

except Exception as e:
    print("发生错误:", e)

finally:
    # 关闭串口
    ser.close()
