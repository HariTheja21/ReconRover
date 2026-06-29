/**
 * @file health_manager.cpp
 * @brief Recon Rover V1 - Health Manager
 */

#include "health_manager.h"

namespace rover {

HealthManager::HealthManager() {
    init();
}

void HealthManager::init() {
    m_system_health = {};
    m_system_health.safe_mode_active = false;
}

void HealthManager::updateHealth(const SensorHealth& sensors, const PowerHealth& power, 
                                 const CommunicationHealth& comms, uint32_t uptime_ms, 
                                 uint32_t free_heap) {
    m_system_health.sensors = sensors;
    m_system_health.power = power;
    m_system_health.comms = comms;
    m_system_health.uptime_ms = uptime_ms;
    m_system_health.free_heap_bytes = free_heap;
}

const SystemHealth& HealthManager::getSystemHealth() const {
    return m_system_health;
}

void HealthManager::setSafeModeActive(bool active) {
    m_system_health.safe_mode_active = active;
}

} // namespace rover
