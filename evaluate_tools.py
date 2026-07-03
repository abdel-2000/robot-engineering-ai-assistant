from robot_assistant.analysis_tools import (
    analyze_package_xml,
    analyze_mqtt_config,
    analyze_robot_parameters,
)

from robot_assistant.analysis_tools.launch_analyzer import analyze_launch_file


def check(name: str, condition: bool):
    if condition:
        print(f"PASS - {name}")
    else:
        print(f"FAIL - {name}")


def main():
    ros2 = analyze_package_xml()
    launch = analyze_launch_file()
    mqtt = analyze_mqtt_config()
    safety = analyze_robot_parameters()

    check("ROS2 package.xml exists", ros2["status"] == "ok")
    check("ROS2 package name detected", ros2.get("name") == "assistive_robot")
    check("ROS2 dependencies detected", "rclpy" in ros2.get("dependencies", []))

    check("Launch file exists", launch["status"] == "ok")
    check("LaunchDescription detected", launch.get("has_launch_description") is True)
    check("robot_controller mentioned", launch.get("mentions_robot_controller") is True)

    check("MQTT config exists", mqtt["status"] == "ok")
    check("MQTT topics detected", mqtt.get("total_topics", 0) >= 1)
    check("MQTT security warning detected", len(mqtt.get("warnings", [])) >= 1)

    check("Safety params exist", safety["status"] == "ok")
    check("Emergency stop enabled", safety["parameters"].get("emergency_stop_enabled") is True)
    check("Safety score acceptable", safety.get("safety_score", 0) >= 80)


if __name__ == "__main__":
    main()