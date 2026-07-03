from pathlib import Path
import xml.etree.ElementTree as ET


def analyze_package_xml(workspace_path: str = "workspace") -> dict:
    package_file = Path(workspace_path) / "package.xml"

    if not package_file.exists():
        return {
            "status": "missing",
            "file": str(package_file),
            "message": "package.xml not found",
        }

    tree = ET.parse(package_file)
    root = tree.getroot()

    def text(tag):
        element = root.find(tag)
        return element.text.strip() if element is not None and element.text else None

    dependencies = []
    for tag in ["depend", "exec_depend", "build_depend", "test_depend"]:
        for dep in root.findall(tag):
            if dep.text:
                dependencies.append(dep.text.strip())

    return {
        "status": "ok",
        "file": str(package_file),
        "name": text("name"),
        "version": text("version"),
        "description": text("description"),
        "maintainer": text("maintainer"),
        "license": text("license"),
        "dependencies": sorted(set(dependencies)),
        "missing_recommended_dependencies": [
            dep for dep in ["rclpy", "std_msgs", "geometry_msgs"]
            if dep not in dependencies
        ],
    }