import os
import yaml

def analyze_safety_parameters(params_path: str = "workspace/config/robot_params.yaml") -> str:
    """
    Analyzes a robot configuration parameters YAML file from a safety perspective, calculating a safety score.
    
    Args:
        params_path (str): Path to the robot parameters YAML file.
        
    Returns:
        str: A formatted safety report.
    """
    if not os.path.exists(params_path):
        return f"Error: Safety parameter file not found at {params_path}."
        
    try:
        with open(params_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return f"Error parsing safety YAML file {params_path}: {str(e)}"
        
    if not data:
        return "Error: Empty or invalid YAML parameter file."
        
    params = {}
    if 'robot_controller' in data and 'ros__parameters' in data['robot_controller']:
        params = data['robot_controller']['ros__parameters']
    else:
        def find_params_recursive(d):
            res = {}
            for k, v in d.items():
                if isinstance(v, dict):
                    res.update(find_params_recursive(v))
                else:
                    res[k] = v
            return res
        params = find_params_recursive(data)
        
    max_speed = params.get('max_speed')
    max_accel = params.get('max_acceleration')
    force_limit = params.get('force_limit') or params.get('max_force')
    estop_enabled = params.get('emergency_stop_enabled')
    proximity_threshold = params.get('human_proximity_threshold')
    
    missing_params = []
    warnings = []
    score = 10.0
    
    if max_speed is None:
        missing_params.append("max_speed")
        warnings.append("Maximum speed limit ('max_speed') is not specified.")
        score -= 2.0
    else:
        try:
            val = float(max_speed)
            if val > 1.0:
                warnings.append(f"Maximum speed ({val} m/s) is high for an indoor assistive robot. Recommend limiting to <= 1.0 m/s.")
                score -= 1.5
            elif val <= 0.0:
                warnings.append("Maximum speed is set to 0 or negative value; robot will not move.")
                score -= 0.5
        except (ValueError, TypeError):
            warnings.append("Maximum speed is not a valid number.")
            score -= 1.0
            
    if max_accel is None:
        missing_params.append("max_acceleration")
        warnings.append("Maximum acceleration limit ('max_acceleration') is not specified.")
        score -= 1.5
    else:
        try:
            val = float(max_accel)
            if val > 0.5:
                warnings.append(f"Maximum acceleration ({val} m/s^2) is high. Recommend limiting to <= 0.5 m/s^2 for smooth deceleration.")
                score -= 1.0
        except (ValueError, TypeError):
            warnings.append("Maximum acceleration is not a valid number.")
            score -= 1.0
            
    if force_limit is None:
        missing_params.append("force_limit")
        warnings.append("Collision force limit ('force_limit') is not specified. Highly recommended for collaborative and assistive robots.")
        score -= 1.5
        
    if estop_enabled is None:
        missing_params.append("emergency_stop_enabled")
        warnings.append("Emergency stop status parameter ('emergency_stop_enabled') is missing.")
        score -= 2.0
    elif estop_enabled is not True:
        warnings.append("Emergency stop is initially disabled (enabled: false). Recommend setting to true by default for safe initialization.")
        score -= 2.0
        
    if proximity_threshold is None:
        missing_params.append("human_proximity_threshold")
        warnings.append("Human proximity deceleration/stop threshold ('human_proximity_threshold') is not specified.")
        score -= 2.0
    else:
        try:
            val = float(proximity_threshold)
            if val < 0.8:
                warnings.append(f"Human proximity threshold ({val} m) is low. Safety margin should be at least 0.8-1.0m to allow for safe braking.")
                score -= 1.0
        except (ValueError, TypeError):
            warnings.append("Human proximity threshold is not a valid number.")
            score -= 1.0
            
    score = max(0.0, min(10.0, score))
    
    report = []
    report.append("=== Robot Safety Parameter Analysis ===")
    report.append(f"Maximum Speed: {max_speed if max_speed is not None else 'Not set'} m/s")
    report.append(f"Maximum Acceleration: {max_accel if max_accel is not None else 'Not set'} m/s^2")
    report.append(f"Force Limits: {force_limit if force_limit is not None else 'Not set'} N")
    report.append(f"Emergency Stop Enabled (Initial): {estop_enabled}")
    report.append(f"Human Proximity Threshold: {proximity_threshold if proximity_threshold is not None else 'Not set'} m")
    
    report.append("Missing Parameters:")
    if missing_params:
        for m in missing_params:
            report.append(f" - {m}")
    else:
        report.append(" - None")
        
    report.append("Safety Warnings:")
    if warnings:
        for w in warnings:
            report.append(f" - {w}")
    else:
        report.append(" - None")
        
    report.append(f"Overall Safety Score: {score:.1f}/10.0")
    
    return "\n".join(report)
