import math 
import numpy as np 
import colormap2d 

from pendulum import DoublePendulum 

def theta_to_index(theta, N):
    """Convertit un angle en indice de matrice."""
    index = math.floor(theta  * N / (2 * np.pi))
    return index % N 

def index_to_theta(index, N):
    """Convertit un indice de matrice en angle."""
    theta = index * 2 * np.pi / N
    return theta

def compute_colormap(N, M):
    grid = np.array([
        [[x/N, y/N] for y in range(M)] for x in range(N) 
    ])

    return colormap2d.cyclic_pinwheel(grid)

def matrix_generator(N, M, l1=1.0, m1=1.0, l2=1.0, m2=1.0, g=9.81):
    colormap = compute_colormap(N, M)
    matrix = [] 

    for i in range(N):
        matrix.append([]) 
        theta1 = index_to_theta(i, N) - np.pi 
        for j in range(M):
            theta2 = index_to_theta(j, M) - np.pi 
            color = colormap[i, j] 
            pendulum = DoublePendulum(l1=l1, m1=m1, l2=l2, m2=m2, g=g, 
                theta1_deg=np.rad2deg(theta1), omega1=0.0, 
                theta2_deg=np.rad2deg(theta2), omega2=0.0, 
                gamma=0.0, color=color) 
            matrix[i].append(pendulum) 

    return matrix

class DoublePendulumMatrix: 
    def __init__(self, matrix):
        self.N = len(matrix)      # Number of rows 
        self.M = len(matrix[0])   # Number of columns 
        self.matrix = matrix 
        self.colormap = compute_colormap(self.N, self.M) 

    def step(self, dt):
        for i in range(self.N):
            for j in range(self.M): 
                self.matrix[i][j].step(dt) 

    def update_color(self):
        for i in range(self.N):
            for j in range(self.N):
                pendulum = self.matrix[i][j]
                theta1, _, theta2, _ = pendulum.Y 
                i_new = theta_to_index(theta1, self.N)
                j_new = theta_to_index(theta2, self.M)
                pendulum.color = self.colormap[i_new, j_new]

    def get_image(self):
        colors = np.zeros((self.N, self.M, 4))
        for i in range(self.N):
            for j in range(self.M):
                colors[i, j] = self.matrix[i][j].color
        return colors 
