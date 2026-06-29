/**
 * @file driver_vl53l0x.h
 * @brief Recon Rover V1 - VL53L0X Time-of-Flight Sensor Driver
 *
 * Hardware driver for the VL53L0X. Assumes connection via PCA9548A multiplexer.
 */

#ifndef ROVER_DRIVER_VL53L0X_H
#define ROVER_DRIVER_VL53L0X_H

#include <cstdint>
#include "hal_i2c.h"

namespace rover {
namespace driver {

/**
 * @brief Default I2C address for VL53L0X.
 */
constexpr uint8_t VL53L0X_ADDR = 0x29;

/**
 * @class DriverVl53l0x
 * @brief Driver class for the VL53L0X ToF sensor.
 */
class DriverVl53l0x {
public:
    /**
     * @brief Constructs the driver.
     * @param i2c Pointer to an initialized HalI2c instance.
     */
    explicit DriverVl53l0x(hal::HalI2c* i2c);

    /**
     * @brief Initializes the sensor (basic config, calibration, default profile).
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus init();

    /**
     * @brief Triggers a single-shot measurement and blocks until result is ready.
     * @param[out] distance_mm Measured distance in millimeters.
     * @param timeout_ms Maximum time to wait for measurement completion.
     * @return HalStatus indicating success (OK) or failure (ERR_TIMEOUT).
     */
    hal::HalStatus readRangeSingleMillimeters(uint16_t& distance_mm, uint32_t timeout_ms = 500);

    /**
     * @brief Starts continuous measurement mode.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus startContinuous();

    /**
     * @brief Stops continuous measurement mode.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus stopContinuous();

    /**
     * @brief Reads the latest measurement in continuous mode (non-blocking if ready, else blocks up to timeout).
     * @param[out] distance_mm Measured distance in millimeters.
     * @param timeout_ms Maximum time to wait.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus readRangeContinuousMillimeters(uint16_t& distance_mm, uint32_t timeout_ms = 500);

    /**
     * @brief Performs a WHO_AM_I check.
     * @return HalStatus indicating success (OK) or hardware fault.
     */
    hal::HalStatus checkHealth();

private:
    hal::HalI2c* m_i2c; /**< Pointer to the I2C HAL */
    
    static constexpr uint8_t REG_SYSRANGE_START = 0x00;
    static constexpr uint8_t REG_RESULT_RANGE_STATUS = 0x14;
    static constexpr uint8_t REG_IDENTIFICATION_MODEL_ID = 0xC0;

    /**
     * @brief Helper to write an 8-bit register.
     */
    hal::HalStatus writeReg(uint8_t reg, uint8_t val);

    /**
     * @brief Helper to read an 8-bit register.
     */
    hal::HalStatus readReg(uint8_t reg, uint8_t& val);
};

} // namespace driver
} // namespace rover

#endif // ROVER_DRIVER_VL53L0X_H
