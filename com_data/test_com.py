# pip install pyserial
# pip install crcmod


import serial
import serial.tools.list_ports
import crcmod.predefined

class TestCom:

    def __init__(self):
        self.serial = None

        ports = list(serial.tools.list_ports.comports())
        # 输出串口名
        for port, desc, hwid in sorted(ports):
            print(f'Port: {port}, Description: {desc}, Hardware ID: {hwid}')

    def open_com(self, port, baud):
        try:
            self.serial = serial.Serial(port=port, baudrate=baud, timeout=0.2)
        except Exception as e:
            print(f"无法打开串口: {e}")
            exit()

        # 创建一个CRC16校验函数，这里使用标准CRC16校验算法，如果设备使用的是其他CRC算法，请更换
        crc16_func = crcmod.predefined.mkPredefinedCrcFun('crc16')

        # 构造要发送的命令（这里是读取探头1的测量值）
        command = b'\x01\x03\x01\x06\x00\x01'

        command = b'\x01\x03\x01\x06\x00\x04\xA5 F4 '

        # 计算CRC16校验值
        crc_value = crc16_func(command)
        # 将校验值添加到原始报文末尾
        # command_with_crc = command + crc_value.to_bytes(2, byteorder='big')

        self.serial.write(command_with_crc)

        print(f"原始报文: {command.hex()}")
        print(f"CRC16校验值: {crc_value:04X}")
        print(f"带有CRC16校验值的报文: {command_with_crc.hex()}")

        # 接收响应
        response = self.serial.read_until(expected=b'\x01')  # 假设响应以地址0x01开始，这里可以根据实际情况修改
        print(f"收到的原始响应: {response.hex()}")
        if len(response) < 8:  # 根据协议，假设有效响应至少包含8个字节
            print("接收到的数据不完整")
            return

        # 检查CRC（这里假设CRC覆盖了整个响应包，如果不是，请按实际情况调整）
        calculated_crc = crc16_func(response[:-2])
        received_crc = int.from_bytes(response[-2:], byteorder='big')

        if calculated_crc != received_crc:
            print("CRC校验失败")
        else:
            # 解析有效数据
            probe_value = int.from_bytes(response[6:-2], byteorder='big')
            print(f"探头1测量值: {probe_value}mm")

if __name__ == '__main__':
    app = TestCom()
    # app.open_com(port="/dev/cu.usbserial-B0019JD8", baud=9600)