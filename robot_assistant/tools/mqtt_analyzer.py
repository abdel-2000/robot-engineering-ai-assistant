import os
import yaml

def analyze_mqtt_config(mqtt_config_path: str = "workspace/config/mqtt_topics.yaml") -> str:
    """
    Analyzes an MQTT topic configuration YAML file and evaluates its security, QoS, and topic layout.
    
    Args:
        mqtt_config_path (str): Path to the MQTT topics YAML file.
        
    Returns:
        str: A formatted analysis report.
    """
    if not os.path.exists(mqtt_config_path):
        return f"Error: MQTT config file not found at {mqtt_config_path}."
        
    try:
        with open(mqtt_config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return f"Error parsing MQTT YAML file {mqtt_config_path}: {str(e)}"
        
    if not data or 'mqtt' not in data:
        return "Error: Invalid MQTT config structure (missing 'mqtt' root key)."
        
    mqtt_data = data['mqtt']
    broker_data = mqtt_data.get('broker', {})
    topics_data = mqtt_data.get('topics', {})
    
    broker = broker_data.get('host', 'Unknown')
    port = broker_data.get('port', 1883)
    
    # Evaluate TLS
    tls_enabled = False
    if broker_data.get('tls') or broker_data.get('ssl') or port == 8883:
        tls_enabled = True
        
    # Evaluate Authentication
    auth_enabled = False
    if 'username' in broker_data or 'password' in broker_data or broker_data.get('auth'):
        auth_enabled = True
        
    # QoS
    qos = broker_data.get('qos', 'Not specified')
    
    telemetry_topics = []
    command_topics = []
    safety_topics = []
    all_topics = {}
    duplicated_topics = []
    
    for key, val in topics_data.items():
        if not val:
            continue
            
        val_str = str(val)
        if val_str in all_topics.values():
            orig_keys = [k for k, v in all_topics.items() if v == val_str]
            duplicated_topics.append(f"{val_str} (mapped to '{key}' and '{orig_keys[0]}')")
        all_topics[key] = val_str
        
        key_lower = key.lower()
        val_lower = val_str.lower()
        
        if 'estop' in key_lower or 'safety' in key_lower or 'estop' in val_lower or 'safety' in val_lower:
            safety_topics.append(f"{key}: {val_str}")
        elif 'cmd' in key_lower or 'control' in key_lower or 'command' in key_lower or 'cmd' in val_lower or 'control' in val_lower:
            command_topics.append(f"{key}: {val_str}")
        elif 'telemetry' in key_lower or 'status' in key_lower or 'state' in key_lower or 'sensor' in key_lower or 'telemetry' in val_lower or 'status' in val_lower:
            telemetry_topics.append(f"{key}: {val_str}")
        else:
            telemetry_topics.append(f"{key}: {val_str}")
            
    sec_recommendations = []
    if port == 1883 and not tls_enabled:
        sec_recommendations.append("Enable TLS/SSL encryption. Standard unencrypted port 1883 is active, transmitting control commands in plain text.")
    if not auth_enabled:
        sec_recommendations.append("Configure client credentials (username/password) or certificate-based authentication on the broker.")
    if not broker_data.get('client_id'):
        sec_recommendations.append("Ensure a unique and randomized client ID configuration to prevent broker connection conflicts.")
    if qos == 'Not specified':
        sec_recommendations.append("Specify explicit QoS levels. For safety-critical topics (like estop), use QoS 2 (exactly once). For telemetry, QoS 1 (at least once) or QoS 0 is acceptable.")
        
    report = []
    report.append("=== MQTT Configuration Analysis ===")
    report.append(f"Broker Host: {broker}")
    report.append(f"Port: {port}")
    report.append(f"TLS Enabled: {tls_enabled}")
    report.append(f"Authentication Configured: {auth_enabled}")
    report.append(f"QoS Configured: {qos}")
    
    report.append("Telemetry Topics:")
    if telemetry_topics:
        for t in telemetry_topics:
            report.append(f" - {t}")
    else:
        report.append(" - None")
        
    report.append("Command Topics:")
    if command_topics:
        for t in command_topics:
            report.append(f" - {t}")
    else:
        report.append(" - None")
        
    report.append("Safety Topics:")
    if safety_topics:
        for t in safety_topics:
            report.append(f" - {t}")
    else:
        report.append(" - None")
        
    report.append("Duplicated Topics:")
    if duplicated_topics:
        for d in duplicated_topics:
            report.append(f" - {d}")
    else:
        report.append(" - None")
        
    report.append("Security Recommendations:")
    if sec_recommendations:
        for r in sec_recommendations:
            report.append(f" - {r}")
    else:
        report.append(" - None")
        
    return "\n".join(report)
