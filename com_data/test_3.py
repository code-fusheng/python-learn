#!/usr/bin/env python3
# -*-coding:utf-8-*-

# pip install modbus_tk
# pip install pymodbus

import sys

sys.path.append("/Users/fusheng/opt/anaconda3/envs/learn-py39/lib/python3.9/site-packages")

from pymodbus.client import ModbusSerialClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

# 串口设置
SERIAL_PORT = '/dev/cu.usbserial-B0019JD8'  # 串口设备路径，根据你的系统配置而定
BAUDRATE = 9600  # 波特率
PARITY = 'N'  # 校验位：None (N), Even (E), Odd (O)
STOPBITS = 1  # 停止位
BYTESIZE = 8  # 数据位

# 寄存器地址
REGISTER_ADDRESS = 0
NUM_REGISTERS = 1  # 要读取的寄存器数量

# 创建Modbus串口客户端
client = ModbusSerialClient(
    method='rtu',
    port=SERIAL_PORT,
    baudrate=BAUDRATE,
    parity=PARITY,
    stopbits=STOPBITS,
    bytesize=BYTESIZE
)

try:
    # 连接到Modbus设备
    if client.connect():
        # 读取保持寄存器的值
        result = client.read_holding_registers(REGISTER_ADDRESS, NUM_REGISTERS, unit=1)  # unit参数表示Modbus设备的地址
        if result.isError():
            print("读取寄存器时发生错误:", result)
        else:
            # 解码读取的寄存器值
            decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big)
            value = decoder.decode_32bit_float()
            print("寄存器值:", value)
    else:
        print("无法连接到Modbus设备")

finally:
    # 关闭Modbus连接
    client.close()
