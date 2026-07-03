from pathlib import Path


def analyze_launch_file(workspace_path: str = "workspace") -> dict:
    launch_file = Path(workspace_path) / "launch" / "robot_launch.py"

    if not launch_file.exists():
        return {
            "status": "missing",
            "file": str(launch_file),
            "message": "robot_launch.py not found",
        }

    content = launch_file.read_text(encoding="utf-8")

    return {
        "status": "ok",
        "file": str(launch_file),
        "has_launch_description": "LaunchDescription" in content,
        "uses_node": "Node(" in content,
        "uses_sim_time": "use_sim_time" in content,
        "mentions_robot_controller": "robot_controller" in content,
        "uses_parameters": "parameters" in content,
        "warnings": [
            warning
            for warning in [
                None if "LaunchDescription" in content else "Missing LaunchDescription.",
                None if "Node(" in content else "No ROS2 Node launch detected.",
                None if "use_sim_time" in content else "use_sim_time not configured.",
                None if "parameters" in content else "No parameters passed to launched node.",
            ]
            if warning is not None
        ],
    }