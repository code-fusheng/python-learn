import numpy as np
import matplotlib.pyplot as plt

# Simulation settings
dt = 0.1  # time step
steps = 100  # number of steps

# Initialize state vector [x, y, v, theta, a, omega]
true_x = np.array([0, 0, 1, np.pi/4, 0.1, 0.05])  # initial true state
estimated_x = np.array([0, 0, 0, 0, 0, 0])  # initial estimated state

# Covariance matrices
P = np.eye(6) * 0.1  # initial covariance
Q = np.diag([0.1, 0.1, 0.05, 0.05, 0.01, 0.01])  # process noise
R = np.diag([0.5, 0.5])  # measurement noise

# Observation matrix H
H = np.array([
    [1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0]
])

# Initialize lists to store true, observed, and estimated positions
true_positions = []
observed_positions = []
estimated_positions = []

# State transition and Jacobian functions
def state_transition(x, dt):
    x_new = np.zeros_like(x)
    x_new[0] = x[0] + x[2] * np.cos(x[3]) * dt
    x_new[1] = x[1] + x[2] * np.sin(x[3]) * dt
    x_new[2] = x[2] + x[4] * dt
    x_new[3] = x[3] + x[5] * dt
    x_new[4] = x[4]
    x_new[5] = x[5]
    return x_new

def jacobian_F(x, dt):
    F = np.eye(6)
    F[0, 2] = np.cos(x[3]) * dt
    F[0, 3] = -x[2] * np.sin(x[3]) * dt
    F[1, 2] = np.sin(x[3]) * dt
    F[1, 3] = x[2] * np.cos(x[3]) * dt
    F[2, 4] = dt
    F[3, 5] = dt
    return F

# Prediction and update functions
def predict(x, P, Q, dt):
    F = jacobian_F(x, dt)
    x = state_transition(x, dt)
    P = F @ P @ F.T + Q
    return x, P

def update(x, P, z, H, R):
    y = z - H @ x
    S = H @ P @ H.T + R
    K = P @ H.T @ np.linalg.inv(S)
    x = x + K @ y
    P = (np.eye(len(x)) - K @ H) @ P
    return x, P

# Simulate EKF with noisy observations
for _ in range(steps):
    # True position
    true_x = state_transition(true_x, dt)
    true_positions.append(true_x[:2])

    # Noisy observation (GPS-like)
    z = true_x[:2] + np.random.normal(0, 0.5, 2)
    observed_positions.append(z)

    # EKF Prediction and Update
    estimated_x, P = predict(estimated_x, P, Q, dt)
    estimated_x, P = update(estimated_x, P, z, H, R)
    estimated_positions.append(estimated_x[:2])

# Convert lists to arrays for easy plotting
true_positions = np.array(true_positions)
observed_positions = np.array(observed_positions)
estimated_positions = np.array(estimated_positions)

# Plot results
plt.figure(figsize=(10, 8))
plt.plot(true_positions[:, 0], true_positions[:, 1], label='True Position', color='blue')
plt.scatter(observed_positions[:, 0], observed_positions[:, 1], label='Observed (Noisy GPS)', color='red', s=10, alpha=0.5)
plt.plot(estimated_positions[:, 0], estimated_positions[:, 1], label='EKF Estimated Position', color='green')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.legend()
plt.title('EKF Position Tracking with Noisy GPS Observations')
plt.grid()
plt.show()
