import rospy
from geometry_msgs.msg import Twist
from evdev import InputDevice, categorize, ecodes

# 设备路径 (根据系统上的具体路径调整)
G29_PATH = '/dev/input/eventXX'  # 请用 G29 的实际路径替换 'eventXX'

# 初始化 ROS 节点
rospy.init_node('g29_cmd_vel_publisher')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
cmd_vel_msg = Twist()

# 打开 G29 设备
try:
    g29 = InputDevice(G29_PATH)
except FileNotFoundError:
    rospy.logerr("无法找到 G29 设备，请确认路径是否正确")
    exit(1)

# 配置最大速度和角速度（可以根据需要调整）
MAX_LINEAR_VELOCITY = 1.0  # 最大线速度
MAX_ANGULAR_VELOCITY = 1.0  # 最大角速度

# 映射函数
def map_axis(value, max_input, max_output):
    return (value / max_input) * max_output

# 主循环
rate = rospy.Rate(50)  # 控制频率
while not rospy.is_shutdown():
    for event in g29.read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_X:  # 方向盘轴
                steering_angle = event.value - 32768  # 转换为中心值 0
                cmd_vel_msg.angular.z = map_axis(steering_angle, 32768, MAX_ANGULAR_VELOCITY)

            elif event.code == ecodes.ABS_RZ:  # 油门踏板
                throttle = event.value
                cmd_vel_msg.linear.x = map_axis(65535 - throttle, 65535, MAX_LINEAR_VELOCITY)

            elif event.code == ecodes.ABS_Z:  # 刹车踏板
                brake = event.value
                brake_effect = map_axis(brake, 65535, MAX_LINEAR_VELOCITY)
                cmd_vel_msg.linear.x -= brake_effect

        pub.publish(cmd_vel_msg)
        rate.sleep()