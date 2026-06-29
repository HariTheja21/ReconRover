/**
 * @file configuration_manager.cpp
 * @brief Recon Rover V1 - Configuration Manager
 */

#include "configuration_manager.h"
#include "utils.h"

namespace rover {

ConfigurationManager::ConfigurationManager() 
    : m_runtime_max_motor_speed(1.0f) {
}

void ConfigurationManager::init() {
    m_runtime_max_motor_speed = 1.0f;
}

float ConfigurationManager::getMaxMotorSpeed() const {
    return m_runtime_max_motor_speed;
}

void ConfigurationManager::setMaxMotorSpeed(float speed) {
    m_runtime_max_motor_speed = utils::constrainFloat(speed, 0.0f, 1.0f);
}

bool ConfigurationManager::isGasHazardous(int32_t voltage_mv) const {
    return voltage_mv >= config::MQ2_HAZARD_THRESHOLD_MV;
}

bool ConfigurationManager::isBatteryLow(float voltage_v) const {
    return voltage_v <= config::INA219_MIN_BUS_VOLTAGE_V;
}

} // namespace rover
