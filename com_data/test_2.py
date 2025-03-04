#!/usr/bin/env python2
# -*-coding:utf-8-*-

import serial
import time
import struct
import crcmod.predefined


class UltrasonicDriver:

    def __init__(self):
        self.serial_port = "/dev/cu.usbserial-B0019JD8"

        self.crc16_func = crcmod.predefined.mkPredefinedCrcFun('crc16')

    def read_measurement(self, probe_number=1):
        address_offset = {
            1: 0x0106,
            2: 0x0107,
            3: 0x0108,
            4: 0x0109,
        }

        if probe_number not in address_offset:
            raise ValueError("Invalid probe number")

        register_address = address_offset[probe_number]
        command = b'\x01'  # 设备地址
        command += b'\x03'  # 功能码（读取保持寄存器）
        command += struct.pack(">H", register_address)  # 寄存器地址
        command += struct.pack(">H", 1)  # 寄存器数量

        # 计算CRC16校验值
        crc_value = self.crc16_func(command)
        command += crc_value.to_bytes(2, byteorder='big')

        with serial.Serial(port=self.serial_port,
                           baudrate=9600,
                           timeout=1,
                           bytesize=serial.EIGHTBITS,
                           parity=serial.PARITY_NONE,
                           stopbits=serial.STOPBITS_ONE) as ser:

            ser.write(command)
            time.sleep(0.5)  # 等待约100ms以获得响应

            # 读取响应，假设响应为设备地址、功能码、1个字节数据长度、2个字节数据和2个字节CRC校验值
            response = ser.read(8)

            if len(response) == 8:
                device_address, function_code, byte_count, data_high, data_low, crc_high, crc_low = struct.unpack(
                    '>BBBHHH', response)

                # 验证CRC
                calculated_crc = self.crc16_func(response[:6])
                received_crc = (crc_high << 8) | crc_low

                if calculated_crc == received_crc:
                    measurement_value = (data_high << 8) | data_low
                    print(f"探头{probe_number}测量值: {measurement_value} mm")
                else:
                    print("CRC校验失败")
            else:
                print("收到的数据长度不符合预期")


if __name__ == '__main__':
    app = UltrasonicDriver()
    app.read_measurement(probe_number=1)