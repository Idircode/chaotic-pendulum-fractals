# Study of the Chaotic Behavior of the Double Pendulum 
**CodingWeeks 2025–2026 — Theme: Physical Simulations**  

---

## Project Objective
This project aims to:  
- Study and visualize the dynamic behavior of the double pendulum.  
- Observe non-linear and chaotic phenomena.  
- Modify physical parameters in real time (length, mass, gravity, damping, initial angles, initial speed).   

---

## Main Features

### Double Pendulum Simulation
- Realistic simulation of chaotic dynamics.  
- Variation of several parameters in real time.   
- Phase diagram and energy vs time plot computation in real time.  
- Possibility to run an experiment with the trace of the previous ones behind.
- Choice among several interesting presets or a personalized one.
- Start, Pause, Reset buttons with several options on reset.

### Visualisation of the chaotic behaviour

- **Color matrices (chaos maps)**  
  - Grid-based representation of how pairs of initial angles `(θ₁, θ₂)` evolve over time.  
  - Each pendulum in the matrix is simulated independently; its final state determines the color in the grid.  
  - Useful to visually detect sensitive regions where small changes in initial angles produce diverging trajectories — a hallmark of chaotic systems.  
  - Helps compare stable basins, transition zones, and fully chaotic regions.
- **Bifurcation diagrams**  
  - Numerical exploration of how small variations in the initial angular velocity of the second pendulum (`ω₂`) lead to drastically different long-term behaviours.  
  - Allows the identification of transition zones between periodic, quasi-periodic, and chaotic regimes.  
  - Optimized version implemented using a vectorized `OptimizedPendulumMatrix`, reducing computation time significantly.
---

## Clone the Project

```bash
git clone git@gitlab-research.centralesupelec.fr:hugo.charles/rk4.git
cd rk4
```

---

## Project Structure
```
rk4/                       
├── double_pendulum/              # Main source code package
│   ├── __pycache__/              # Python cache (ignored)
│   ├── animations/               # Saved animations (if any)
│   ├── illustrations/            # Images used in the README/presentation
│   ├── __init__.py               # Package initializer
│   ├── animation.py              # Generates animations from a pendulum matrix
│   ├── bifurcation_diagram.py    # Bifurcation diagram generation (classic & optimized)
│   ├── constants.py              # Global constants (timestep, colors, display scale…)
│   ├── display.py                # Real-time graphical interface using Tkinter
│   ├── main.py                   # Program entry point (launches the GUI)
│   ├── optimized_pendulum_matrix.py  # Vectorized/optimized pendulum matrix
│   ├── pendulum.py               # Class definitions for SimplePendulum & DoublePendulum
│   ├── pendulum_matrix.py        # Classic non-vectorized pendulum matrix
│   └── presets.py                # Library of predefined scenarios for the simulator
│
├── tests/                        # Unit tests (pytest)
│   └── test_pendulum.py          # Tests: energy, RK4 stability, init, setters, bifurcation…
│
├── README.md                     # Project description
├── TODO.md                       # Remaining tasks / improvements
└── requirements.txt              # Python dependencies

```
--- 

## Important
Make sure to install all project dependencies before running the application:
```bash
pip install -r requirements.txt
