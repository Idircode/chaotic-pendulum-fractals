import numpy as np
import matplotlib.pyplot as plt

from optimized_pendulum_matrix import OptimizedPendulumMatrix
from constants import PHYSICS_DT


def bifurcation_diagram_optimized(omega2_min=0.0,omega2_max=25.0,n_omega2=600,T=25.0,dt=PHYSICS_DT,samples_per_branch=150,
        transient_ratio=0.85,theta_wrap=True,filename="illustrations/bifurcation_diagram_optimized.png"):
    """
    Vectorized bifurcation diagram using OptimizedPendulumMatrix.
    """

    n_steps = int(T / dt)

    transient_steps = int(n_steps * transient_ratio)

    # Sampling interval
    sample_step = ((n_steps - transient_steps) // samples_per_branch)

    omega2_init = np.linspace(omega2_min, omega2_max, n_omega2).reshape(-1,1)

    theta1 = np.zeros((n_omega2, 1))
    theta2 = np.zeros((n_omega2, 1))
    omega1 = np.zeros((n_omega2, 1))
    omega2 = omega2_init.copy()

    pend = OptimizedPendulumMatrix(N=n_omega2,M=1,theta1=theta1,theta2=theta2,omega1=omega1,omega2=omega2)
    
    # Storage for collected θ₂
    theta2_points = [[] for _ in range(n_omega2)]

    # Iterate simulation
    for step in range(n_steps):
        pend.step(dt)

        if step >= transient_steps and (step - transient_steps) % sample_step == 0:
            # Extract θ₂ vector (shape Nx1)
            theta2_vec = np.rad2deg(pend.theta2[:, 0])

            if theta_wrap:
                theta2_vec = ((theta2_vec + 180) % 360) - 180

            for i in range(n_omega2):
                theta2_points[i].append(theta2_vec[i])

    # Flatten for plotting
    all_theta = np.hstack(theta2_points)
    all_omega = np.repeat(omega2_init[:, 0], samples_per_branch)

    # Plot (all points in blue)
    plt.figure(figsize=(10, 6))
    plt.scatter(all_omega, all_theta, s=1, color="blue", alpha=0.2)

    plt.xlabel("Initial ω₂ (rad/s)")
    plt.ylabel("Sampled θ₂ (degrees)")
    plt.title("Optimized Bifurcation Diagram")

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

    return omega2_init, theta2_points


if __name__ == "__main__":
    bifurcation_diagram_optimized()
    print("Optimized bifurcation diagram saved.")
