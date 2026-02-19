import numpy as np
from math import sin, cos, pi

class Pendulum():
    def __init__(self, g, gamma, color=None):
        self.g = g
        self.gamma = gamma
        self.time_elapsed = 0.0
        self.Y = np.array([])
        self.Y0 = np.array([])
        self.color = color
    
    def step(self, dt):
        y_old = self.Y

        k1 = self.derivative(y_old)
        k2 = self.derivative(y_old + dt/2 * k1)
        k3 = self.derivative(y_old + dt/2 * k2)
        k4 = self.derivative(y_old + dt * k3)
        self.Y += (dt/6) * (k1 + 2*k2 + 2*k3 + k4)
        self.time_elapsed += dt       
    
    def reset(self):
        self.Y = self.Y0.copy()
        self.time_elapsed = 0.0
    
    def set_initial_conditions(self, Y0):
        self.Y0 = Y0 

    def set_gravity(self, g):
        self.g = float(g)
    
    def set_gamma(self, gamma):
        self.gamma = float(gamma)
        
    def derivative(self, Y):
        pass 
    
    def get_cartesian_coords(self):
        pass
    
    def get_energy(self):
        pass

class SimplePendulum(Pendulum):
    def __init__(self, l=1.0, m=1.0, g=9.81, theta_deg=120.0, omega=0.0, gamma=0.0, color=None):
        super().__init__(g,gamma,color)
        self.l = l
        self.m = m
        theta_rad = np.deg2rad(theta_deg)
        self.Y = np.array([theta_rad, omega])
        self.Y0 = self.Y.copy()
    
    def derivative(self, Y):
        theta, omega = Y
        d_theta = omega
        d_omega = - (self.g / self.l) * np.sin(theta) - self.gamma * omega
        return np.array([d_theta, d_omega])
    
    def get_cartesian_coords(self):
        theta, _ = self.Y
        x = self.l * np.sin(theta)
        y = -self.l * np.cos(theta)
        return (x,y)
    
    def get_energy(self):
        _, omega = self.Y
        Ke = 0.5 * self.m * (self.l * omega)**2
        Pe = self.m * self.g * self.get_cartesian_coords()[1]
        return Ke + Pe
    
    # Specific setters
    def set_length(self, l):
        self.l = float(l)
        
    def set_mass(self, m):
        self.m = float(m)
        
class DoublePendulum(Pendulum):
    def __init__(self, l1=1.0, m1=1.0, l2=1.0, m2=1.0, g=9.81, 
                 theta1_deg=120.0, omega1=0.0, 
                 theta2_deg=120.0, omega2=0.0,
                 gamma=0.0, color=None):
        super().__init__(g, gamma, color)
        self.l1 = l1
        self.m1 = m1
        self.l2 = l2
        self.m2 = m2
        theta1_rad = np.deg2rad(theta1_deg)
        theta2_rad = np.deg2rad(theta2_deg)
        self.Y = np.array([theta1_rad, omega1, theta2_rad, omega2])
        self.Y0 = self.Y.copy()
    
    def derivative(self, Y):
        theta1, omega1, theta2, omega2 = Y
    
        delta_theta = theta1 - theta2
        sin_delta = sin(delta_theta)
        cos_delta = cos(delta_theta)
        
        m1, m2, l1, l2, g = self.m1, self.m2, self.l1, self.l2, self.g
  
        # Calculation of d_omega1
        d_omega1_num = (m2 * g * sin(theta2) * cos_delta 
                        - m2 * sin_delta * (l1 * omega1**2 * cos_delta + l2 * omega2**2) 
                        - (m1 + m2) * g * sin(theta1))
        d_omega1 = d_omega1_num / (l1 * (m1 + m2 * sin_delta**2))
        d_omega1 -= self.gamma * omega1

        # Calculation of d_omega2
        d_omega2_num = ((m1 + m2) * (l1 * omega1**2 * sin_delta - g * sin(theta2) + g * sin(theta1) * cos_delta) 
                        + m2 * l2 * omega2**2 * sin_delta * cos_delta)
        d_omega2 = d_omega2_num / (l2 * (m1 + m2 * sin_delta**2))
        d_omega2 -= self.gamma * omega2 
    
        return np.array([omega1, d_omega1, omega2, d_omega2])
    
    def get_cartesian_coords(self):
        theta1, _, theta2, _ = self.Y
        x1 = self.l1 * np.sin(theta1)
        y1 = -self.l1 * np.cos(theta1)
        x2 = x1 + self.l2 * np.sin(theta2)
        y2 = y1 - self.l2 * np.cos(theta2)
        return (x1,y1), (x2,y2)
    
    def get_energy(self):
        theta1, omega1, theta2, omega2 = self.Y
        l1, m1, l2, m2, g = self.l1, self.m1, self.l2, self.m2, self.g
    
        # Kinetic energies
        ke_1 = 0.5 * m1 * (l1 * omega1)**2
        ke_2 = 0.5 * m2 * ((l1 * omega1)**2 + (l2 * omega2)**2 + 
                         2 * l1 * l2 * omega1 * omega2 * cos(theta1 - theta2))

        # Potential energies
        (_, y1), (_, y2) = self.get_cartesian_coords() 
        pe_1 = m1 * g * y1
        pe_2 = m2 * g * y2

        return ke_1 + ke_2 + pe_1 + pe_2
    
    # Specific setters
    def set_l1(self, l1):
        self.l1 = float(l1)
        
    def set_m1(self, m1):
        self.m1 = float(m1)
        
    def set_l2(self, l2):
        self.l2 = float(l2)
        
    def set_m2(self, m2):
        self.m2 = float(m2)
