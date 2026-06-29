/**
 * @file telemetry_router.cpp
 * @brief Recon Rover V1 - Telemetry Router
 */

#include "telemetry_router.h"

namespace rover {
namespace comms {

void TelemetryRouter::processSensorEvent(const SensorEvent& event) {
    m_packet.timestamp_ms = event.data.imu.timestamp_ms; // Or another appropriate timestamp

    // If the event structure carried specific subsystem updates we'd map them here.
    // In Phase 2.3D, we packed all of them into the SensorEvent.
    m_packet.imu = event.data.imu;
    m_packet.tof = event.data.tof;
    m_packet.sonar = event.data.sonar;
    m_packet.gas = event.data.gas;
    m_packet.power = event.data.power;
}

void TelemetryRouter::processHealthEvent(const SystemHealth& health) {
    m_packet.state = health.safe_mode_active ? SystemState::SAFE_MODE : SystemState::ACTIVE;
    // active_faults mapping could go here based on health.
}

const TelemetryPacket& TelemetryRouter::getPacket() const {
    return m_packet;
}

} // namespace comms
} // namespace rover
