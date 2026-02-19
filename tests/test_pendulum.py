import pytest
import numpy as np
from math import isclose, pi

from double_pendulum.pendulum import SimplePendulum, DoublePendulum
from double_pendulum.pendulum_matrix import (theta_to_index, index_to_theta, compute_colormap, 
                                             matrix_generator, DoublePendulumMatrix)

# --- Simple Pendulum Tests ---

@pytest.fixture
def simple_sim():
    """Fixture to create a basic simple pendulum."""
    return SimplePendulum(l=1.0, m=1.0, g=9.81, theta_deg=135)

def test_simple_init(simple_sim):
    """Verifies correct initialization."""
    assert simple_sim.l == 1.0
    assert simple_sim.g == 9.81
    assert isclose(simple_sim.Y[0], 3*pi/4) 
    assert simple_sim.Y[1] == 0.0

def test_simple_setters(simple_sim):
    """Verifies specific setters for the simple pendulum."""
    simple_sim.set_length(2.5)
    simple_sim.set_mass(5.0)
    simple_sim.set_gravity(1.62)
    
    assert simple_sim.l == 2.5
    assert simple_sim.m == 5.0
    assert simple_sim.g == 1.62

def test_simple_energy_conservation(simple_sim):
    """
    Crucial test: Without friction, energy must be constant.
    """
    simple_sim.set_gamma(0.0)
    
    # Recalculate initial energy after reset to be sure
    simple_sim.reset()
    E_start = simple_sim.get_energy()
    
    # Advance the simulation
    dt = 0.01
    for _ in range(100):
        simple_sim.step(dt)
        
    E_end = simple_sim.get_energy()
    
    # Check that energy has not varied by more than 0.1%
    assert isclose(E_start, E_end, rel_tol=1e-3)

def test_simple_reset(simple_sim):
    """Verifies that reset properly restores the initial state."""
    # Advance
    simple_sim.step(1.0)
    assert simple_sim.time_elapsed > 0
    assert simple_sim.Y[0] != 3*pi/4
    
    # Reset
    simple_sim.reset()
    
    # Checks
    assert simple_sim.time_elapsed == 0.0
    assert isclose(simple_sim.Y[0], 3*pi/4)

# --- Double Pendulum Tests ---

@pytest.fixture
def double_sim():
    """Fixture to create a double pendulum."""
    return DoublePendulum(l1=1.0, m1=1.0, l2=1.0, m2=1.0, 
                          theta1_deg=180.0, theta2_deg=180.0)

def test_double_init(double_sim):
    assert len(double_sim.Y) == 4
    assert isclose(double_sim.Y[0], pi)
    assert isclose(double_sim.Y[2], pi)

def test_double_setters(double_sim):
    """Verifies that setters correctly modify attributes (case sensitive)."""
    double_sim.set_l1(2.5)
    double_sim.set_m2(10.0)
    double_sim.set_gravity(1.62) # Moon gravity
    
    assert double_sim.l1 == 2.5
    assert double_sim.m2 == 10.0
    assert double_sim.g == 1.62

def test_double_energy_conservation(double_sim):
    """
    RK4 stability test for the double pendulum (chaotic system).
    """
    double_sim.set_gamma(0.0)

    Y_horizontal = np.array([pi, 0, pi+0.1, 0])
    double_sim.set_initial_conditions(Y_horizontal)
    double_sim.reset()
    
    E_start = double_sim.get_energy()

    dt = 0.001 # Fine timestep for precision
    for _ in range(1000): # 1 second of physical simulation
        double_sim.step(dt)
        
    E_end = double_sim.get_energy()

    assert isclose(E_start, E_end, rel_tol=1e-3)

# --- PENDULUM MATRIX TESTS ---

def test_matrix_generator_dimension():
    mat = matrix_generator(10, 12)
    assert len(mat) == 10
    assert len(mat[0]) == 12
    assert isinstance(mat[0][0], DoublePendulum)


def test_matrix_step_updates_state():
    mat = matrix_generator(5, 5)
    sim = DoublePendulumMatrix(mat)

    before = sim.matrix[2][2].Y.copy()
    sim.step(0.01)
    after = sim.matrix[2][2].Y.copy()

    assert not np.array_equal(before, after)


def test_update_color_changes_color():
    mat = matrix_generator(6, 6)
    sim = DoublePendulumMatrix(mat)

    before = sim.matrix[3][3].color
    sim.step(0.01)
    sim.update_color()
    after = sim.matrix[3][3].color

    assert not np.array_equal(before, after)


# ============================================================
# BIFURCATION DIAGRAM LOGIC TESTS
# (light tests, do not generate full plots)
# ============================================================

def dummy_bifurcation_test():
    """Ensures angles are wrapped correctly and dataset sizes match."""
    from bifurcation_diagram import bifurcation_diagram

    omegas, points = bifurcation_diagram(
        n_omega2=20,
        T=1.0,
        samples_per_branch=10,
        filename="test.png"
    )

    assert len(omegas) == 20
    assert len(points) == 20

    # angles must be within [-180, 180]
    for branch in points:
        for th in branch:
            assert -180 <= th <= 180
