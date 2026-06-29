/**
 * @file driver_ina219.h
 * @brief Recon Rover V1 - INA219 Power Monitor Driver
 *
 * Hardware driver for the INA219 current/power monitor.
 */

#ifndef ROVER_DRIVER_INA219_H
#define ROVER_DRIVER_INA219_H

#include <cstdint>
#include "hal_i2c.h"

namespace rover {
namespace driver {

/**
 * @brief Default I2C address for INA219 (A0/A1 to GND).
 */
constexpr uint8_t INA219_ADDR = 0x40;

/**
 * @class DriverIna219
 * @brief Driver class for the INA219 sensor.
 */
class DriverIna219 {
public:
    /**
     * @brief Constructs the driver.
     * @param i2c Pointer to an initialized HalI2c instance.
     */
    explicit DriverIna219(hal::HalI2c* i2c);

    /**
     * @brief Initializes the sensor and sets default calibration for 32V, 2A.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus init();

    /**
     * @brief Gets the shunt voltage in millivolts.
     * @param[out] voltage_mv Shunt voltage in mV.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus getShuntVoltage_mV(float& voltage_mv);

    /**
     * @brief Gets the bus voltage (load voltage) in volts.
     * @param[out] voltage_v Bus voltage in V.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus getBusVoltage_V(float& voltage_v);

    /**
     * @brief Gets the current flowing through the shunt in milliamperes.
     * @param[out] current_ma Current in mA.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus getCurrent_mA(float& current_ma);

    /**
     * @brief Gets the power being consumed in milliwatts.
     * @param[out] power_mw Power in mW.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus getPower_mW(float& power_mw);

private:
    hal::HalI2c* m_i2c; /**< Pointer to the I2C HAL */
    
    // Register Map
    static constexpr uint8_t REG_CONFIG = 0x00;
    static constexpr uint8_t REG_SHUNT_VOLTAGE = 0x01;
    static constexpr uint8_t REG_BUS_VOLTAGE = 0x02;
    static constexpr uint8_t REG_POWER = 0x03;
    static constexpr uint8_t REG_CURRENT = 0x04;
    static constexpr uint8_t REG_CALIBRATION = 0x05;

    // Calibration settings (Pre-calculated for 32V, 2A max, 0.1 ohm shunt)
    uint16_t m_calValue;
    uint32_t m_currentDivider_mA;
    float m_powerMultiplier_mW;

    /**
     * @brief Writes a 16-bit register.
     */
    hal::HalStatus writeRegister(uint8_t reg, uint16_t val);

    /**
     * @brief Reads a 16-bit register.
     */
    hal::HalStatus readRegister(uint8_t reg, uint16_t& val);
};

} // namespace driver
} // namespace rover

#endif // ROVER_DRIVER_INA219_H
