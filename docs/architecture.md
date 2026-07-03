# Robot Engineering AI Assistant Architecture

## Overview

Robot Engineering AI Assistant is a multi-agent AI system designed to help robotics engineers inspect, understand and review robotics software projects.

The system combines Google ADK, Model Context Protocol (MCP), reusable Python analysis tools and specialized AI agents.

The assistant never controls a physical robot.

Its purpose is software inspection, documentation review and engineering analysis.

---

# High-Level Architecture

```
                           User
                             │
                             ▼
                     Manager Agent
                             │
        ┌──────────────┬──────────────┬──────────────┐
        │              │              │              │
        ▼              ▼              ▼              ▼
 Project Explorer   ROS2 Expert   MQTT Expert   Safety Review
        │              │              │              │
        │              │              │              │
        ▼              ▼              ▼              ▼
Filesystem MCP   Python Tools   Python Tools   Python Tools
        │              │              │              │
        └──────────────┴──────────────┴──────────────┘
                             │
                             ▼
                     Robotics Workspace
                             │
                             ▼
                  Engineering Analysis Report
```

---

# System Components

## 1. Manager Agent

Responsibilities

- Receive user requests
- Understand user intent
- Select the correct specialist agent
- Coordinate the final response

The Manager Agent never performs technical analysis directly.

---

## 2. Project Explorer Agent

Responsibilities

- Inspect project folders
- Explain project organization
- Describe robotics software architecture
- Summarize workspace content

Main Tool

- Shared Filesystem MCP

---

## 3. ROS2 Expert Agent

Responsibilities

- Analyze ROS2 packages
- Review package.xml
- Inspect launch files
- Analyze ROS2 nodes
- Detect dependencies
- Explain ROS2 architecture

Python Tools

- ROS2 Package Analyzer
- Launch Analyzer

Files

```
workspace/package.xml
workspace/launch/robot_launch.py
workspace/src/robot_controller.py
```

---

## 4. MQTT Expert Agent

Responsibilities

- Analyze MQTT broker configuration
- Inspect telemetry topics
- Review command topics
- Detect communication risks
- Review MQTT security

Python Tool

- MQTT Analyzer

Files

```
workspace/config/mqtt_topics.yaml
```

---

## 5. Safety Review Agent

Responsibilities

- Review safety parameters
- Evaluate emergency stop
- Check robot speed
- Check acceleration
- Produce Safety Score

Python Tool

- Safety Analyzer

Files

```
workspace/config/robot_params.yaml
```

---

# Shared Filesystem MCP

The project uses the official Filesystem MCP Server.

```
@modelcontextprotocol/server-filesystem
```

The Filesystem MCP is shared by all specialist agents.

It allows the assistant to inspect only the authorized workspace folder.

The assistant cannot access arbitrary directories.

---

# Python Analysis Layer

Unlike a simple chatbot, the specialist agents rely on dedicated Python analysis tools before generating their answers.

Architecture

```
Specialist Agent

        │

        ▼

Python Analysis Tool

        │

        ▼

Workspace File

        │

        ▼

Structured Python Dictionary

        │

        ▼

Large Language Model

        │

        ▼

Engineering Report
```

---

# Python Analysis Tools

## ROS2 Package Analyzer

Reads

```
workspace/package.xml
```

Returns

- package name
- version
- description
- maintainer
- license
- dependencies
- missing dependencies

---

## Launch Analyzer

Reads

```
workspace/launch/robot_launch.py
```

Checks

- LaunchDescription
- launched nodes
- use_sim_time
- parameters
- launch configuration

---

## MQTT Analyzer

Reads

```
workspace/config/mqtt_topics.yaml
```

Checks

- broker
- host
- port
- client id
- telemetry topics
- command topics
- duplicated topics
- security warnings

---

## Safety Analyzer

Reads

```
workspace/config/robot_params.yaml
```

Checks

- maximum speed
- maximum acceleration
- maximum angular rate
- emergency stop
- human proximity threshold
- safety score

---

# Workspace

The assistant analyzes a robotics workspace.

```
workspace/

├── package.xml
├── README.md
├── launch/
│   └── robot_launch.py
├── src/
│   └── robot_controller.py
├── config/
│   ├── mqtt_topics.yaml
│   └── robot_params.yaml
```

---

# Safety Policy

The assistant never

- controls real robots
- executes robot movements
- sends commands to hardware
- bypasses safety systems

The assistant only

- reads files
- analyzes software
- reviews documentation
- generates engineering reports

---

# Current Architecture Status

Completed

- Manager Agent
- Project Explorer Agent
- ROS2 Expert Agent
- MQTT Expert Agent
- Safety Review Agent
- Shared Filesystem MCP
- ROS2 Package Analyzer
- Launch Analyzer
- MQTT Analyzer
- Safety Analyzer
- Workspace Demo
- Documentation
- Evaluation

Status

**Version 1.0 – Ready for Demonstration**

---

# Future Architecture

Planned improvements

- URDF Analyzer
- MoveIt2 Analyzer
- Gazebo Analyzer
- RViz Analyzer
- ROS2 Topic Analyzer
- Diagnostics Agent
- Planning Agent
- GitHub Actions
- Automated Testing
- CI/CD Pipeline