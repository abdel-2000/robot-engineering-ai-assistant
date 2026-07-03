# Robot Engineering AI Assistant Demo

## Introduction

This demo presents the Robot Engineering AI Assistant.

The assistant is designed to help robotics engineers inspect and review robotics software projects using multiple AI agents and Python analysis tools.

---

# Architecture

User

↓

Manager Agent

↓

Specialist Agent

↓

Python Analysis Tool

↓

Workspace Files

↓

Engineering Report

---

# Demo 1 — Project Structure

User asks:

Analyze my robotics workspace.

Manager Agent

↓

Project Explorer Agent

↓

Filesystem MCP

↓

workspace/

↓

Project Structure Report

---

# Demo 2 — ROS2 Analysis

User asks:

Analyze my ROS2 package.

Manager Agent

↓

ROS2 Expert Agent

↓

ROS2 Package Analyzer

↓

package.xml

↓

Engineering Report

Expected Report

- Package name
- Version
- Dependencies
- Maintainer
- Missing dependencies

---

# Demo 3 — Launch Analysis

User asks:

Review my ROS2 launch configuration.

Manager Agent

↓

ROS2 Expert Agent

↓

Launch Analyzer

↓

robot_launch.py

↓

Launch Report

Expected Report

- LaunchDescription
- ROS2 Nodes
- Parameters
- use_sim_time

---

# Demo 4 — MQTT Review

User asks:

Review my MQTT communication.

Manager Agent

↓

MQTT Expert Agent

↓

MQTT Analyzer

↓

mqtt_topics.yaml

↓

MQTT Report

Expected Report

- Broker
- Topics
- Telemetry
- Commands
- Security warnings

---

# Demo 5 — Safety Review

User asks:

Review robot safety.

Manager Agent

↓

Safety Review Agent

↓

Safety Analyzer

↓

robot_params.yaml

↓

Safety Report

Expected Report

- Maximum speed
- Acceleration
- Human proximity threshold
- Emergency Stop
- Safety Score

---

# Automated Evaluation

Run

```bash
python evaluate_tools.py
```

Expected Output

PASS

PASS

PASS

PASS

PASS

PASS

PASS

PASS

PASS

PASS

PASS

PASS

---

# Technologies

- Google ADK
- Gemini
- Python
- ROS2
- MQTT
- MCP
- Filesystem MCP

---

# Current Status

Version 1.0

Ready for demonstration.