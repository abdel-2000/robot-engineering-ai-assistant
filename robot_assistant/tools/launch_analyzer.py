import os
import ast

def analyze_launch_file(launch_file_path: str = "workspace/launch/robot_launch.py") -> str:
    """
    Analyzes a ROS2 launch file and returns details of nodes, parameter structures, use_sim_time, issues, and recommendations.
    
    Args:
        launch_file_path (str): Path to the launch file.
        
    Returns:
        str: A formatted analysis report.
    """
    if not os.path.exists(launch_file_path):
        return f"Error: Launch file not found at {launch_file_path}."
        
    try:
        with open(launch_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return f"Error reading launch file {launch_file_path}: {str(e)}"
        
    launched_nodes = []
    parameters = []
    use_sim_time = "Unknown"
    missing_configs = []
    recommendations = []
    
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'Node':
                pkg = None
                exe = None
                node_name = None
                node_params = []
                
                for kw in node.keywords:
                    if kw.arg == 'package':
                        if isinstance(kw.value, ast.Constant):
                            pkg = kw.value.value
                        elif isinstance(kw.value, ast.Str):
                            pkg = kw.value.s
                    elif kw.arg == 'executable':
                        if isinstance(kw.value, ast.Constant):
                            exe = kw.value.value
                        elif isinstance(kw.value, ast.Str):
                            exe = kw.value.s
                    elif kw.arg == 'name':
                        if isinstance(kw.value, ast.Constant):
                            node_name = kw.value.value
                        elif isinstance(kw.value, ast.Str):
                            node_name = kw.value.s
                    elif kw.arg == 'parameters':
                        if isinstance(kw.value, ast.List):
                            for item in kw.value.elts:
                                if isinstance(item, ast.Dict):
                                    for k, v in zip(item.keys, item.values):
                                        key_val = None
                                        if isinstance(k, ast.Constant):
                                            key_val = k.value
                                        elif isinstance(k, ast.Str):
                                            key_val = k.s
                                        if key_val:
                                            node_params.append(key_val)
                                            if key_val == 'use_sim_time':
                                                if isinstance(v, ast.Constant):
                                                    use_sim_time = str(v.value)
                                                elif isinstance(v, ast.Name):
                                                    use_sim_time = v.id
                                                else:
                                                    use_sim_time = "True/Dynamic"
                
                node_info = f"Node '{node_name}' (pkg: '{pkg}', exe: '{exe}')" if node_name else f"Unnamed Node (pkg: '{pkg}', exe: '{exe}')"
                launched_nodes.append(node_info)
                if node_params:
                    parameters.extend(node_params)
    except Exception as e:
        if "Node(" in content:
            launched_nodes.append("Found Node declaration (failed to parse AST details)")
            
    if not parameters:
        if "use_sim_time" in content:
            use_sim_time = "Declared (detected via text)"
            parameters.append("use_sim_time")
            
    if "use_sim_time" not in content:
        missing_configs.append("use_sim_time parameter specification")
        recommendations.append("Add 'use_sim_time' parameter support to nodes to ensure simulation synchronization.")
        
    if "robot_params.yaml" not in content and "config" not in content:
        missing_configs.append("External YAML parameters loading config")
        recommendations.append("Configure the launch file to load node parameters from 'config/robot_params.yaml' dynamically.")
        
    if "stdout" not in content and "output=" not in content:
        missing_configs.append("Output/logging output redirection configuration")
        recommendations.append("Specify output='screen' in Node instantiation for console log streaming.")
        
    report = []
    report.append("=== ROS2 Launch File Analysis ===")
    report.append("Launched Nodes:")
    if launched_nodes:
        for n in launched_nodes:
            report.append(f" - {n}")
    else:
        report.append(" - None detected")
        
    report.append(f"Parameters Found: {', '.join(set(parameters)) if parameters else 'None'}")
    report.append(f"use_sim_time Configured: {use_sim_time}")
    
    report.append("Missing Configuration:")
    if missing_configs:
        for m in missing_configs:
            report.append(f" - {m}")
    else:
        report.append(" - None")
        
    report.append("Recommendations:")
    if recommendations:
        for r in recommendations:
            report.append(f" - {r}")
    else:
        report.append(" - None")
        
    return "\n".join(report)
