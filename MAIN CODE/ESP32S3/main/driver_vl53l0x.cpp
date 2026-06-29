/**
 * @file driver_vl53l0x.cpp
 * @brief Recon Rover V1 - VL53L0X Time-of-Flight Sensor Driver
 *
 * Implementation of the DriverVl53l0x class.
 * Note: A full ST API port for VL53L0X is extremely large. 
 * This provides a heavily simplified register initialization suitable for 
 * basic default-range (1.2m) sensing.
 */

#include "driver_vl53l0x.h"
#include "hal_timer.h"

namespace rover {
namespace driver {

DriverVl53l0x::DriverVl53l0x(hal::HalI2c* i2c) : m_i2c(i2c) {
}

hal::HalStatus DriverVl53l0x::init() {
    if (m_i2c == nullptr) {
        return {hal::HalError::ERR_INVALID_ARG, 0};
    }

    // Delay to allow sensor boot
    hal::HalTimer::delayMs(20);

    hal::HalStatus st = checkHealth();
    if (!st.isOk()) return st;

    // A complete initialization requires uploading tuning settings.
    // For this driver, we implement the minimal sequence to take it out of standby.
    // (In production, integrating ST's official API or a full Pololu port is common).
    
    // Simplistic 'magic' init sequence
    writeReg(0x88, 0x00);
    writeReg(0x80, 0x01);
    writeReg(0xFF, 0x01);
    writeReg(0x00, 0x00);
    writeReg(0x91, 0x3C);
    writeReg(0x00, 0x01);
    writeReg(0xFF, 0x00);
    writeReg(0x80, 0x00);

    return {hal::HalError::OK, 0};
}

hal::HalStatus DriverVl53l0x::checkHealth() {
    uint8_t id = 0;
    hal::HalStatus st = readReg(REG_IDENTIFICATION_MODEL_ID, id);
    if (!st.isOk()) return st;

    if (id != 0xEE) {
        return {hal::HalError::ERR_HARDWARE, 0};
    }

    return {hal::HalError::OK, 0};
}

hal::HalStatus DriverVl53l0x::readRangeSingleMillimeters(uint16_t& distance_mm, uint32_t timeout_ms) {
    writeReg(0x80, 0x01);
    writeReg(0xFF, 0x01);
    writeReg(0x00, 0x00);
    writeReg(0x91, 0x3C);
    writeReg(0x00, 0x01);
    writeReg(0xFF, 0x00);
    writeReg(0x80, 0x00);

    // Trigger measurement (0x01 = single shot)
    writeReg(REG_SYSRANGE_START, 0x01);

    // Wait for completion
    uint32_t start = hal::HalTimer::getMillis();
    while (true) {
        uint8_t status = 0;
        readReg(REG_RESULT_RANGE_STATUS, status);
        
        if ((status & 0x01) == 0x01) {
            break; // Ready
        }

        if (hal::HalTimer::getMillis() - start > timeout_ms) {
            return {hal::HalError::ERR_TIMEOUT, 0};
        }
        
        hal::HalTimer::delayMs(5);
    }

    // Read 2 bytes of range (registers 0x14 to 0x1B contain various results, 0x1E is distance)
    uint8_t reg = 0x1E;
    uint8_t data[2];
    hal::HalStatus st = m_i2c->writeRead(VL53L0X_ADDR, &reg, 1, data, 2);
    if (!st.isOk()) return st;

    distance_mm = (data[0] << 8) | data[1];

    // Clear interrupt
    writeReg(0x0B, 0x01);

    return {hal::HalError::OK, 0};
}

hal::HalStatus DriverVl53l0x::startContinuous() {
    // 0x02 = back-to-back mode
    return writeReg(REG_SYSRANGE_START, 0x02);
}

hal::HalStatus DriverVl53l0x::stopContinuous() {
    return writeReg(REG_SYSRANGE_START, 0x01); // Standard fallback
}

hal::HalStatus DriverVl53l0x::readRangeContinuousMillimeters(uint16_t& distance_mm, uint32_t timeout_ms) {
    uint32_t start = hal::HalTimer::getMillis();
    while (true) {
        uint8_t status = 0;
        readReg(REG_RESULT_RANGE_STATUS, status);
        
        if ((status & 0x01) == 0x01) {
            break; // Ready
        }

        if (hal::HalTimer::getMillis() - start > timeout_ms) {
            return {hal::HalError::ERR_TIMEOUT, 0};
        }
        
        hal::HalTimer::delayMs(5);
    }

    uint8_t reg = 0x1E;
    uint8_t data[2];
    hal::HalStatus st = m_i2c->writeRead(VL53L0X_ADDR, &reg, 1, data, 2);
    if (!st.isOk()) return st;

    distance_mm = (data[0] << 8) | data[1];

    // Clear interrupt
    writeReg(0x0B, 0x01);

    return {hal::HalError::OK, 0};
}

hal::HalStatus DriverVl53l0x::writeReg(uint8_t reg, uint8_t val) {
    uint8_t buf[2] = {reg, val};
    return m_i2c->write(VL53L0X_ADDR, buf, 2);
}

hal::HalStatus DriverVl53l0x::readReg(uint8_t reg, uint8_t& val) {
    return m_i2c->writeRead(VL53L0X_ADDR, &reg, 1, &val, 1);
}

} // namespace driver
} // namespace rover
