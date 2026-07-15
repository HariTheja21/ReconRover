#pragma once
#include <cstdint>

namespace ReconRover {
namespace Runtime {

enum class EventType {
    MOTOR_COMMAND,
    SERVO_COMMAND,
    OLED_COMMAND,
    RGB_COMMAND,
    BUZZER_COMMAND,
    EMERGENCY_STOP,
    RUNTIME_HEALTH
};

struct MotorCommandEvent {
    int16_t left_velocity;
    int16_t right_velocity;
};

struct ServoCommandEvent {
    uint8_t servo_id;
    int16_t angle;
};

struct OLEDCommandEvent {
    uint8_t display_mode;
};

struct RGBCommandEvent {
    uint8_t r, g, b;
};

struct BuzzerCommandEvent {
    uint16_t frequency;
    uint16_t duration_ms;
};

struct EmergencyStopEvent {
    uint8_t reason_code;
};

struct RuntimeHealthEvent {
    bool is_healthy;
    uint32_t uptime_ms;
};

// Generic Event Wrapper for Queueing
struct RuntimeEvent {
    EventType type;
    union {
        MotorCommandEvent motor;
        ServoCommandEvent servo;
        OLEDCommandEvent oled;
        RGBCommandEvent rgb;
        BuzzerCommandEvent buzzer;
        EmergencyStopEvent estop;
        RuntimeHealthEvent health;
    } payload;
};

} // namespace Runtime
} // namespace ReconRover
