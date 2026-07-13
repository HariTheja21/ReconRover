/**
 * @file servo_manager.cpp
 * @brief Recon Rover V1 - Servo Manager
 */

#include "servo_manager.h"

namespace rover {

ServoManager::ServoManager(driver::DriverServo* pan_servo, driver::DriverServo* tilt_servo)
    : m_pan(pan_servo), m_tilt(tilt_servo) {
}

void ServoManager::init() {
    if (m_pan) m_pan->init();
    if (m_tilt) m_tilt->init();
    center();
}

void ServoManager::setPan(float angle_deg) {
    if (m_pan) {
        m_pan->setAngle(angle_deg);
    }
}

void ServoManager::setTilt(float angle_deg) {
    if (m_tilt) {
        m_tilt->setAngle(angle_deg);
    }
}

void ServoManager::center() {
    setPan(90.0f);
    setTilt(90.0f);
}

} // namespace rover
