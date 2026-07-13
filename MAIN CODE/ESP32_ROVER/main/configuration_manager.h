/**
 * @file configuration_manager.h
 * @brief Recon Rover V1 - Configuration Manager
 *
 * Provides runtime access to system configuration and limits, 
 * abstracting the static config.h variables.
 */

#ifndef ROVER_CONFIGURATION_MANAGER_H
#define ROVER_CONFIGURATION_MANAGER_H

#include "config.h"
#include "error_system.h"
#include <cstdint>

namespace rover {

/**
 * @class ConfigurationManager
 * @brief Manages system configuration and threshold validation.
 */
class ConfigurationManager {
public:
    ConfigurationManager();
    
    /**
     * @brief Initializes the configuration manager.
     */
    void init();

    /**
     * @brief Gets the maximum allowed motor speed.
     * @return Speed factor from 0.0 to 1.0.
     */
    float getMaxMotorSpeed() const;

    /**
     * @brief Sets a runtime limit on motor speed.
     * @param speed Speed factor from 0.0 to 1.0.
     */
    void setMaxMotorSpeed(float speed);

    /**
     * @brief Validates if a gas voltage reading is hazardous based on config.
     * @param voltage_mv The reading in millivolts.
     * @return True if hazardous.
     */
    bool isGasHazardous(int32_t voltage_mv) const;

    /**
     * @brief Validates if the battery voltage is critically low.
     * @param voltage_v The reading in volts.
     * @return True if battery is low.
     */
    bool isBatteryLow(float voltage_v) const;

private:
    float m_runtime_max_motor_speed;
};

} // namespace rover

#endif // ROVER_CONFIGURATION_MANAGER_H
