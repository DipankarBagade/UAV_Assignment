import deconflict, path, visualization
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import json

# Color scheme - High-tech dark theme
COLORS = {
    'bg_dark': '#1a1a1a',
    'bg_medium': '#2d2d2d',
    'bg_light': '#3d3d3d',
    'accent_cyan': '#00d4ff',
    'accent_blue': '#0099cc',
    'text_white': '#ffffff',
    'text_gray': '#cccccc',
    'success': '#00ff88',
    'warning': '#ff3366',
    'border': '#00d4ff'
}

def load_primary_csv():
    global csv_file_path
    csv_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if csv_file_path:
        filename = csv_file_path.split('/')[-1]
        label_primary_csv.config(text=f"✓ {filename}", fg=COLORS['success'])
        btn_primary_csv.config(bg=COLORS['bg_light'])

def load_sim_json():
    global json_file_path
    json_file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if json_file_path:
        filename = json_file_path.split('/')[-1]
        label_sim_json.config(text=f"✓ {filename}", fg=COLORS['success'])
        btn_sim_json.config(bg=COLORS['bg_light'])

def check_conflict():
    global paths_obj
    global deconflict_obj
    
    try:
        temporal_threshold = float(entry_temporal.get())
        spatial_threshold = float(entry_spatial.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric thresholds")
        return
    
    if csv_file_path is None or json_file_path is None:
        messagebox.showerror("Error", "Please load both Primary CSV and JSON")
        return
    
    # Update status to analyzing
    status_label.config(text="⚡ ANALYZING...", fg=COLORS['accent_cyan'])
    root.update()
    
    paths_obj = path.Paths(primary_path_csv=csv_file_path, primary_path_json=json_file_path)
    deconflict_obj = deconflict.Deconflict(paths_obj, spatial_threshold, temporal_threshold)
    
    # Apply temporal and spatial thresholds to the conflict check logic
    conflict_detected = deconflict_obj.conflict_bool
    
    if conflict_detected:
        status_label.config(text="⚠ CONFLICT DETECTED", fg=COLORS['warning'])
    else:
        status_label.config(text="✓ PATH CLEAR", fg=COLORS['success'])
    
    summary_text.delete("1.0", tk.END)
    summary_text.insert(tk.END, deconflict_obj.get_conflict_summary())
    
    # Enable visualization buttons with visual feedback
    for btn in [btn_vis_fp, btn_vis_stc, btn_vis_animation, btn_vis_sc]:
        btn.config(state=tk.NORMAL, bg=COLORS['accent_blue'], fg=COLORS['text_white'])

def visualize_fp():
    visualization.visualize_paths(paths_obj)

def visualize_stc():
    visualization.visualize_conflicts(paths_obj, deconflict_obj.spatial_temporal_conflict_results)

def visualize_animation():
    visualization.visualize_flight(paths_obj)

def visualize_sc():
    visualization.visualize_conflicts(paths_obj, deconflict_obj.spatial_conflict_results)

# Initialize global variables
csv_file_path = None
json_file_path = None

# Tkinter UI setup
root = tk.Tk()
root.title("UAV STRATEGIC DECONFLICTION SYSTEM")
root.configure(bg=COLORS['bg_dark'])
root.geometry("900x750")

# Configure grid layout
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Title Header
title_frame = tk.Frame(root, bg=COLORS['bg_dark'], pady=15)
title_frame.grid(row=0, column=0, columnspan=3, sticky="ew")

title_label = tk.Label(
    title_frame,
    text="⬢ UAV CONFLICT CHECKER ⬢",
    font=("Consolas", 20, "bold"),
    bg=COLORS['bg_dark'],
    fg=COLORS['accent_cyan']
)
title_label.pack()

subtitle_label = tk.Label(
    title_frame,
    text="Strategic Deconfliction in Shared Airspace",
    font=("Consolas", 10),
    bg=COLORS['bg_dark'],
    fg=COLORS['text_gray']
)
subtitle_label.pack()

# Separator
separator1 = tk.Frame(root, height=2, bg=COLORS['border'])
separator1.grid(row=1, column=0, columnspan=3, sticky="ew", padx=20, pady=5)

# ===== SECTION 1: FILE LOADING =====
section1_frame = tk.Frame(root, bg=COLORS['bg_medium'], relief=tk.RAISED, bd=2)
section1_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=20, pady=10)

section1_title = tk.Label(
    section1_frame,
    text="▸ FLIGHT DATA INPUT",
    font=("Consolas", 12, "bold"),
    bg=COLORS['bg_medium'],
    fg=COLORS['accent_cyan'],
    anchor="w"
)
section1_title.pack(fill=tk.X, padx=10, pady=5)

# CSV Load
csv_frame = tk.Frame(section1_frame, bg=COLORS['bg_medium'])
csv_frame.pack(fill=tk.X, padx=10, pady=5)

tk.Label(
    csv_frame,
    text="Primary Path (CSV):",
    font=("Consolas", 10),
    bg=COLORS['bg_medium'],
    fg=COLORS['text_white'],
    width=20,
    anchor="w"
).pack(side=tk.LEFT, padx=5)

btn_primary_csv = tk.Button(
    csv_frame,
    text="IMPORT CSV",
    command=load_primary_csv,
    font=("Consolas", 9, "bold"),
    bg=COLORS['bg_light'],
    fg=COLORS['accent_cyan'],
    activebackground=COLORS['accent_blue'],
    activeforeground=COLORS['text_white'],
    relief=tk.FLAT,
    bd=0,
    padx=15,
    pady=5,
    cursor="hand2"
)
btn_primary_csv.pack(side=tk.LEFT, padx=5)

label_primary_csv = tk.Label(
    csv_frame,
    text="○ No file loaded",
    font=("Consolas", 9),
    bg=COLORS['bg_medium'],
    fg=COLORS['text_gray']
)
label_primary_csv.pack(side=tk.LEFT, padx=10)

# JSON Load
json_frame = tk.Frame(section1_frame, bg=COLORS['bg_medium'])
json_frame.pack(fill=tk.X, padx=10, pady=5)

tk.Label(
    json_frame,
    text="Primary Path (JSON):",
    font=("Consolas", 10),
    bg=COLORS['bg_medium'],
    fg=COLORS['text_white'],
    width=20,
    anchor="w"
).pack(side=tk.LEFT, padx=5)

btn_sim_json = tk.Button(
    json_frame,
    text="IMPORT JSON",
    command=load_sim_json,
    font=("Consolas", 9, "bold"),
    bg=COLORS['bg_light'],
    fg=COLORS['accent_cyan'],
    activebackground=COLORS['accent_blue'],
    activeforeground=COLORS['text_white'],
    relief=tk.FLAT,
    bd=0,
    padx=15,
    pady=5,
    cursor="hand2"
)
btn_sim_json.pack(side=tk.LEFT, padx=5)

label_sim_json = tk.Label(
    json_frame,
    text="○ No file loaded",
    font=("Consolas", 9),
    bg=COLORS['bg_medium'],
    fg=COLORS['text_gray']
)
label_sim_json.pack(side=tk.LEFT, padx=10)

# ===== SECTION 2: CONFIGURATION =====
section2_frame = tk.Frame(root, bg=COLORS['bg_medium'], relief=tk.RAISED, bd=2)
section2_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=20, pady=10)

section2_title = tk.Label(
    section2_frame,
    text="▸ THRESHOLD CONFIGURATION",
    font=("Consolas", 12, "bold"),
    bg=COLORS['bg_medium'],
    fg=COLORS['accent_cyan'],
    anchor="w"
)
section2_title.pack(fill=tk.X, padx=10, pady=5)

# Temporal Threshold
temporal_frame = tk.Frame(section2_frame, bg=COLORS['bg_medium'])
temporal_frame.pack(fill=tk.X, padx=10, pady=5)

tk.Label(
    temporal_frame,
    text="Temporal Threshold (sec):",
    font=("Consolas", 10),
    bg=COLORS['bg_medium'],
    fg=COLORS['text_white'],
    width=25,
    anchor="w"
).pack(side=tk.LEFT, padx=5)

entry_temporal = tk.Entry(
    temporal_frame,
    font=("Consolas", 10),
    bg=COLORS['bg_light'],
    fg=COLORS['text_white'],
    insertbackground=COLORS['accent_cyan'],
    relief=tk.FLAT,
    bd=0,
    width=15
)
entry_temporal.insert(0, "5")
entry_temporal.pack(side=tk.LEFT, padx=5, ipady=5)

# Spatial Threshold
spatial_frame = tk.Frame(section2_frame, bg=COLORS['bg_medium'])
spatial_frame.pack(fill=tk.X, padx=10, pady=5)

tk.Label(
    spatial_frame,
    text="Spatial Threshold (m):",
    font=("Consolas", 10),
    bg=COLORS['bg_medium'],
    fg=COLORS['text_white'],
    width=25,
    anchor="w"
).pack(side=tk.LEFT, padx=5)

entry_spatial = tk.Entry(
    spatial_frame,
    font=("Consolas", 10),
    bg=COLORS['bg_light'],
    fg=COLORS['text_white'],
    insertbackground=COLORS['accent_cyan'],
    relief=tk.FLAT,
    bd=0,
    width=15
)
entry_spatial.insert(0, "5")
entry_spatial.pack(side=tk.LEFT, padx=5, ipady=5)

# ===== SECTION 3: ANALYSIS =====
section3_frame = tk.Frame(root, bg=COLORS['bg_dark'])
section3_frame.grid(row=4, column=0, columnspan=3, pady=15)

btn_check = tk.Button(
    section3_frame,
    text="⚡ RUN CONFLICT ANALYSIS ⚡",
    command=check_conflict,
    font=("Consolas", 12, "bold"),
    bg=COLORS['accent_cyan'],
    fg=COLORS['bg_dark'],
    activebackground=COLORS['accent_blue'],
    activeforeground=COLORS['text_white'],
    relief=tk.FLAT,
    bd=0,
    padx=30,
    pady=12,
    cursor="hand2"
)
btn_check.pack()

# ===== SECTION 4: STATUS =====
status_frame = tk.Frame(root, bg=COLORS['bg_medium'], relief=tk.RAISED, bd=2)
status_frame.grid(row=5, column=0, columnspan=3, sticky="ew", padx=20, pady=10)

status_label = tk.Label(
    status_frame,
    text="● AWAITING INPUT",
    font=("Consolas", 14, "bold"),
    bg=COLORS['bg_medium'],
    fg=COLORS['text_gray'],
    pady=10
)
status_label.pack()

# ===== SECTION 5: VISUALIZATIONS =====
section5_frame = tk.Frame(root, bg=COLORS['bg_medium'], relief=tk.RAISED, bd=2)
section5_frame.grid(row=6, column=0, columnspan=3, sticky="ew", padx=20, pady=10)

section5_title = tk.Label(
    section5_frame,
    text="▸ VISUALIZATION OPTIONS",
    font=("Consolas", 12, "bold"),
    bg=COLORS['bg_medium'],
    fg=COLORS['accent_cyan'],
    anchor="w"
)
section5_title.pack(fill=tk.X, padx=10, pady=5)

vis_buttons_frame = tk.Frame(section5_frame, bg=COLORS['bg_medium'])
vis_buttons_frame.pack(fill=tk.X, padx=10, pady=10)

# Create 2x2 grid for visualization buttons
btn_vis_fp = tk.Button(
    vis_buttons_frame,
    text="📊 FLIGHT PLAN",
    command=visualize_fp,
    state=tk.DISABLED,
    font=("Consolas", 9, "bold"),
    bg=COLORS['bg_light'],
    fg=COLORS['text_gray'],
    activebackground=COLORS['accent_blue'],
    activeforeground=COLORS['text_white'],
    relief=tk.FLAT,
    bd=0,
    padx=15,
    pady=8,
    cursor="hand2",
    width=25
)
btn_vis_fp.grid(row=0, column=0, padx=5, pady=5)

btn_vis_stc = tk.Button(
    vis_buttons_frame,
    text="⚠ SPATIAL-TEMPORAL",
    command=visualize_stc,
    state=tk.DISABLED,
    font=("Consolas", 9, "bold"),
    bg=COLORS['bg_light'],
    fg=COLORS['text_gray'],
    activebackground=COLORS['accent_blue'],
    activeforeground=COLORS['text_white'],
    relief=tk.FLAT,
    bd=0,
    padx=15,
    pady=8,
    cursor="hand2",
    width=25
)
btn_vis_stc.grid(row=0, column=1, padx=5, pady=5)

btn_vis_animation = tk.Button(
    vis_buttons_frame,
    text="▶ FLIGHT ANIMATION",
    command=visualize_animation,
    state=tk.DISABLED,
    font=("Consolas", 9, "bold"),
    bg=COLORS['bg_light'],
    fg=COLORS['text_gray'],
    activebackground=COLORS['accent_blue'],
    activeforeground=COLORS['text_white'],
    relief=tk.FLAT,
    bd=0,
    padx=15,
    pady=8,
    cursor="hand2",
    width=25
)
btn_vis_animation.grid(row=1, column=0, padx=5, pady=5)

btn_vis_sc = tk.Button(
    vis_buttons_frame,
    text="📍 SPATIAL CONFLICTS",
    command=visualize_sc,
    state=tk.DISABLED,
    font=("Consolas", 9, "bold"),
    bg=COLORS['bg_light'],
    fg=COLORS['text_gray'],
    activebackground=COLORS['accent_blue'],
    activeforeground=COLORS['text_white'],
    relief=tk.FLAT,
    bd=0,
    padx=15,
    pady=8,
    cursor="hand2",
    width=25
)
btn_vis_sc.grid(row=1, column=1, padx=5, pady=5)

# ===== SECTION 6: CONFLICT SUMMARY =====
section6_frame = tk.Frame(root, bg=COLORS['bg_medium'], relief=tk.RAISED, bd=2)
section6_frame.grid(row=7, column=0, columnspan=3, sticky="ew", padx=20, pady=10)

section6_title = tk.Label(
    section6_frame,
    text="▸ CONFLICT SUMMARY",
    font=("Consolas", 12, "bold"),
    bg=COLORS['bg_medium'],
    fg=COLORS['accent_cyan'],
    anchor="w"
)
section6_title.pack(fill=tk.X, padx=10, pady=5)

# Frame for summary text and scrollbar
summary_frame = tk.Frame(section6_frame, bg=COLORS['bg_medium'])
summary_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Scrollbar widget
scrollbar = tk.Scrollbar(summary_frame, bg=COLORS['bg_light'])
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Text widget for conflict summary
summary_text = tk.Text(
    summary_frame,
    height=8,
    font=("Consolas", 9),
    bg=COLORS['bg_light'],
    fg=COLORS['text_white'],
    insertbackground=COLORS['accent_cyan'],
    relief=tk.FLAT,
    bd=0,
    yscrollcommand=scrollbar.set,
    wrap=tk.WORD
)
summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Link scrollbar with text widget
scrollbar.config(command=summary_text.yview)

# Footer
footer_label = tk.Label(
    root,
    text="═══════════════════════════════════════════════════════",
    font=("Consolas", 8),
    bg=COLORS['bg_dark'],
    fg=COLORS['border']
)
footer_label.grid(row=8, column=0, columnspan=3, pady=5)

root.mainloop()
