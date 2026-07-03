# Robot Engineering AI Assistant

An AI-powered multi-agent assistant for robotics software engineering, ROS2 project analysis, MQTT communication review, and robotics safety assessment.

---

# Project Goal

Robot Engineering AI Assistant helps robotics engineers inspect, understand, and review robotics software projects without manually reading hundreds of files.

The assistant analyzes a robotics workspace, extracts technical information, and generates engineering reports.

This project was developed as part of the Google × Kaggle AI Agents learning journey.

---

# Main Features

- Multi-Agent Architecture
- Manager Agent
- Project Explorer Agent
- ROS2 Expert Agent
- MQTT Expert Agent
- Safety Review Agent
- Shared Filesystem MCP Server
- Python Analysis Tools
- Skills-based architecture
- Evaluation test cases
- Robotics workspace analysis

---

# Technologies

- Google ADK
- Gemini API
- Python
- ROS2
- MQTT
- Model Context Protocol (MCP)
- Filesystem MCP Server
- Node.js / npm

---

# Project Architecture

```
User
 │
 ▼
Manager Agent
 │
 ├──────────────┬──────────────┬──────────────┐
 │              │              │              │
 ▼              ▼              ▼              ▼
Explorer     ROS2 Expert    MQTT Expert   Safety Review
 │              │              │              │
 │              │              │              │
 ▼              ▼              ▼              ▼
Filesystem   ROS2 Tools     MQTT Tools    Safety Tools
      \           |              |             /
       \__________|______________|____________/
                      │
                      ▼
                 Workspace Files
                      │
                      ▼
              Engineering Report
```

---

# Agents

## Manager Agent

Responsibilities:

- Receive user requests
- Understand user intent
- Route the request to the correct specialist agent
- Aggregate results

---

## Project Explorer Agent

Responsibilities:

- Analyze workspace structure
- Explain project architecture
- Describe folders and files
- Provide project summaries

---

## ROS2 Expert Agent

Responsibilities:

- Analyze ROS2 packages
- Analyze package.xml
- Analyze launch files
- Analyze ROS2 nodes
- Identify dependencies
- Review ROS2 project organization

Uses:

- ROS2 Package Analyzer
- Launch Analyzer

---

## MQTT Expert Agent

Responsibilities:

- Analyze MQTT configuration
- Inspect broker settings
- Analyze command topics
- Analyze telemetry topics
- Detect communication risks

Uses:

- MQTT Analyzer

---

## Safety Review Agent

Responsibilities:

- Review robot safety parameters
- Evaluate emergency stop configuration
- Review speed limits
- Review acceleration limits
- Generate safety reports
- Produce Safety Score

Uses:

- Safety Analyzer

---

# Python Analysis Tools

The project contains reusable Python tools that perform structured engineering analysis before the LLM generates its answer.

## ROS2 Package Analyzer

Reads:

```
workspace/package.xml
```

Extracts:

- Package name
- Version
- Description
- Maintainer
- License
- Dependencies
- Missing recommended dependencies

---

## Launch Analyzer

Reads:

```
workspace/launch/robot_launch.py
```

Checks:

- LaunchDescription
- ROS2 Nodes
- Parameters
- use_sim_time
- Launch configuration

---

## MQTT Analyzer

Reads:

```
workspace/config/mqtt_topics.yaml
```

Analyzes:

- Broker
- Port
- Client ID
- Topics
- Telemetry
- Commands
- Safety topics
- Duplicate topics
- Security warnings

---

## Safety Analyzer

Reads:

```
workspace/config/robot_params.yaml
```

Checks:

- Maximum speed
- Maximum acceleration
- Human proximity threshold
- Emergency Stop
- Safety parameters
- Safety Score

---

# Workspace

The assistant analyzes a robotics workspace containing files such as:

```
workspace/

├── package.xml
├── launch/
│   └── robot_launch.py
├── src/
│   └── robot_controller.py
├── config/
│   ├── mqtt_topics.yaml
│   └── robot_params.yaml
└── README.md
```

---

# Skills

Current Skills:

- Project Explorer Skill
- Safety Review Skill

The Skills define the behavior and responsibilities of the specialist agents.

---

# MCP Integration

The project uses the official Filesystem MCP Server.

```
@modelcontextprotocol/server-filesystem
```

The Filesystem MCP is shared across all specialist agents.

It allows agents to safely inspect only the authorized `workspace/` directory.

---

# Safety Policy

The assistant never:

- Controls a real robot
- Executes robot movements
- Sends commands to physical hardware
- Bypasses safety systems

The assistant only analyzes project files and generates engineering reports.

---

# Evaluation

The project includes evaluation scenarios for testing:

- Workspace exploration
- ROS2 analysis
- MQTT analysis
- Safety review
- Architecture explanation

---

# Current Status

Current Version:

**v1.0 (Prototype)**

Completed:

- Multi-Agent Architecture
- Manager Agent
- ROS2 Expert Agent
- MQTT Expert Agent
- Safety Review Agent
- Shared Filesystem MCP
- Python Analysis Tools
- Documentation
- Workspace Demo
- Evaluation Suite

---

# Future Improvements

- MoveIt2 Analyzer
- Gazebo Analyzer
- URDF Analyzer
- RViz Analyzer
- ROS2 Topic Analyzer
- AI Planning Agent
- Robot Diagnostics Agent
- Automated Testing
- GitHub Actions CI/CD

---

# License

Apache-2.0

---
## Author

**Abdellatif El Majdoubi**

AI & Robotics Engineering Student

This project was developed as part of the **Google × Kaggle AI Agents: Intensive Vibe Coding Course (2026)** and contributes to my robotics engineering portfolio, focusing on AI Agents, Google ADK, ROS2, MQTT, Model Context Protocol (MCP), and robotic software analysis.

GitHub: https://github.com/abdel-2000
## Automated Evaluation

The project includes an automated evaluation script:

```bash
python evaluate_tools.py
## Why this project

Robotics software projects are complex and often contain hundreds of files.

Robot Engineering AI Assistant helps robotics engineers quickly inspect ROS2 projects, review MQTT communication, evaluate robot safety parameters and generate engineering reports using multiple AI agents and reusable Python analysis tools.