/**
 * @file motor_manager.cpp
 * @brief Recon Rover V1 - Motor Manager
 */

#include "motor_manager.h"
#include "utils.h"

namespace rover {

MotorManager::MotorManager(driver::DriverL298N* driver, ConfigurationManager* config)
    : m_driver(driver), m_config(config) {
}

void MotorManager::init() {
    if (m_driver) {
        m_driver->init();
        m_driver->stop();
    }
}

void MotorManager::setSpeed(float left_speed, float right_speed) {
    if (!m_driver) return;

    // Apply global speed limits from ConfigurationManager
    float max_speed = 1.0f;
    if (m_config) {
        max_speed = m_config->getMaxMotorSpeed();
    }

    left_speed = utils::constrainFloat(left_speed, -max_speed, max_speed);
    right_speed = utils::constrainFloat(right_speed, -max_speed, max_speed);

    m_driver->setLeftSpeed(left_speed);
    m_driver->setRightSpeed(right_speed);
}

void MotorManager::stop() {
    if (m_driver) {
        m_driver->stop();
    }
}

void MotorManager::emergencyStop() {
    if (m_driver) {
        m_driver->brake();
    }
}

} // namespace rover
