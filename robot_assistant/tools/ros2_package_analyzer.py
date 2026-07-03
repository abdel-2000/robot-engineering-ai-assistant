import os
import xml.etree.ElementTree as ET

def analyze_ros2_package(package_xml_path: str = "workspace/package.xml") -> str:
    """
    Analyzes a ROS2 package.xml file and returns structured information about package details, dependencies, and issues.
    
    Args:
        package_xml_path (str): Path to the package.xml file.
        
    Returns:
        str: A formatted analysis report.
    """
    if not os.path.exists(package_xml_path):
        return f"Error: package.xml file not found at {package_xml_path}."
        
    try:
        tree = ET.parse(package_xml_path)
        root = tree.getroot()
    except Exception as e:
        return f"Error parsing XML file {package_xml_path}: {str(e)}"
        
    # Get basic details
    pkg_name = root.findtext('name', '').strip()
    version = root.findtext('version', '').strip()
    license_text = root.findtext('license', '').strip()
    
    maintainer_elem = root.find('maintainer')
    maintainer = ""
    maintainer_email = ""
    if maintainer_elem is not None:
        maintainer = maintainer_elem.text.strip() if maintainer_elem.text else ""
        maintainer_email = maintainer_elem.get('email', '').strip()
        
    # Find dependencies
    dependencies = []
    for dep_type in ['depend', 'build_depend', 'exec_depend', 'test_depend', 'buildtool_depend']:
        for dep in root.findall(dep_type):
            if dep.text:
                dependencies.append(dep.text.strip())
    # De-duplicate
    dependencies = sorted(list(set(dependencies)))
    
    # Analyze warnings/missing dependencies
    warnings = []
    missing_dependencies = []
    
    # For assistive robotics Python packages, usually we expect rclpy, std_msgs, geometry_msgs
    expected_deps = ['rclpy', 'std_msgs', 'geometry_msgs']
    for exp in expected_deps:
        if exp not in dependencies:
            missing_dependencies.append(exp)
            
    # Check format version
    fmt = root.get('format')
    if fmt != '3':
        warnings.append(f"package.xml format is '{fmt}'. It is recommended to use format='3'.")
        
    if not pkg_name:
        warnings.append("Package name is missing or empty.")
    if not version:
        warnings.append("Package version is missing.")
    if not maintainer:
        warnings.append("Maintainer name is missing.")
    if maintainer_email and "example.com" in maintainer_email:
        warnings.append(f"Maintainer email '{maintainer_email}' is a placeholder.")
        
    # Build report
    report = []
    report.append("=== ROS2 Package Analysis ===")
    report.append(f"Package Name: {pkg_name if pkg_name else 'Unknown'}")
    report.append(f"Version: {version if version else 'Unknown'}")
    report.append(f"Maintainer: {maintainer} ({maintainer_email})" if maintainer_email else f"Maintainer: {maintainer}")
    report.append(f"License: {license_text if license_text else 'Unknown'}")
    report.append(f"Dependencies: {', '.join(dependencies) if dependencies else 'None'}")
    report.append(f"Missing Dependencies: {', '.join(missing_dependencies) if missing_dependencies else 'None'}")
    report.append("Warnings:")
    if warnings:
        for w in warnings:
            report.append(f" - {w}")
    else:
        report.append(" - None")
        
    return "\n".join(report)
