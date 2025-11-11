# 🛩️ UAV Strategic Deconfliction in Shared Airspace

The **UAV Strategic Deconfliction System** is an intelligent tool designed to detect potential conflicts in UAV (Unmanned Aerial Vehicle) flight paths based on **spatial** and **temporal** parameters.  
It enables users to load flight data, configure detection thresholds, visualize trajectories, and analyze conflicts using **AI-assisted development** and 3D/4D simulations.

---

## 🧭 Project Overview

This system ensures **safe UAV mission execution** by verifying that planned flight paths do not intersect in both **space** and **time** with other UAVs operating in shared airspace.  
It provides both **automated analysis** and **interactive visualization** for understanding UAV trajectory interactions and conflict patterns.

The tool supports:
- Loading UAV flight data (CSV/JSON)
- Performing automated **spatial-temporal conflict detection**
- Customizable detection thresholds
- Generating conflict summaries and 3D/4D visualizations
- AI-assisted design and optimization of the codebase

---

## ✨ Features

### 📂 Load UAV Flight Paths
- Import **primary UAV waypoints** from CSV.  
- Import **simulated UAV missions** from JSON.

### ⚠️ Conflict Detection
- Detect **spatial conflicts** (proximity in meters).  
- Detect **temporal conflicts** (time overlap in seconds).  
- Combine both for complete **4D deconfliction**.

### ⚙️ Threshold Configuration
- Adjustable **Spatial Threshold (m)** and **Temporal Threshold (s)**.  
- Default: 5 meters and 5 seconds.

### 📊 Visualizations
- **Flight Plan Visualization**
- **Spatial Conflict Visualization**
- **Spatial-Temporal Conflict Visualization**
- **Flight Animation**

### 🧾 Conflict Summary
- Detailed conflict summary in an interactive, scrollable text panel.
- Includes UAV pair, conflict type, time window, and distance metrics.

---

## 🧱 Prerequisites

Before running the application, ensure you have:

- **Python 3.x**  
- **Tkinter** (bundled with Python)  
- Required dependencies listed in `requirements.txt`

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/DipankarBagade/UAV_Assignment.git
cd UAV_Assignment
2️⃣ Create and Activate a Virtual Environment
bash
Copy code
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
▶️ Usage
🖥️ Run the Application
bash
Copy code
python .\src\main.py
This launches the UAV Deconfliction GUI.

🗂️ Load Flight Path Data
Import CSV → Load your UAV flight waypoints.

Import JSON → Load simulated UAV trajectories or mission data.

Example files are included in the /data directory.

⚙️ Set Conflict Detection Thresholds
Enter:

Spatial Threshold (m) → Minimum safe distance between UAVs.

Temporal Threshold (s) → Minimum time separation for safe crossing.

Default values: 5 and 5.

🚦 Detect Conflicts
Click "Check Conflict" to analyze all flight paths.

Performs spatial + temporal overlap detection

Displays results in the Conflict Summary window

Conflicting UAVs are visualized in red

🧭 Visualize Flight Data
Once detection completes, you can:

Option	Description
Show Flight Plan	Display UAV flight paths
Show Spatial Conflicts	Highlight spatial proximity violations
Show Spatial-Temporal Conflicts	Visualize 4D overlaps
Show Flight Animation	Animate UAV trajectories in 3D

📜 Conflict Summary
The Conflict Summary Panel shows:

UAV pairs in conflict

Conflict type (spatial/temporal/both)

Conflict start and end time

Minimum distance during conflict

🧠 Technical Details
Language: Python 3.x

Libraries: tkinter, numpy, pandas, matplotlib, datetime

Visualization: 3D and animated plots using Matplotlib’s Axes3D

Conflict Logic: Euclidean distance + synchronized timestamp analysis

Architecture: Modular design with src/ and tests/ separation


🤖 AI Integration
This project leveraged multiple AI tools during development to accelerate productivity and improve quality:

💬 ChatGPT (OpenAI)
Used for:
System design brainstorming
Code structuring and optimization
Technical documentation and rubric alignment
Debugging and explaining algorithmic logic

⚡ Blackbox AI
Used for:
Inline code completion within VS Code
efactoring and rapid syntax corrections
Speeding up repetitive function generation

🧠 Sixth AI — AI-Powered Coding Agent
Sixth AI is an AI-powered coding agent that helps you build features faster and navigate codebases effortlessly — all within Visual Studio Code.
With Sixth AI, you get:
AI Agents & Chat Assistant: Generate, edit, and modify multiple files via interactive chat
MCP Servers: Access 1000+ verified AI-capable servers for extensions
Blazing-fast Code Completion: Real-time intelligent autocompletion
Codebase Indexing: Understand and query large codebases instantly
Inline Chat: Edit snippets directly within your editor
Terminal Generation: Create terminal commands from natural prompts
Smart Code Suggestions: Write cleaner, optimized, and maintainable code

Sixth AI accelerated the modular design, file navigation, and rapid testing workflows, improving overall productivity and consistency during project development.

🧩 Testing
Run unit tests:

bash
Copy code
pytest tests/
Test coverage includes:

No-conflict scenario

Spatial-only conflict

Temporal-only conflict

Combined 4D conflict

Invalid data handling

📈 Example Visualization
🟩 Green Paths → Safe UAV trajectories
🟥 Red Paths → Conflicting UAVs
⏱ Time Slider → Demonstrates conflict progression

🔮 Future Enhancements
AI-driven route optimization and predictive conflict avoidance

Integration with real-time telemetry APIs (FlytBase, AirSim, ROS)

Web-based live dashboard

Cloud-based scalability for 10,000+ UAVs (KD-Tree, R-Tree indexing)

Reinforcement learning for autonomous rerouting

