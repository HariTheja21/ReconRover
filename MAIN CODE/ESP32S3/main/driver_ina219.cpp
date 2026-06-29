/**
 * @file driver_ina219.cpp
 * @brief Recon Rover V1 - INA219 Power Monitor Driver
 *
 * Implementation of the DriverIna219 class.
 */

#include "driver_ina219.h"
#include "hal_timer.h"

namespace rover {
namespace driver {

DriverIna219::DriverIna219(hal::HalI2c* i2c) 
    : m_i2c(i2c), m_calValue(4096), m_currentDivider_mA(10), m_powerMultiplier_mW(2.0f) {
}

hal::HalStatus DriverIna219::init() {
    if (m_i2c == nullptr) {
        return {hal::HalError::ERR_INVALID_ARG, 0};
    }

    // Set Calibration register to '32V, 2A' range.
    hal::HalStatus st = writeRegister(REG_CALIBRATION, m_calValue);
    if (!st.isOk()) return st;

    // Set Config register to take into account the settings above
    uint16_t config = (0x01 << 13) | // Bus Voltage Range (32V)
                      (0x03 << 11) | // Gain (8, 320mV)
                      (0x03 << 7)  | // Bus ADC Resolution (12-bit)
                      (0x03 << 3)  | // Shunt ADC Resolution (12-bit)
                      (0x07);        // Operating Mode (Shunt and Bus Continuous)
                      
    return writeRegister(REG_CONFIG, config);
}

hal::HalStatus DriverIna219::getShuntVoltage_mV(float& voltage_mv) {
    uint16_t value = 0;
    hal::HalStatus st = readRegister(REG_SHUNT_VOLTAGE, value);
    if (!st.isOk()) return st;

    int16_t signed_value = static_cast<int16_t>(value);
    voltage_mv = signed_value * 0.01f;
    return {hal::HalError::OK, 0};
}

hal::HalStatus DriverIna219::getBusVoltage_V(float& voltage_v) {
    uint16_t value = 0;
    hal::HalStatus st = readRegister(REG_BUS_VOLTAGE, value);
    if (!st.isOk()) return st;

    // Shift to the right 3 to drop CNVR and OVF and multiply by LSB
    int16_t signed_value = static_cast<int16_t>((value >> 3) * 4);
    voltage_v = signed_value * 0.001f;
    return {hal::HalError::OK, 0};
}

hal::HalStatus DriverIna219::getCurrent_mA(float& current_ma) {
    // Sometimes a sharp load will reset the INA219, which will
    // reset the cal register, meaning CURRENT and POWER will
    // not be available... avoid this by always writing a cal
    // value even if it's an extra step.
    writeRegister(REG_CALIBRATION, m_calValue);

    uint16_t value = 0;
    hal::HalStatus st = readRegister(REG_CURRENT, value);
    if (!st.isOk()) return st;

    int16_t signed_value = static_cast<int16_t>(value);
    current_ma = static_cast<float>(signed_value) / static_cast<float>(m_currentDivider_mA);
    return {hal::HalError::OK, 0};
}

hal::HalStatus DriverIna219::getPower_mW(float& power_mw) {
    writeRegister(REG_CALIBRATION, m_calValue);

    uint16_t value = 0;
    hal::HalStatus st = readRegister(REG_POWER, value);
    if (!st.isOk()) return st;

    int16_t signed_value = static_cast<int16_t>(value);
    power_mw = static_cast<float>(signed_value) * m_powerMultiplier_mW;
    return {hal::HalError::OK, 0};
}

hal::HalStatus DriverIna219::writeRegister(uint8_t reg, uint16_t val) {
    uint8_t buf[3];
    buf[0] = reg;
    buf[1] = (val >> 8) & 0xFF; // MSB
    buf[2] = val & 0xFF;        // LSB
    return m_i2c->write(INA219_ADDR, buf, 3);
}

hal::HalStatus DriverIna219::readRegister(uint8_t reg, uint16_t& val) {
    uint8_t buf[2];
    hal::HalStatus st = m_i2c->writeRead(INA219_ADDR, &reg, 1, buf, 2);
    if (st.isOk()) {
        val = (buf[0] << 8) | buf[1];
    }
    return st;
}

} // namespace driver
} // namespace rover
