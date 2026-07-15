// AUTO-GENERATED FILE. DO NOT MODIFY.

export interface PacketHeader {
    sync_1: number;
    sync_2: number;
    protocol_version: number;
    source_module: number;
    dest_module: number;
    priority: number;
    sequence_num: number;
    timestamp_ms: number;
    payload_type: number;
    payload_length: number;
    header_crc: number;
}

export interface HeartbeatPacket {
    system_state: number;
    operating_mode: number;
    mission_mode: number;
    battery_v: number;
    uptime_ms: number;
}

export interface MotionCommand {
    left_pwm: number;
    right_pwm: number;
    duration_ms: number;
}

export interface ServoCommand {
    servo_id: number;
    target_angle: number;
    speed: number;
}

export interface SensorTelemetry {
    sensor_type: number;
    reading_1: number;
    reading_2: number;
    reading_3: number;
}

export interface MissionPacket {
    mission_mode: number;
    command_type: number;
    waypoint_count: number;
}

export interface ConfigurationPacket {
    config_id: number;
    value: number;
}

export interface DiagnosticPacket {
    module_id: number;
    error_code: number;
    free_heap: number;
    cpu_usage_pct: number;
}

export interface EventPacket {
    event_type: number;
    event_data: number;
}

export interface StatusPacket {
    connection_state: number;
    health_state: number;
    safety_state: number;
}

export interface OLEDPacket {
    line_number: number;
    text: string;
}

export interface AIPredictionPacket {
    prediction_class: number;
    confidence: number;
}
