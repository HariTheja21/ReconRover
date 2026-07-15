#include "telemetry_encoder.h"

namespace ReconRover {
namespace Telemetry {

TelemetryEncoder::TelemetryEncoder(TelemetryStatistics& stats) : stats_(stats) {}

void TelemetryEncoder::EncodePayload(const TelemetryEvent& event, uint8_t* payload_buffer, uint8_t& payload_length) {
    switch(event.type) {
        case TelemetryType::HEARTBEAT:
            payload_buffer[0] = event.payload.heartbeat.uptime_s;
            payload_buffer[1] = 0x00; // Pad
            payload_buffer[2] = 0x00; // Pad
            payload_buffer[3] = 0x00; // Pad
            payload_length = 4;
            break;

        case TelemetryType::MOTOR_STATUS:
            payload_buffer[0] = (event.payload.motor.left_v >> 8) & 0xFF;
            payload_buffer[1] = event.payload.motor.left_v & 0xFF;
            payload_buffer[2] = (event.payload.motor.right_v >> 8) & 0xFF;
            payload_buffer[3] = event.payload.motor.right_v & 0xFF;
            payload_length = 4;
            break;

        case TelemetryType::BATTERY_STATUS:
            payload_buffer[0] = (event.payload.battery.voltage_mv >> 8) & 0xFF;
            payload_buffer[1] = event.payload.battery.voltage_mv & 0xFF;
            payload_buffer[2] = event.payload.battery.soc_pct;
            payload_buffer[3] = 0x00; // Pad
            payload_length = 4;
            break;

        // Add other cases here, capping at 4 bytes per payload matching Raspberry Pi 9-byte structure
        default:
            payload_buffer[0] = 0;
            payload_buffer[1] = 0;
            payload_buffer[2] = 0;
            payload_buffer[3] = 0;
            payload_length = 4;
            break;
    }
}

} // namespace Telemetry
} // namespace ReconRover
