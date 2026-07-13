/**
 * @file motor_manager.h
 * @brief Recon Rover V1 - Motor Manager
 *
 * Manages the L298N motor driver, applies speed limits, and 
 * provides a safe high-level interface for differential drive.
 */

#ifndef ROVER_MOTOR_MANAGER_H
#define ROVER_MOTOR_MANAGER_H

#include "driver_l298n.h"
#include "configuration_manager.h"
#include "error_system.h"

namespace rover {

/**
 * @class MotorManager
 * @brief Plain C++ class that owns and orchestrates the motor driver.
 */
class MotorManager {
public:
    /**
     * @brief Constructs the manager.
     * @param driver Pointer to the initialized L298N driver.
     * @param config Pointer to the configuration manager.
     */
    MotorManager(driver::DriverL298N* driver, ConfigurationManager* config);

    /**
     * @brief Initializes the motor hardware.
     */
    void init();

    /**
     * @brief Sets the speed for both tracks.
     * @param left_speed Speed from -1.0 to 1.0.
     * @param right_speed Speed from -1.0 to 1.0.
     */
    void setSpeed(float left_speed, float right_speed);

    /**
     * @brief Coasts the motors to a stop.
     */
    void stop();

    /**
     * @brief Actively brakes the motors.
     */
    void emergencyStop();

private:
    driver::DriverL298N* m_driver;
    ConfigurationManager* m_config;
};

} // namespace rover

#endif // ROVER_MOTOR_MANAGER_H
