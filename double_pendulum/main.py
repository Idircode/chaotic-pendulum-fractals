import ttkbootstrap as ttk
import time 

from display import start_application
from animation import * 
from bifurcation_diagram import *

if __name__ == "__main__":
    N = 30
    M = 30 
    dt = 1e-3
    tau = 0.1 
    T = 10.0 
    pendulums = optimized_different_angles(N, M)

    optimized_simulation_live(pendulums, dt=dt, tau=tau, T=100*T)
