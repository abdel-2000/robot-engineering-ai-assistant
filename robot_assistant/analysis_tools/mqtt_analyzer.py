from pathlib import Path
import yaml


def analyze_mqtt_config(workspace_path: str = "workspace") -> dict:
    mqtt_file = Path(workspace_path) / "config" / "mqtt_topics.yaml"

    if not mqtt_file.exists():
        return {
            "status": "missing",
            "file": str(mqtt_file),
            "message": "mqtt_topics.yaml not found",
        }

    with open(mqtt_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    mqtt = data.get("mqtt", {})

    broker = mqtt.get("broker", {})
    topics = mqtt.get("topics", {})

    all_topics = []

    for value in topics.values():
        if isinstance(value, str):
            all_topics.append(value)

    duplicated_topics = sorted(
        {topic for topic in all_topics if all_topics.count(topic) > 1}
    )

    warnings = []

    if broker.get("port") == 1883:
        warnings.append("MQTT broker uses port 1883 without TLS.")

    if not broker.get("tls_enabled", False):
        warnings.append("TLS is not enabled for MQTT communication.")

    if not broker.get("authentication_required", False):
        warnings.append("MQTT authentication is not required.")

    return {
        "status": "ok",
        "file": str(mqtt_file),
        "broker": broker,
        "topics": topics,
        "total_topics": len(all_topics),
        "duplicated_topics": duplicated_topics,
        "warnings": warnings,
    }