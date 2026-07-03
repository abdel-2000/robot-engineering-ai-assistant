from pathlib import Path
import yaml


def analyze_robot_parameters(workspace_path: str = "workspace") -> dict:
    params_file = Path(workspace_path) / "config" / "robot_params.yaml"

    if not params_file.exists():
        return {
            "status": "missing",
            "file": str(params_file),
            "message": "robot_params.yaml not found",
        }

    with open(params_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    params = data.get("robot_controller", {}).get("ros__parameters", {})

    warnings = []
    score = 100

    max_speed = params.get("max_speed")
    max_acceleration = params.get("max_acceleration")
    force_limit = params.get("force_limit")
    proximity_threshold = params.get("human_proximity_threshold")
    emergency_stop_enabled = params.get("emergency_stop_enabled")

    if max_speed is None:
        warnings.append("Missing max_speed parameter.")
        score -= 20
    elif max_speed > 0.5:
        warnings.append("Maximum speed is high for assistive robotics near humans.")
        score -= 15

    if max_acceleration is None:
        warnings.append("Missing max_acceleration parameter.")
        score -= 15
    elif max_acceleration > 0.3:
        warnings.append("Maximum acceleration is high for close human interaction.")
        score -= 10

    if force_limit is None:
        warnings.append("Missing force_limit parameter.")
        score -= 10
    elif force_limit > 150:
        warnings.append("Force limit is high for assistive robotics.")
        score -= 15

    if proximity_threshold is None:
        warnings.append("Missing human_proximity_threshold parameter.")
        score -= 15
    elif proximity_threshold < 1.0:
        warnings.append("Human proximity threshold may be too small.")
        score -= 10

    if emergency_stop_enabled is not True:
        warnings.append("Emergency stop is not enabled.")
        score -= 25

    score = max(score, 0)

    return {
        "status": "ok",
        "file": str(params_file),
        "parameters": params,
        "warnings": warnings,
        "safety_score": score,
    }