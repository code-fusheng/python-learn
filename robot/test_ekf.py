import numpy as np

# 初始化参数
dt = 0.1  # 时间步长，假设为0.1秒

# 状态向量: [x, y, v, theta, a, omega] 
x = np.array([0, 0, 0, 0, 0, 0])  # 初始状态 [位置x, 位置y, 速度, 航向角, 加速度, 角速度]

# 状态协方差矩阵
P = np.eye(6) * 0.1  # 初始不确定性

# 过程噪声协方差矩阵 Q (根据系统的加速度和角速度噪声调整)
Q = np.diag([0.1, 0.1, 0.1, 0.1, 0.1, 0.1])

# 观测噪声协方差矩阵 R (根据GPS和IMU精度调整)
R = np.diag([0.5, 0.5])

# 状态转移矩阵函数 F (根据当前状态 x 非线性计算)
def state_transition(x, dt):
    x_new = np.zeros_like(x)
    x_new[0] = x[0] + x[2] * np.cos(x[3]) * dt  # x' = x + v * cos(theta) * dt
    x_new[1] = x[1] + x[2] * np.sin(x[3]) * dt  # y' = y + v * sin(theta) * dt
    x_new[2] = x[2] + x[4] * dt                 # v' = v + a * dt
    x_new[3] = x[3] + x[5] * dt                 # theta' = theta + omega * dt
    x_new[4] = x[4]                             # a' = a (假设加速度保持不变)
    x_new[5] = x[5]                             # omega' = omega (假设角速度保持不变)
    return x_new

# 雅可比矩阵 F (状态转移模型对状态的偏导数)
def jacobian_F(x, dt):
    F = np.eye(6)
    F[0, 2] = np.cos(x[3]) * dt
    F[0, 3] = -x[2] * np.sin(x[3]) * dt
    F[1, 2] = np.sin(x[3]) * dt
    F[1, 3] = x[2] * np.cos(x[3]) * dt
    F[2, 4] = dt
    F[3, 5] = dt
    return F

# 观测矩阵 H (测量 [x, y])
H = np.array([
    [1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0]
])

# EKF 预测步骤
def predict(x, P, Q, dt):
    F = jacobian_F(x, dt)
    x = state_transition(x, dt)
    P = F @ P @ F.T + Q
    return x, P

# EKF 更新步骤
def update(x, P, z, H, R):
    y = z - H @ x                    # 计算测量残差
    S = H @ P @ H.T + R               # 计算残差协方差
    K = P @ H.T @ np.linalg.inv(S)    # 计算卡尔曼增益
    x = x + K @ y                     # 更新状态
    P = (np.eye(len(x)) - K @ H) @ P  # 更新协方差
    return x, P

# 模拟EKF流程
for t in range(100):  # 假设100个时间步
    # 预测步骤
    x, P = predict(x, P, Q, dt)
    
    # 假设从传感器获得观测数据 z
    z = np.array([x[0] + np.random.normal(0, 0.5), x[1] + np.random.normal(0, 0.5)])  # 模拟GPS位置测量噪声
    
    # 更新步骤
    x, P = update(x, P, z, H, R)
    
    # 输出当前估计的状态
    print(f"Step {t+1}, Estimated Position: ({x[0]:.2f}, {x[1]:.2f}), Velocity: {x[2]:.2f}, Heading: {x[3]:.2f}")
