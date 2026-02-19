from pendulum_matrix import compute_colormap, matrix_generator, DoublePendulumMatrix 
from optimized_pendulum_matrix import OptimizedPendulumMatrix, rk4_step, optimized_different_angles, optimized_different_speeds
import numpy as np
import imageio.v2 as imageio
import matplotlib.pyplot as plt

def matrix_simulation_gif(N, dt=1e-3, tau=0.1, T=10.0, filename="pendulum_matrix_simulation.gif"):
    """
    Simule l'évolution de la matrice de pendules et génère un fichier GIF 
    représentant l'évolution des couleurs.
    """
    M = N 
    num_steps = int(T / dt)
    steps_per_frame = int(tau / dt)
    matrix = matrix_generator(N, M)
    pendulum_matrix = DoublePendulumMatrix(matrix)

    frames = []

    for step in range(num_steps):
        pendulum_matrix.step(dt) 

        if step % steps_per_frame == 0:
            pendulum_matrix.update_color()
            image = pendulum_matrix.get_image()

            frames.append(image)

    # Convert to uint8 format for GIF 
    frames_uint8 = [np.clip(frame * 255, 0, 255).astype(np.uint8) for frame in frames] 

    # Save as GIF
    imageio.mimsave(filename, frames_uint8, fps=int(1 / tau)) 

def matrix_simulation_live(N, dt=1e-3, tau=0.1, T=10.0):
    M = N
    matrix = matrix_generator(N, M)
    pendulum_matrix = DoublePendulumMatrix(matrix)

    num_steps = int(T / dt)
    steps_per_frame = int(tau / dt)  # how often to refresh the display

    # --- Matplotlib setup ---
    plt.ion()  # interactive mode ON
    fig, ax = plt.subplots()
    pendulum_matrix.update_color()
    image = pendulum_matrix.get_image()          # (N, N, 4) float in [0,1]
    im = ax.imshow(image, interpolation="nearest")
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()

    for step in range(num_steps):
        pendulum_matrix.step(dt)

        if step % steps_per_frame == 0:
            pendulum_matrix.update_color()
            image = pendulum_matrix.get_image()

            # Update image data
            im.set_data(image)
            ax.set_title(f"Step {step}/{num_steps}")
            fig.canvas.draw()
            # Small pause so the GUI can update
            plt.pause(0.001)

    # Keep the window open at the end
    plt.ioff()
    plt.show()

def optimized_simulation_gif(pendulums, dt=1e-3, tau=0.1, T=10.0, filename="optimized_pendulum_matrix_simulation.gif"):
    """
    Simule l'évolution de la matrice de pendules optimisée et génère un fichier GIF 
    représentant l'évolution des couleurs.
    """
    N = pendulums.N
    M = pendulums.M
    colormap = compute_colormap(N, M)
    num_steps = int(T / dt)
    steps_per_frame = int(tau / dt)
    frames = [] 

    for step in range(num_steps):
        pendulums.step(dt) 

        if step % steps_per_frame == 0:
            # Compute colors based on angles
            theta1 = pendulums.theta1
            theta2 = pendulums.theta2
            i_indices = ((theta1 + np.pi) / (2 * np.pi) * N).astype(int) % N
            j_indices = ((theta2 + np.pi) / (2 * np.pi) * M).astype(int) % M

            image = colormap[i_indices, j_indices]

            frames.append(image)

    # Convert to uint8 format for GIF 
    frames_uint8 = [np.clip(frame * 255, 0, 255).astype(np.uint8) for frame in frames] 

    # Save as GIF
    imageio.mimsave(filename, frames_uint8, fps=int(1 / tau))

def optimized_simulation_live(pendulums, dt=1e-3, tau=0.1, T=10.0):
    N = pendulums.N
    M = pendulums.M
    colormap = compute_colormap(N, M)
    num_steps = int(T / dt)
    steps_per_frame = int(tau / dt)  # how often to refresh the display

    # --- Matplotlib setup ---
    plt.ion()  # interactive mode ON
    fig, ax = plt.subplots()
    # Initial color computation
    theta1 = pendulums.theta1
    theta2 = pendulums.theta2
    i_indices = ((theta1 + np.pi) / (2 * np.pi) * N).astype(int) % N
    j_indices = ((theta2 + np.pi) / (2 * np.pi) * M).astype(int) % M
    image = colormap[i_indices, j_indices]          # (N, N, 4) float in [0,1]
    im = ax.imshow(image)
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()

    for step in range(num_steps):
        pendulums.step(dt)

        if step % steps_per_frame == 0:
            # Compute colors based on angles
            theta1 = pendulums.theta1
            theta2 = pendulums.theta2
            i_indices = ((theta1 + np.pi) / (2 * np.pi) * N).astype(int) % N 
            j_indices = ((theta2 + np.pi) / (2 * np.pi) * M).astype(int) % M 
            image = colormap[i_indices, j_indices]

            # Update image data
            im.set_data(image)
            ax.set_title(f"Step {step}/{num_steps}")
            fig.canvas.draw()
            # Small pause so the GUI can update
            plt.pause(0.001)

    # Keep the window open at the end
    plt.ioff()
    plt.show()
