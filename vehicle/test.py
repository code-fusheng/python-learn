import math

# 定义车辆参数
L = 2.5  # 轴距，单位：米
W = 1.5  # 轮距，单位：米
theta_f = math.radians(30)  # 前轮转角，单位：弧度
theta_r = math.radians(30)  # 后轮转角，单位：弧度
v_fl = 2.0  # 前左轮速度，单位：米/秒
v_fr = 2.0  # 前右轮速度，单位：米/秒

# 计算前后轮转向半径
R_f = L / math.tan(theta_f)
R_r = L / math.tan(theta_r)

# 计算车辆瞬时转向半径
R = 1 / (1 / R_f + 1 / R_r)

# 计算车辆线速度和角速度
v = (v_fl + v_fr) / 2
omega = v / R

# 更新车辆位姿
delta_t = 0.1  # 时间间隔，单位：秒
theta = 0.0  # 初始航向角，单位：弧度
x, y = 0.0, 0.0  # 初始位置，单位：米

x += v * math.cos(theta) * delta_t
y += v * math.sin(theta) * delta_t
theta += omega * delta_t

print(f"车辆新位姿：x = {x:.2f} m, y = {y:.2f} m, θ = {math.degrees(theta):.2f}°")
