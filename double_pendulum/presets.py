# List of pre-recorded scenarios/presets

PRESETS = [
    {
        "name": "Classic Chaos (180°)",
        "style": "outline-success", # Green/Success style
        "description": "Starts vertically upright with a tiny perturbation on θ₂. Demonstrates extreme sensitivity to initial conditions.",
        "params": {
            "t1": 180.0, "w1": 0.0, 
            "t2": 180.1, "w2": 0.0,
            "l1": 1.0, "m1": 1.0, 
            "l2": 1.0, "m2": 1.0,
            "g": 9.81, "gamma": 0.0
        }
    },
    {
        "name": "Periodic (Small Angles)",
        "style": "outline-success", # Green/Success style
        "description": "Small and regular oscillations. In this regime, the system behaves almost linearly and is stable.",
        "params": {
            "t1": 20.0, "w1": 0.0, 
            "t2": 20.0, "w2": 0.0,
            "l1": 1.0, "m1": 1.0, 
            "l2": 1.0, "m2": 1.0,
            "g": 9.81, "gamma": 0.0
        }
    },
    {
        "name": "High Energy (Rotation)",
        "style": "outline-success", # Green/Success style
        "description": "High initial velocity causing full rotations. The pendulum has enough kinetic energy to overcome gravity.",
        "params": {
            "t1": 0.0, "w1": 8.0, 
            "t2": 0.0, "w2": 8.0,
            "l1": 1.0, "m1": 1.0, 
            "l2": 1.0, "m2": 1.0,
            "g": 9.81, "gamma": 0.1 # A little damping to observe the transition to oscillation
        }
    },
    {
        "name": "Double Period (L₂=2*L₁)",
        "style": "outline-success", # Green/Success style
        "description": "The second pendulum arm is twice as long as the first. Creates interesting visual patterns.",
        "params": {
            "t1": 45.0, "w1": 0.0, 
            "t2": 45.0, "w2": 0.0,
            "l1": 1.0, "m1": 1.0, 
            "l2": 2.0, "m2": 1.0,
            "g": 9.81, "gamma": 0.0
        }
    },
     {
        "name": "Whip Effect (m₁ >> m₂)",
        "style": "outline-success", # Green/Success style
        "description": "Mass 1 is very heavy, Mass 2 is very light. The heavy mass drives the light one violently.",
        "params": {
            "t1": 90.0, "w1": 0.0, 
            "t2": 90.0, "w2": 0.0,
            "l1": 1.0, "m1": 10.0, 
            "l2": 1.0, "m2": 0.1,
            "g": 9.81, "gamma": 0.0
        }
    },
    {
        "name": "Heavy Tip (m₂ >> m₁)",
        "style": "outline-success", # Green/Success style
        "description": "Mass 2 is much heavier than Mass 1. The top arm is pulled chaotically by the heavy bottom mass.",
        "params": {
            "t1": 90.0, "w1": 0.0, 
            "t2": 90.0, "w2": 0.0,
            "l1": 1.0, "m1": 0.1, 
            "l2": 1.0, "m2": 10.0,
            "g": 9.81, "gamma": 0.0
        }
    },
     {
        "name": "Approximate Simple Pendulum",
        "style": "outline-success", # Green/Success style
        "description": "Simulates a simple pendulum by making L₁ tiny and m₁ heavy (acting as a pivot), while L₂ swings.",
        "params": {
            "t1": 0.0, "w1": 0.0, 
            "t2": 90.0, "w2": 0.0,
            "l1": 0.0001, "m1": 100.0, # Effectively a fixed pivot point
            "l2": 1.0, "m2": 0.1,
            "g": 9.81, "gamma": 0.0
        }
    },
    {
        "name": "Zero Gravity (Space)",
        "style": "outline-success", # Green/Success style
        "description": "No gravity (g=0). The system conserves angular momentum and rotates indefinitely if undamped.",
        "params": {
            "t1": 0.0, "w1": 2.0, 
            "t2": 90.0, "w2": -3.0,
            "l1": 1.0, "m1": 1.0, 
            "l2": 1.0, "m2": 1.0,
            "g": 0.0, "gamma": 0.0
        }
    },
    {
        "name": "Heavy Planet (Jupiter)",
        "style": "outline-success", # Green/Success style
        "description": "Simulation with Jupiter's gravity (g=24.79 m/s²). Oscillations are faster and forces higher.",
        "params": {
            "t1": 140.0, "w1": 0.0, 
            "t2": 140.0, "w2": 0.0,
            "l1": 0.5, "m1": 1.0, 
            "l2": 0.5, "m2": 1.0,
            "g": 24.79, "gamma": 0.0
        }
    }
]