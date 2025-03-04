import serial
import time
import binascii
import crcmod.predefined

# CRC16-MODBUS校验
crc16_func = crcmod.predefined.mkPredefinedCrcFun('crc16_modbus')

# 其他串口设置不变...
...

cmd2 = bytearray(b'\x01\x03\x01\x06\x00\x04')

# 添加CRC校验
crc_value = crc16_func(cmd2)
cmd2.extend(crc_value.to_bytes(2, byteorder='big'))

# 发送命令并接收响应
for _ in range(10):
    print("write {} to serial".format(cmd2.hex()))
    serial_client.write(cmd2)

    time.sleep(0.5)  # 增加延时，等待响应

    # 读取响应，假设设备返回2个字节数据加上CRC校验值
    response = serial_client.read(6)

    # 检查响应长度
    if len(response) == 6:
        data, crc_received = response[:4], response[4:]
        crc_calculated = crc16_func(data)

        if crc_calculated == int.from_bytes(crc_received, byteorder='big'):
            measurement_value = int.from_bytes(data[2:], byteorder='big')
            print(f"测量值: {measurement_value} mm")
        else:
            print("CRC校验失败")
    else:
        print("响应长度不符预期")

serial_client.close()