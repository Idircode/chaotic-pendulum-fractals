# --- Simulation Constants ---
ANIMATION_DT = 30  # Screen refresh rate (ms) -> ~60 FPS
PHYSICS_DT = 0.001    # Physics timestep (s) -> 0.1 ms (for RK4 stability)
MAX_HISTORY_POINTS = 1000 # Max points for trace and phase plot

# --- Display Constants (Canvas) ---
CANVAS_WIDTH_PX = 1800
CANVAS_HEIGHT_PX = 700
PIXELS_PER_METER = 100   # Scale: 100 pixels = 1 meter

# --- Visual Styling ---
PIVOT_RADIUS = 4
MASS_RADIUS = 8
MASS_OUTLINE_WIDTH = 2
LINE_WIDTH = 3

PIVOT_COLOR = "#CCCCCC"
LINE_COLOR = "#AAAAAA"
TRACE_COLOR = "#3399FF"
TRACE_COLOR_FADE = "#66B2FF"

SIM_BG_COLOR = "#E8E8E8"
SIM_BORDER_COLOR = "#AAAAAA"
SIM_LINE_COLOR = "#555555"
SIM_PIVOT_COLOR = "#444444"


# Color palettes for superposition

COLOR_PALETTE = [
    ("#3399FF", "#66B2FF"), # Bleu (Défaut)
    ("#FF3333", "#FF6666"), # Rouge
    ("#32CD32", "#98FB98"), # Vert Lime
    ("#FFD700", "#F0E68C"), # Or
    ("#FF00FF", "#FF69B4"), # Magenta
    ("#00FFFF", "#E0FFFF"), # Cyan
    ("#FF8C00", "#FFA500")  # Orange
]

MASS1_FILL = "#555555"
MASS1_OUTLINE = "#777777"

TRACE_COLOR = COLOR_PALETTE[0][0]

# Ohter colors
GOLD = "#EDB844"
WHITE = '#E7E7E7'
PURPLE = "#BA3CEB"
DARKGRAY = "#5d5d5d"