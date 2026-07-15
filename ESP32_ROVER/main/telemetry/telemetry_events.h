#pragma once
#include <cstdint>

namespace ReconRover {
namespace Telemetry {

// Event types representing raw telemetry data emitted by hardware drivers
enum class TelemetryType {
    HEARTBEAT = 0x80,
    RUNTIME_STATUS = 0x81,
    MOTOR_STATUS = 0x82,
    SERVO_STATUS = 0x83,
    BATTERY_STATUS = 0x84,
    IMU_STATUS = 0x85,
    OLED_STATUS = 0x86,
    RGB_STATUS = 0x87,
    BUZZER_STATUS = 0x88,
    SYSTEM_HEALTH = 0x89
};

// Represents an abstract outgoing event payload (before byte serialization)
struct TelemetryEvent {
    TelemetryType type;
    uint32_t timestamp_ms;
    union {
        struct { uint8_t uptime_s; } heartbeat;
        struct { int16_t left_v; int16_t right_v; } motor;
        struct { uint8_t id; int16_t angle; } servo;
        struct { uint16_t voltage_mv; uint8_t soc_pct; } battery;
        struct { int16_t ax; int16_t ay; int16_t az; } imu;
    } payload;
};

// The fully serialized packet ready for UART transport
struct TelemetryPacket {
    static constexpr uint8_t MAX_LENGTH = 16;
    uint8_t buffer[MAX_LENGTH];
    uint8_t length;
};

} // namespace Telemetry
} // namespace ReconRover
