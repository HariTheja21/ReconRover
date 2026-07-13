/**
 * @file driver_mpu6050.h
 * @brief Recon Rover V1 - MPU6050 6-DoF IMU Driver
 *
 * Hardware driver for the MPU6050 Accelerometer and Gyroscope.
 * Uses the I2C HAL for communication.
 */

#ifndef ROVER_DRIVER_MPU6050_H
#define ROVER_DRIVER_MPU6050_H

#include <cstdint>
#include "hal_i2c.h"

namespace rover {
namespace driver {

/**
 * @brief Default I2C address for MPU6050 (AD0 low).
 */
constexpr uint8_t MPU6050_ADDR = 0x68;

/**
 * @struct Mpu6050Data
 * @brief Holds a complete reading from the MPU6050.
 */
struct Mpu6050Data {
    float accel_x; /**< Acceleration in X axis (g) */
    float accel_y; /**< Acceleration in Y axis (g) */
    float accel_z; /**< Acceleration in Z axis (g) */
    float gyro_x;  /**< Angular velocity around X axis (deg/s) */
    float gyro_y;  /**< Angular velocity around Y axis (deg/s) */
    float gyro_z;  /**< Angular velocity around Z axis (deg/s) */
    float temp_c;  /**< Temperature in degrees Celsius */
};

/**
 * @class DriverMpu6050
 * @brief Driver class for the MPU6050 IMU.
 */
class DriverMpu6050 {
public:
    /**
     * @brief Constructs the driver.
     * @param i2c Pointer to an initialized HalI2c instance.
     */
    explicit DriverMpu6050(hal::HalI2c* i2c);

    /**
     * @brief Initializes the MPU6050, waking it up and setting default ranges.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus init();

    /**
     * @brief Performs a WHO_AM_I check to verify hardware presence.
     * @return HalStatus OK if hardware matches expected ID.
     */
    hal::HalStatus checkHealth();

    /**
     * @brief Reads the accelerometer, gyroscope, and temperature in one transaction.
     * @param[out] data Structure to populate with the converted readings.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus readAll(Mpu6050Data& data);

    /**
     * @brief Executes the internal self-test routine.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus performSelfTest();

    /**
     * @brief Performs gyroscope and accelerometer offset calibration.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus calibrate();

private:
    hal::HalI2c* m_i2c; /**< Pointer to the I2C HAL */
    
    // Register Map
    static constexpr uint8_t REG_SMPLRT_DIV   = 0x19;
    static constexpr uint8_t REG_CONFIG       = 0x1A;
    static constexpr uint8_t REG_GYRO_CONFIG  = 0x1B;
    static constexpr uint8_t REG_ACCEL_CONFIG = 0x1C;
    static constexpr uint8_t REG_ACCEL_XOUT_H = 0x3B;
    static constexpr uint8_t REG_TEMP_OUT_H   = 0x41;
    static constexpr uint8_t REG_GYRO_XOUT_H  = 0x43;
    static constexpr uint8_t REG_PWR_MGMT_1   = 0x6B;
    static constexpr uint8_t REG_WHO_AM_I     = 0x75;

    // Constants
    static constexpr uint8_t WHO_AM_I_VAL     = 0x68;
    static constexpr float ACCEL_SCALE_2G     = 16384.0f;
    static constexpr float GYRO_SCALE_250     = 131.0f;
    
    // Calibration Offsets
    int16_t m_accel_offset[3];
    int16_t m_gyro_offset[3];

    /**
     * @brief Helper to write a single register.
     * @param reg Register address.
     * @param val Value to write.
     * @return HalStatus
     */
    hal::HalStatus writeRegister(uint8_t reg, uint8_t val);
};

} // namespace driver
} // namespace rover

#endif // ROVER_DRIVER_MPU6050_H
