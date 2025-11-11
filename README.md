# UAV Strategic Deconfliction System

An intelligent conflict detection tool for UAV flight path management that analyzes spatial and temporal parameters to ensure safe mission execution in shared airspace.

## Overview

The UAV Strategic Deconfliction System helps verify that planned UAV flight paths do not intersect in both space and time. It provides automated conflict analysis with interactive 3D/4D visualizations, enabling operators to identify and resolve potential airspace conflicts before deployment.

### Key Features

- **Multi-format Data Import**: Load flight data from CSV or JSON files
- **4D Conflict Detection**: Analyze both spatial proximity and temporal overlap
- **Customizable Thresholds**: Configure detection sensitivity for different operational requirements
- **Interactive Visualizations**: View flight plans, conflicts, and animated trajectories in 3D
- **Comprehensive Reports**: Generate detailed conflict summaries with metrics and time windows

## Requirements

- Python 3.x
- Tkinter (included with Python)
- Dependencies listed in `requirements.txt`

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/DipankarBagade/UAV_Assignment.git
cd UAV_Assignment
```

2. **Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Usage

### Launch Application
```bash
python src/main.py
```

### Workflow

1. **Load Data**: Import UAV waypoints (CSV) or mission trajectories (JSON). Sample files are provided in the `/data` directory.

2. **Configure Thresholds**: 
   - Spatial Threshold: Minimum safe distance in meters (default: 5m)
   - Temporal Threshold: Minimum time separation in seconds (default: 5s)

3. **Detect Conflicts**: Click "Check Conflict" to analyze flight paths. The system performs spatial-temporal overlap detection and highlights conflicts in red.

4. **Visualize Results**: Choose from multiple visualization options:
   - Flight Plan: Display all UAV trajectories
   - Spatial Conflicts: Highlight proximity violations
   - Spatial-Temporal Conflicts: Show 4D overlaps
   - Flight Animation: Animate trajectories with time progression

5. **Review Summary**: The conflict panel displays UAV pairs in conflict, conflict types, time windows, and minimum separation distances.

## Technical Stack

- **Language**: Python 3.x
- **GUI Framework**: Tkinter
- **Data Processing**: NumPy, Pandas
- **Visualization**: Matplotlib (3D/Animated plots)
- **Conflict Detection**: Euclidean distance calculation with synchronized timestamp analysis


## Development

This project was developed with assistance from AI tools including ChatGPT for system design and documentation, Blackbox AI for code completion, and Sixth AI for codebase navigation and modular architecture.

## Future Enhancements

- Real-time telemetry integration 
- AI-driven route optimization and predictive conflict avoidance
- Web-based dashboard for live monitoring
- Scalability improvements for large-scale operations (10,000+ UAVs)
- Reinforcement learning for autonomous rerouting

