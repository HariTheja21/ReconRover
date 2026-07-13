/**
 * @file servo_manager.h
 * @brief Recon Rover V1 - Servo Manager
 *
 * Manages the Pan/Tilt servo drivers.
 */

#ifndef ROVER_SERVO_MANAGER_H
#define ROVER_SERVO_MANAGER_H

#include "driver_servo.h"

namespace rover {

/**
 * @class ServoManager
 * @brief Plain C++ class that owns and orchestrates the servo drivers.
 */
class ServoManager {
public:
    /**
     * @brief Constructs the manager.
     * @param pan_servo Pointer to the initialized pan servo driver.
     * @param tilt_servo Pointer to the initialized tilt servo driver.
     */
    ServoManager(driver::DriverServo* pan_servo, driver::DriverServo* tilt_servo);

    /**
     * @brief Initializes the servo hardware.
     */
    void init();

    /**
     * @brief Sets the pan angle.
     * @param angle_deg Angle in degrees (0-180).
     */
    void setPan(float angle_deg);

    /**
     * @brief Sets the tilt angle.
     * @param angle_deg Angle in degrees (0-180).
     */
    void setTilt(float angle_deg);

    /**
     * @brief Centers both servos at 90 degrees.
     */
    void center();

private:
    driver::DriverServo* m_pan;
    driver::DriverServo* m_tilt;
};

} // namespace rover

#endif // ROVER_SERVO_MANAGER_H
