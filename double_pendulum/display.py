import tkinter as tk
import ttkbootstrap as ttk
import numpy as np
from collections import deque
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from pendulum import Pendulum, SimplePendulum, DoublePendulum
from constants import *
from presets import PRESETS

class PendulumApplication():
    
    # =================================================================================
    # 1. INITIALISATION AND SETUP
    # =================================================================================
    
    def __init__(self, root):
        self.root = root
        self.root.title("Double Pendulum Simulation")
        
        self.initial_width = CANVAS_WIDTH_PX
        self.initial_height = CANVAS_HEIGHT_PX
        self.root.geometry(f"{self.initial_width}x{self.initial_height}")
        self.view_range_meters = 4.0

        self.current_pivot_x = 0
        self.current_pivot_y = 0
        self.current_pixels_per_meter = PIXELS_PER_METER
        
        self.animation_dt_ms = ANIMATION_DT
        self.physics_dt =  PHYSICS_DT
        
        self.steps_per_frame = int(self.animation_dt_ms / (self.physics_dt * 1000))
        if self.steps_per_frame < 1:
            self.steps_per_frame = 1 # Sécurité
            
        style = ttk.Style.get_instance()
        self.theme_bg = style.colors.get('bg')
        self.theme_fg = style.colors.get('fg')
        
        self.default_theta1 = 180.0
        self.default_theta2 = 180.01
        self.default_omega1 = 0.0
        self.default_omega2 = 0.0
        
        self.sim = DoublePendulum(l1=1.0, m1=1.0, l2=1.0, m2=1.0,
                                  theta1_deg=self.default_theta1, theta2_deg=self.default_theta2,
                                  omega1=self.default_omega1, omega2=self.default_omega2)
        
        self.var_theta1 = tk.StringVar(value=str(self.default_theta1))
        self.var_omega1 = tk.StringVar(value=str(self.default_omega1))
        self.var_theta2 = tk.StringVar(value=str(self.default_theta2))
        self.var_omega2 = tk.StringVar(value=str(self.default_omega2))
        
        self.color_idx = 0
        self.current_color = COLOR_PALETTE[0][0]
        self.current_outline = COLOR_PALETTE[0][1]
        
        self.trace_data = []
        self.stored_traces = []
        self.phase_lines = []
        self.stored_phases = []
        self.energy_lines = []
        self.stored_energies = []
        self.max_trace_length = MAX_HISTORY_POINTS        
        self.show_trace_var = tk.BooleanVar(value=True)
        self.limit_trace_var = tk.BooleanVar(value=False)
        self.clear_on_reset_var = tk.BooleanVar(value=True)
        
        self.create_widgets()
        self.is_running = True
        self.update_loop()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column: Animation
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.canvas = tk.Canvas(canvas_frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.configure(bg=SIM_BG_COLOR, highlightthickness=2, highlightbackground=SIM_BORDER_COLOR)
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.pivot_id = self.canvas.create_oval(0, 0, 0, 0, fill= 
                                SIM_PIVOT_COLOR, outline="")
        
        # Middle column: Plots
        graphs_frame = ttk.Frame(main_frame)
        graphs_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 5))
        self.fig = Figure(figsize=(5, 8), dpi=100, facecolor=self.theme_bg)
        
        # Phase Diagram
        self.ax_phase = self.fig.add_subplot(211)
        self.ax_phase.set_facecolor(WHITE)
        self.ax_phase.set_title("Phase Space (θ₂ vs ω₂)", color=self.theme_fg, fontsize=10)
        self.ax_phase.set_xlabel("θ₂ (deg)", color=self.theme_fg, fontsize=8)
        self.ax_phase.set_ylabel("ω₂ (rad/s)", color=self.theme_fg, fontsize=8)
        self.ax_phase.tick_params(colors=self.theme_fg, labelsize=8)
        self.ax_phase.grid(True, color=self.theme_fg, linestyle='--', alpha=0.5)
        self.ax_phase.axhline(0, color=self.theme_fg, linewidth=1.5, alpha=0.5)
        self.ax_phase.axvline(0, color=self.theme_fg, linewidth=1.5, alpha=0.5)
        for spine in self.ax_phase.spines.values(): spine.set_edgecolor(self.theme_fg)
        self.line_phase, = self.ax_phase.plot([], [], color=TRACE_COLOR, lw=1)
        self.ax_phase.set_xlim(-180, 180)
        
        # Energy Plot
        self.ax_energy = self.fig.add_subplot(212)
        self.ax_energy.set_facecolor(WHITE)
        self.ax_energy.set_title("Total Energy vs Time", color=self.theme_fg, fontsize=10)
        self.ax_energy.set_xlabel("Time (s)", color=self.theme_fg, fontsize=8)
        self.ax_energy.set_ylabel("Total Energy (J)", color=self.theme_fg, fontsize=8)
        self.ax_energy.tick_params(colors=self.theme_fg, labelsize=8)
        self.ax_energy.grid(True, color=self.theme_fg, linestyle='--', alpha=0.5)
        self.ax_energy.axhline(0, color=self.theme_fg, linewidth=1.5, alpha=0.5)
        self.ax_energy.axvline(0, color=self.theme_fg, linewidth=1.5, alpha=0.5)
        for spine in self.ax_energy.spines.values(): spine.set_edgecolor(self.theme_fg)
        self.line_energy, = self.ax_energy.plot([], [], color=TRACE_COLOR_FADE, lw=1.5)
        self.add_new_graph_line()
        
        self.fig.tight_layout(pad=2.0)
        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=graphs_frame)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Right column: Controls
        controls_frame = ttk.Labelframe(main_frame, text="Physical Parameters", padding=10)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))

        # Pause/Reset buttons
        btn_group = ttk.Labelframe(controls_frame, text="Controls", padding=10)
        btn_group.pack(fill='x', pady=(0, 10))
        
        self.energy_label = ttk.Label(btn_group, text="Energy: 0.00 J", font=("", 10, "bold"))
        self.energy_label.pack(fill='x', pady=(0, 10))
        
        row_btns = ttk.Frame(btn_group)
        row_btns.pack(fill='x')
        self.pause_button = ttk.Button(row_btns, text="Pause", bootstyle="warning", command=self.toggle_pause)
        self.pause_button.pack(side=tk.LEFT, fill='x', expand=True, padx=(0, 2))
        self.reset_button = ttk.Button(row_btns, text="Reset", bootstyle="danger", command=self.reset_simulation)
        self.reset_button.pack(side=tk.RIGHT, fill='x', expand=True, padx=(2, 0))
        
        # Trace options buttons
        trace_frame = ttk.Frame(btn_group)
        trace_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Checkbutton(trace_frame, text="Display Trace", variable=self.show_trace_var, bootstyle="round-toggle").pack(anchor='w')
        ttk.Checkbutton(trace_frame, text="Limit Trace", variable=self.limit_trace_var, bootstyle="round-toggle").pack(anchor='w')
        ttk.Checkbutton(trace_frame, text="Delete Trace on Reset", variable=self.clear_on_reset_var, bootstyle="round-toggle").pack(anchor='w')
        
        # Adding preset buttons
        presets_frame = ttk.Labelframe(controls_frame, text="Scenarios", padding=10)
        presets_frame.pack(fill='x', pady=(0, 10))
        
        preset_names = [p["name"] for p in PRESETS]
        self.preset_combo = ttk.Combobox(presets_frame, values=preset_names, state="readonly")
        if preset_names:
            self.preset_combo.current(0)
        self.preset_combo.pack(fill='x', pady=(0, 5))
        self.preset_combo.bind("<<ComboboxSelected>>", self.on_preset_combo_change)
        self.lbl_desc = ttk.Label(presets_frame, text="...", wraplength=200, font=("", 9, "italic"))
        self.lbl_desc.pack(fill='x', pady=(0, 10))
        self.btn_apply = ttk.Button(presets_frame, text="Apply Preset", bootstyle="outline-primary", command=self.apply_selected_preset)
        self.btn_apply.pack(fill='x', pady=(0, 5))
        
        # Initial conditions frame
        ci_frame = ttk.Labelframe(controls_frame, text="Initial Conditions", padding=10)
        ci_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(ci_frame, text="θ₁ (deg)", font=("", 8)).grid(row=0, column=0, padx=5)
        ttk.Label(ci_frame, text="ω₁ (rad/s)", font=("", 8)).grid(row=0, column=1, padx=5)
        entry_t1 = ttk.Entry(ci_frame, textvariable=self.var_theta1, width=8)
        entry_t1.grid(row=1, column=0, padx=5, pady=(0, 10))
        entry_w1 = ttk.Entry(ci_frame, textvariable=self.var_omega1, width=8)
        entry_w1.grid(row=1, column=1, padx=5, pady=(0, 10))
        
        ttk.Label(ci_frame, text="θ₂ (deg)", font=("", 8)).grid(row=2, column=0, padx=5)
        ttk.Label(ci_frame, text="ω₂ (rad/s)", font=("", 8)).grid(row=2, column=1, padx=5)
        entry_t2 = ttk.Entry(ci_frame, textvariable=self.var_theta2, width=8)
        entry_t2.grid(row=3, column=0, padx=5, pady=(0, 10))
        entry_w2 = ttk.Entry(ci_frame, textvariable=self.var_omega2, width=8)
        entry_w2.grid(row=3, column=1, padx=5, pady=(0, 10))
         
        # Draw controls frame sliders
        slider_frame = ttk.Labelframe(controls_frame, text="Physical Parameters", padding=10)
        slider_frame.pack(fill='x', pady=5)
        
        # Gravity slider
        g_frame = ttk.Frame(slider_frame)
        self.g_label = ttk.Label(g_frame, text=f"Gravity g (m/s²): {self.sim.g:.2f}")
        self.g_label.pack(side=tk.LEFT)
        self.g_slider = ttk.Scale(g_frame, from_=1.0, to=20.0, orient=tk.HORIZONTAL, 
                                  command=self._on_g_slide)
        self.g_slider.set(self.sim.g)
        self.g_slider.pack(side=tk.RIGHT, fill='x', expand=True, padx=(10,0))
        g_frame.pack(fill='x', pady=5)
        
        # Damping slider
        gamma_frame = ttk.Frame(slider_frame)
        self.gamma_label = ttk.Label(gamma_frame, text=f"Damping: {self.sim.gamma:.2f} s⁻¹")
        self.gamma_label.pack(side=tk.LEFT)
        self.gamma_slider = ttk.Scale(gamma_frame, from_=0.0, to=1.0, 
                                      orient=tk.HORIZONTAL, 
                                      command=self._on_gamma_slide) 
        self.gamma_slider.set(self.sim.gamma)
        self.gamma_slider.pack(side=tk.RIGHT, fill='x', expand=True, padx=(10,0))
        gamma_frame.pack(fill='x', pady=5)
        
        # Pendulum 1 controls
        ttk.Label(slider_frame, text="Pendulum 1 (Red)",
                  font="TkDefaultFont 9 bold").pack(pady=(10,0))
        
        # l1 slider
        l1_frame = ttk.Frame(slider_frame)
        self.l1_label = ttk.Label(l1_frame, text=f"l₁ (m): {self.sim.l1:.2f}")
        self.l1_label.pack(side=tk.LEFT)
        self.l1_slider = ttk.Scale(l1_frame, from_=0.1, to=5.0, orient=tk.HORIZONTAL, 
                                   command=self._on_l1_slide) 
        self.l1_slider.set(self.sim.l1) 
        self.l1_slider.pack(side=tk.RIGHT, fill='x', expand=True, padx=(10,0))
        l1_frame.pack(fill='x', pady=5)
        
        # m1 slider
        m1_frame = ttk.Frame(slider_frame)
        self.m1_label = ttk.Label(m1_frame, text=f"m₁ (kg): {self.sim.m1:.2f}")
        self.m1_label.pack(side=tk.LEFT)
        self.m1_slider = ttk.Scale(m1_frame, from_=0.1, to=5.0, orient=tk.HORIZONTAL, 
                                   command=self._on_m1_slide) 
        self.m1_slider.set(self.sim.m1) 
        self.m1_slider.pack(side=tk.RIGHT, fill='x', expand=True, padx=(10,0))
        m1_frame.pack(fill='x', pady=5)
        
        # Pendulum 2 controls
        ttk.Label(slider_frame, text="Pendulum 2 (Blue)",
                  font="TkDefaultFont 9 bold").pack(pady=(10,0))

        # l2 slider
        l2_frame = ttk.Frame(slider_frame)
        self.l2_label = ttk.Label(l2_frame, text=f"l₂ (m): {self.sim.l2:.2f}")
        self.l2_label.pack(side=tk.LEFT)
        self.l2_slider = ttk.Scale(l2_frame, from_=0.1, to=5.0, orient=tk.HORIZONTAL, 
                                   command=self._on_l2_slide) 
        self.l2_slider.set(self.sim.l2) 
        self.l2_slider.pack(side=tk.RIGHT, fill='x', expand=True, padx=(10,0))
        l2_frame.pack(fill='x', pady=5)
        
        # m2 slider
        m2_frame = ttk.Frame(slider_frame)
        self.m2_label = ttk.Label(m2_frame, text=f"m₂ (kg): {self.sim.m2:.2f}")
        self.m2_label.pack(side=tk.LEFT)
        self.m2_slider = ttk.Scale(m2_frame, from_=0.1, to=5.0, orient=tk.HORIZONTAL, 
                                   command=self._on_m2_slide) 
        self.m2_slider.set(self.sim.m2) 
        self.m2_slider.pack(side=tk.RIGHT, fill='x', expand=True, padx=(10,0))
        m2_frame.pack(fill='x', pady=5)
        
        self.on_preset_combo_change(None)  # Initial update of preset description
        
    # =================================================================================    
    # 2. UPDATE THE LOOP
    # =================================================================================
    
    def update_loop(self):
        if not self.is_running:
            return

        for _ in range(self.steps_per_frame):
            self.sim.step(self.physics_dt)

        # Acquiring data
        _, (x2, y2) = self.sim.get_cartesian_coords()
        theta2_rad, omega2 = self.sim.Y[2:4]
        theta2_deg = self.normalize_angle(theta2_rad)
        current_energy = self.sim.get_energy()
        time = self.sim.time_elapsed
        
        # Data storage
        self.trace_data.append((x2, y2))
        
        if self.stored_phases:
            if self.stored_phases[-1]:
                prev_theta = self.stored_phases[-1][-1][0]
                if abs(theta2_deg - prev_theta) > 300:
                    self.stored_phases[-1].append((np.nan, np.nan))
            self.stored_phases[-1].append((theta2_deg, omega2))
        
        if self.stored_energies:
            self.stored_energies[-1].append((time, current_energy))
        
        if self.limit_trace_var.get():
            if len(self.trace_data) > self.max_trace_length:
                self.trace_data.pop(0)
                
            if self.stored_phases and len(self.stored_phases[-1]) > self.max_trace_length:
                self.stored_phases[-1].pop(0)
                
            if self.stored_energies and len(self.stored_energies[-1]) > self.max_trace_length:
                self.stored_energies[-1].pop(0)
        
        # Visual updates
        if self.phase_lines and self.stored_phases:
            data = np.array(self.stored_phases[-1])
            if len(data) > 0:
                self.phase_lines[-1].set_data(data[:,0], data[:,1])
                
        if self.energy_lines and self.stored_energies:
            data_e = np.array(self.stored_energies[-1])
            if len(data_e) > 0:
                self.energy_lines[-1].set_data(data_e[:,0], data_e[:,1])
        
        self.ax_phase.relim()
        self.ax_phase.autoscale_view()
        self.ax_energy.relim()
        self.ax_energy.autoscale_view()
        self.graph_canvas.draw_idle()
        self.draw_frame()
        
        self.energy_label.config(text=f"Total Energy: {current_energy:.2f} J")
        self.root.after(self.animation_dt_ms, self.update_loop)
    
    def draw_frame(self):
        self.canvas.delete("moving_item")

        # Draw Traces
        if self.show_trace_var.get():
            for trace in self.stored_traces:
                if len(trace['points']) > 1:
                    pts = []
                    for px, py in trace['points']:
                        cx, cy = self.physics_to_canvas(px, py)
                        pts.extend([cx, cy])
                    self.canvas.create_line(*pts, fill=trace['color'], width=1, tags="moving_item")

            # Draw Current Trace
            if len(self.trace_data) > 1:
                pixel_points = []
                for px, py in self.trace_data:
                    cx, cy = self.physics_to_canvas(px, py)
                    pixel_points.extend([cx, cy])
                self.canvas.create_line(*pixel_points, fill=self.current_color, width=2, tags="moving_item")
        
        # Draw pendulum
        (x1, y1), (x2, y2) = self.sim.get_cartesian_coords()
        (x1_pix, y1_pix) = self.physics_to_canvas(x1, y1)
        (x2_pix, y2_pix) = self.physics_to_canvas(x2, y2)
        
        self.canvas.create_line(self.current_pivot_x, self.current_pivot_y, x1_pix, y1_pix, 
                                fill=SIM_LINE_COLOR, width=LINE_WIDTH, tags="moving_item")
        self.canvas.create_oval(x1_pix - MASS_RADIUS, y1_pix - MASS_RADIUS,
                                x1_pix + MASS_RADIUS, y1_pix + MASS_RADIUS,
                                fill=MASS1_FILL, outline=MASS1_OUTLINE, width=2, tags="moving_item")
        
        self.canvas.create_line(x1_pix, y1_pix, x2_pix, y2_pix, 
                                fill=SIM_LINE_COLOR, width=LINE_WIDTH, tags="moving_item")
        self.canvas.create_oval(x2_pix - MASS_RADIUS, y2_pix - MASS_RADIUS,
                                x2_pix + MASS_RADIUS, y2_pix + MASS_RADIUS,
                                fill=self.current_color, outline=self.current_outline, width=2, tags="moving_item")

    # =================================================================================
    # 3. CONTROL LOGIC
    # =================================================================================
    
    def reset_simulation(self):
        t1 = float(self.var_theta1.get())
        w1 = float(self.var_omega1.get())
        t2 = float(self.var_theta2.get())
        w2 = float(self.var_omega2.get())
            
        Y0 = np.array([np.deg2rad(t1), w1, np.deg2rad(t2), w2])
        self.sim.set_initial_conditions(Y0)
        
        self.sim.reset()
        
        if self.clear_on_reset_var.get():
            self.trace_data = []
            self.stored_traces = []
            self.color_idx = 0
            for line in self.phase_lines: line.remove()
            self.phase_lines = []
            for line in self.energy_lines: line.remove()
            self.energy_lines = []
            self.current_color = COLOR_PALETTE[0][0]
            self.current_outline = COLOR_PALETTE[0][1]
            self.add_new_graph_line()

            
        else:
            if self.trace_data:
                self.stored_traces.append({'points': list(self.trace_data), 'color': self.current_color})
            self.trace_data = []
            self.color_idx  =(self.color_idx + 1) % len(COLOR_PALETTE)
            self.current_color = COLOR_PALETTE[self.color_idx][0]
            self.current_outline = COLOR_PALETTE[self.color_idx][1]
            self.add_new_graph_line()
            
        self.draw_frame()

        current_energy = self.sim.get_energy()
        self.energy_label.config(text=f"Total Energy: {current_energy:.2f} J")

        if not self.is_running:
            self.is_running = True
            self.pause_button.config(text="Pause", bootstyle="warning")
            self.update_loop()

    def toggle_pause(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.pause_button.config(text="Pause", bootstyle="warning")
            self.update_loop()
        else:
            self.pause_button.config(text="Resume", bootstyle="success")
    
    def apply_preset(self,t1,w1,t2,w2,l1,m1,l2,m2,g,gamma):
        self.var_theta1.set(str(t1))
        self.var_omega1.set(str(w1))
        self.var_theta2.set(str(t2))
        self.var_omega2.set(str(w2))
        self.sim.set_l1(l1)
        self.l1_slider.set(l1)
        self.sim.set_m1(m1)
        self.m1_slider.set(m1)
        self.sim.set_l2(l2)
        self.l2_slider.set(l2)
        self.sim.set_m2(m2)
        self.m2_slider.set(m2)
        self.sim.set_gravity(g)
        self.g_slider.set(g)
        self.sim.set_gamma(gamma)
        self.gamma_slider.set(gamma)
        self.reset_simulation()
    
    def apply_selected_preset(self):
        selected_preset = self.preset_combo.get()
        target_preset = next((p for p in PRESETS if p["name"] == selected_preset), None)
        if target_preset:
            self.apply_preset(**target_preset["params"])
    
    def add_new_graph_line(self):
        self.stored_phases.append([])
        self.stored_energies.append([])
        phase_line, = self.ax_phase.plot([], [], color=self.current_color, lw=1)
        self.phase_lines.append(phase_line)
        energy_line, = self.ax_energy.plot([], [], color=self.current_outline, lw=1.5)
        self.energy_lines.append(energy_line)

    # =================================================================================
    # 4.EVENT HELDERS (CALLBACKS)
    # =================================================================================

    def _on_g_slide(self, value):
        self.sim.set_gravity(float(value))
        self.g_label.config(text=f"g : {self.sim.g:.2f} m⋅s⁻²")

    def _on_gamma_slide(self, value):
        self.sim.set_gamma(float(value))
        self.gamma_label.config(text=f"γ : {self.sim.gamma:.2f} s⁻¹")

    def _on_l1_slide(self, value):
        self.sim.set_l1(float(value))
        self.l1_label.config(text=f"l₁ : {self.sim.l1:.2f} m")
 
    def _on_m1_slide(self, value):
        self.sim.set_m1(float(value))
        self.m1_label.config(text=f"m₁ : {self.sim.m1:.2f} kg")

    def _on_l2_slide(self, value):
        self.sim.set_l2(float(value))
        self.l2_label.config(text=f"l₂ : {self.sim.l2:.2f} m")

    def _on_m2_slide(self, value):
        self.sim.set_m2(float(value))
        self.m2_label.config(text=f"m₂ : {self.sim.m2:.2f} kg")

    def on_preset_combo_change(self, event):
        selected_name = self.preset_combo.get()
        target_preset = next((p for p in PRESETS if p["name"] == selected_name), None)
        if target_preset:
            new_style = target_preset.get("style", "outline-primary")
            self.btn_apply.config(bootstyle=new_style)
            self.lbl_desc.config(text=target_preset.get("description", ""))
  
    def on_canvas_resize(self, event):
        self.current_canvas_width = event.width
        self.current_canvas_height = event.height
        self.current_pivot_x = self.current_canvas_width / 2
        self.current_pivot_y = self.current_canvas_height / 2
        
        min_dimension_px = min(self.current_canvas_width, self.current_canvas_height)
        padding_factor = 0.85
        self.current_pixels_per_meter = (min_dimension_px * padding_factor) / self.view_range_meters
        
        self.canvas.coords(self.pivot_id, 
                           self.current_pivot_x - PIVOT_RADIUS, self.current_pivot_y - PIVOT_RADIUS,
                           self.current_pivot_x + PIVOT_RADIUS, self.current_pivot_y + PIVOT_RADIUS)
        if not self.is_running: self.draw_frame()
    
    # =================================================================================
    # 5. HELPERS
    # =================================================================================
    
    def physics_to_canvas(self, x, y):
        x_pix = self.current_pivot_x + x * self.current_pixels_per_meter
        y_pix = self.current_pivot_y - y * self.current_pixels_per_meter
        return (x_pix, y_pix)

    def normalize_angle(self, theta_rad):
        deg = np.rad2deg(theta_rad)
        return ((deg + 180) % 360) - 180
    
def start_application():
    root = ttk.Window(themename="flatly") 
    app = PendulumApplication(root)
    root.mainloop()