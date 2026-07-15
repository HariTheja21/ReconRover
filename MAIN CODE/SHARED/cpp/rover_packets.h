// AUTO-GENERATED FILE. DO NOT MODIFY.
#ifndef ROVER_PACKETS_H
#define ROVER_PACKETS_H

#include <stdint.h>

#pragma pack(push, 1)

struct PacketHeader {
    uint8_t sync_1;
    uint8_t sync_2;
    uint8_t protocol_version;
    uint8_t source_module;
    uint8_t dest_module;
    uint8_t priority;
    uint16_t sequence_num;
    uint32_t timestamp_ms;
    uint8_t payload_type;
    uint16_t payload_length;
    uint16_t header_crc;
};

struct HeartbeatPacket {
    uint8_t system_state;
    uint8_t operating_mode;
    uint8_t mission_mode;
    float battery_v;
    uint32_t uptime_ms;
};

struct MotionCommand {
    int16_t left_pwm;
    int16_t right_pwm;
    uint16_t duration_ms;
};

struct ServoCommand {
    uint8_t servo_id;
    uint16_t target_angle;
    uint16_t speed;
};

struct SensorTelemetry {
    uint8_t sensor_type;
    float reading_1;
    float reading_2;
    float reading_3;
};

struct MissionPacket {
    uint8_t mission_mode;
    uint8_t command_type; // e.g. Start, Stop, Pause
    uint16_t waypoint_count;
};

struct ConfigurationPacket {
    uint8_t config_id;
    float value;
};

struct DiagnosticPacket {
    uint8_t module_id;
    uint8_t error_code;
    uint32_t free_heap;
    uint8_t cpu_usage_pct;
};

struct EventPacket {
    uint8_t event_type;
    uint32_t event_data;
};

struct StatusPacket {
    uint8_t connection_state;
    uint8_t health_state;
    uint8_t safety_state;
};

struct OLEDPacket {
    uint8_t line_number;
    char text[20];
};

struct AIPredictionPacket {
    uint8_t prediction_class;
    float confidence;
};

#pragma pack(pop)

#endif // ROVER_PACKETS_H
