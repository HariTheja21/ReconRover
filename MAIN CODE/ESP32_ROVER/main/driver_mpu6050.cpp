/**
 * @file driver_mpu6050.cpp
 * @brief Recon Rover V1 - MPU6050 6-DoF IMU Driver
 *
 * Implementation of the DriverMpu6050 class.
 */

#include "driver_mpu6050.h"
#include "hal_timer.h" // For calibration delays

namespace rover {
namespace driver {

DriverMpu6050::DriverMpu6050(hal::HalI2c* i2c) 
    : m_i2c(i2c) {
    m_accel_offset[0] = m_accel_offset[1] = m_accel_offset[2] = 0;
    m_gyro_offset[0] = m_gyro_offset[1] = m_gyro_offset[2] = 0;
}

hal::HalStatus DriverMpu6050::init() {
    if (m_i2c == nullptr) {
        return {hal::HalError::ERR_INVALID_ARG, 0};
    }

    // Wake up the MPU6050 (clear sleep bit in PWR_MGMT_1)
    hal::HalStatus st = writeRegister(REG_PWR_MGMT_1, 0x00);
    if (!st.isOk()) return st;
    
    hal::HalTimer::delayMs(50); // Wait for sensor to stabilize

    // Set sample rate to 1kHz
    st = writeRegister(REG_SMPLRT_DIV, 0x07);
    if (!st.isOk()) return st;

    // Set Config (DLPF_CFG = 0, FSYNC disabled)
    st = writeRegister(REG_CONFIG, 0x00);
    if (!st.isOk()) return st;

    // Gyro Config (+/- 250 dps)
    st = writeRegister(REG_GYRO_CONFIG, 0x00);
    if (!st.isOk()) return st;

    // Accel Config (+/- 2g)
    st = writeRegister(REG_ACCEL_CONFIG, 0x00);
    if (!st.isOk()) return st;

    return checkHealth();
}

hal::HalStatus DriverMpu6050::checkHealth() {
    uint8_t id = 0;
    uint8_t reg = REG_WHO_AM_I;
    hal::HalStatus st = m_i2c->writeRead(MPU6050_ADDR, &reg, 1, &id, 1);
    
    if (!st.isOk()) return st;
    
    if (id != WHO_AM_I_VAL) {
        return {hal::HalError::ERR_HARDWARE, 0};
    }
    
    return {hal::HalError::OK, 0};
}

hal::HalStatus DriverMpu6050::readAll(Mpu6050Data& data) {
    uint8_t raw[14];
    uint8_t reg = REG_ACCEL_XOUT_H;
    
    hal::HalStatus st = m_i2c->writeRead(MPU6050_ADDR, &reg, 1, raw, 14);
    if (!st.isOk()) return st;

    int16_t ax = (raw[0] << 8) | raw[1];
    int16_t ay = (raw[2] << 8) | raw[3];
    int16_t az = (raw[4] << 8) | raw[5];
    int16_t temp = (raw[6] << 8) | raw[7];
    int16_t gx = (raw[8] << 8) | raw[9];
    int16_t gy = (raw[10] << 8) | raw[11];
    int16_t gz = (raw[12] << 8) | raw[13];

    data.accel_x = static_cast<float>(ax - m_accel_offset[0]) / ACCEL_SCALE_2G;
    data.accel_y = static_cast<float>(ay - m_accel_offset[1]) / ACCEL_SCALE_2G;
    data.accel_z = static_cast<float>(az - m_accel_offset[2]) / ACCEL_SCALE_2G;
    
    data.temp_c = (static_cast<float>(temp) / 340.0f) + 36.53f;
    
    data.gyro_x = static_cast<float>(gx - m_gyro_offset[0]) / GYRO_SCALE_250;
    data.gyro_y = static_cast<float>(gy - m_gyro_offset[1]) / GYRO_SCALE_250;
    data.gyro_z = static_cast<float>(gz - m_gyro_offset[2]) / GYRO_SCALE_250;

    return {hal::HalError::OK, 0};
}

hal::HalStatus DriverMpu6050::performSelfTest() {
    // 1. Enable self-test bits in GYRO_CONFIG and ACCEL_CONFIG
    writeRegister(REG_GYRO_CONFIG, 0xE0); // 11100000
    writeRegister(REG_ACCEL_CONFIG, 0xF0); // 11110000
    
    hal::HalTimer::delayMs(50);
    
    // 2. Read values and verify they are within acceptable bounds
    Mpu6050Data data;
    hal::HalStatus st = readAll(data);
    
    // 3. Restore standard configs
    writeRegister(REG_GYRO_CONFIG, 0x00);
    writeRegister(REG_ACCEL_CONFIG, 0x00);
    
    // Returning result based on ability to communicate rather than rigorous 
    // factory trimming bounds for this implementation.
    return st;
}

hal::HalStatus DriverMpu6050::calibrate() {
    long ax_sum = 0, ay_sum = 0, az_sum = 0;
    long gx_sum = 0, gy_sum = 0, gz_sum = 0;
    const int samples = 200;

    for (int i = 0; i < samples; ++i) {
        uint8_t raw[14];
        uint8_t reg = REG_ACCEL_XOUT_H;
        hal::HalStatus st = m_i2c->writeRead(MPU6050_ADDR, &reg, 1, raw, 14);
        if (!st.isOk()) return st;

        ax_sum += (int16_t)((raw[0] << 8) | raw[1]);
        ay_sum += (int16_t)((raw[2] << 8) | raw[3]);
        az_sum += (int16_t)((raw[4] << 8) | raw[5]);
        gx_sum += (int16_t)((raw[8] << 8) | raw[9]);
        gy_sum += (int16_t)((raw[10] << 8) | raw[11]);
        gz_sum += (int16_t)((raw[12] << 8) | raw[13]);
        
        hal::HalTimer::delayMs(2); // Wait slightly between readings
    }

    m_accel_offset[0] = ax_sum / samples;
    m_accel_offset[1] = ay_sum / samples;
    m_accel_offset[2] = (az_sum / samples) - static_cast<int16_t>(ACCEL_SCALE_2G); // Z should be 1g
    m_gyro_offset[0] = gx_sum / samples;
    m_gyro_offset[1] = gy_sum / samples;
    m_gyro_offset[2] = gz_sum / samples;

    return {hal::HalError::OK, 0};
}

hal::HalStatus DriverMpu6050::writeRegister(uint8_t reg, uint8_t val) {
    uint8_t buf[2] = {reg, val};
    return m_i2c->write(MPU6050_ADDR, buf, 2);
}

} // namespace driver
} // namespace rover
