// AUTO-GENERATED FILE. DO NOT MODIFY.

export interface HeartbeatPacket {
    timestamp_ms: number;
    system_state: number;
    battery_v: number;
}

export interface CommandPacket {
    command_type: number;
    payload_length: number;
    payload: number[];
}

export interface TelemetryPacket {
    telemetry_type: number;
    payload_length: number;
    payload: number[];
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

