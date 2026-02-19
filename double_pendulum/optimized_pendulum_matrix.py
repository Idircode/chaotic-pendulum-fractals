import numpy as np 
import time 
from numpy import sin, cos

m1 = 1.0 # mass of first pendulum bob
m2 = 1.0 # mass of second pendulum bob
l1 = 1.0 # length of first rod
l2 = 1.0 # length of second rod
g = 9.81 # acceleration due to gravity

def derivatives(theta1, theta2, omega1, omega2):
    delta_theta = theta1 - theta2
    sin_delta = np.sin(delta_theta)
    cos_delta = np.cos(delta_theta)

    d_omega1_num = (
        m2 * g * np.sin(theta2) * cos_delta
        - m2 * sin_delta * (l1 * omega1**2 * cos_delta + l2 * omega2**2)
        - (m1 + m2) * g * np.sin(theta1)
    )
    d_omega1 = d_omega1_num / (l1 * (m1 + m2 * sin_delta**2))

    d_omega2_num = (
        (m1 + m2) * (l1 * omega1**2 * sin_delta - g * np.sin(theta2) + g * np.sin(theta1) * cos_delta)
        + m2 * l2 * omega2**2 * sin_delta * cos_delta
    )
    d_omega2 = d_omega2_num / (l2 * (m1 + m2 * sin_delta**2))

    return omega1, d_omega1, omega2, d_omega2

def rk4_step(theta1, theta2, omega1, omega2, dt):
    k1_omega1, k1_domega1, k1_omega2, k1_domega2 = derivatives(theta1, theta2, omega1, omega2)

    k2_omega1, k2_domega1, k2_omega2, k2_domega2 = derivatives(
        theta1 + 0.5 * dt * k1_omega1,
        theta2 + 0.5 * dt * k1_omega2,
        omega1 + 0.5 * dt * k1_domega1,
        omega2 + 0.5 * dt * k1_domega2,
    )

    k3_omega1, k3_domega1, k3_omega2, k3_domega2 = derivatives(
        theta1 + 0.5 * dt * k2_omega1,
        theta2 + 0.5 * dt * k2_omega2,
        omega1 + 0.5 * dt * k2_domega1,
        omega2 + 0.5 * dt * k2_domega2,
    )

    k4_omega1, k4_domega1, k4_omega2, k4_domega2 = derivatives(
        theta1 + dt * k3_omega1,
        theta2 + dt * k3_omega2,
        omega1 + dt * k3_domega1,
        omega2 + dt * k3_domega2,
    )

    theta1_new = theta1 + (dt / 6.0) * (k1_omega1 + 2*k2_omega1 + 2*k3_omega1 + k4_omega1)
    theta2_new = theta2 + (dt / 6.0) * (k1_omega2 + 2*k2_omega2 + 2*k3_omega2 + k4_omega2)
    omega1_new = omega1 + (dt / 6.0) * (k1_domega1 + 2*k2_domega1 + 2*k3_domega1 + k4_domega1)
    omega2_new = omega2 + (dt / 6.0) * (k1_domega2 + 2*k2_domega2 + 2*k3_domega2 + k4_domega2)

    return theta1_new, theta2_new, omega1_new, omega2_new 

class OptimizedPendulumMatrix:
    def __init__(self, N, M, theta1, theta2, omega1, omega2):
        self.N = N 
        self.M = M 
        # shape = (N, M) for theta1, theta2, omega1, omega2 
        self.theta1 = theta1
        self.theta2 = theta2
        self.omega1 = omega1
        self.omega2 = omega2

    def step(self, dt):
        self.theta1, self.theta2, self.omega1, self.omega2 = rk4_step(
            self.theta1, self.theta2, self.omega1, self.omega2, dt
        )

def optimized_different_angles(N, M):
    angles1 = np.linspace(-np.pi, np.pi, N)
    angles2 = np.linspace(-np.pi, np.pi, M)
    theta1, theta2 = np.meshgrid(angles1, angles2)
    omega1 = np.zeros((N, M))
    omega2 = np.zeros((N, M))
    return OptimizedPendulumMatrix(N, M, theta1, theta2, omega1, omega2)

def optimized_different_speeds(N, M):
    speeds1 = np.linspace(-6, 6, N)
    speeds2 = np.linspace(-6, 6, N)
    omega1, omega2 = np.meshgrid(speeds1, speeds2)
    theta1 = np.zeros((N, M))
    theta2 = np.zeros((N, M))
    return OptimizedPendulumMatrix(N, M, theta1, theta2, omega1, omega2)
