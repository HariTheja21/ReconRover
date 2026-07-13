// AUTO-GENERATED FILE. DO NOT MODIFY.
#ifndef ROVER_PACKETS_H
#define ROVER_PACKETS_H

#include <stdint.h>

#pragma pack(push, 1)

struct HeartbeatPacket {
    uint32_t timestamp_ms;
    uint8_t system_state;
    float battery_v;
};

struct CommandPacket {
    uint8_t command_type;
    uint8_t payload_length;
    uint8_t payload[254];
};

struct TelemetryPacket {
    uint8_t telemetry_type;
    uint8_t payload_length;
    uint8_t payload[254];
};

struct MotionCommand {
    int16_t left_pwm;
    int16_t right_pwm;
    uint16_t duration_ms;
};

struct ServoCommand {
    uint8_t servo_id;
    uint8_t target_angle;
    uint8_t speed;
};

struct SensorTelemetry {
    uint8_t sensor_type;
    float reading_1;
    float reading_2;
    float reading_3;
};

#pragma pack(pop)

#endif // ROVER_PACKETS_H
