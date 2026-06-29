/**
 * @file types_sensor.h
 * @brief Recon Rover V1 - Common Sensor Data Types
 *
 * Defines the standardized structures for passing sensor data
 * between the drivers, managers, and telemetry builder.
 */

#ifndef ROVER_TYPES_SENSOR_H
#define ROVER_TYPES_SENSOR_H

#include <cstdint>

namespace rover {

/**
 * @struct IMUData
 * @brief Holds 6-DoF IMU readings and temperature.
 */
struct IMUData {
    float accel_x_g;    /**< Acceleration X-axis (g) */
    float accel_y_g;    /**< Acceleration Y-axis (g) */
    float accel_z_g;    /**< Acceleration Z-axis (g) */
    float gyro_x_dps;   /**< Angular velocity X-axis (deg/s) */
    float gyro_y_dps;   /**< Angular velocity Y-axis (deg/s) */
    float gyro_z_dps;   /**< Angular velocity Z-axis (deg/s) */
    float temp_c;       /**< Temperature (Celsius) */
};

/**
 * @struct ToFData
 * @brief Holds Time-of-Flight distance measurement.
 */
struct ToFData {
    uint16_t distance_mm; /**< Measured distance in millimeters */
    bool valid;           /**< True if measurement is valid and not timed out */
};

/**
 * @struct UltrasonicData
 * @brief Holds ultrasonic distance measurement.
 */
struct UltrasonicData {
    float distance_cm;    /**< Measured distance in centimeters */
    bool valid;           /**< True if measurement is valid and not timed out */
};

/**
 * @struct GasData
 * @brief Holds MQ2 gas sensor readings.
 */
struct GasData {
    int32_t raw_adc;      /**< Raw ADC counts */
    int32_t voltage_mv;   /**< Calibrated voltage in millivolts */
    bool hazard_detected; /**< True if voltage exceeds hazard threshold */
};

/**
 * @struct PowerData
 * @brief Holds INA219 power monitoring readings.
 */
struct PowerData {
    float bus_voltage_v;  /**< Battery/bus voltage in volts */
    float shunt_mv;       /**< Shunt voltage in millivolts */
    float current_ma;     /**< Load current in milliamperes */
    float power_mw;       /**< Power consumption in milliwatts */
};

} // namespace rover

#endif // ROVER_TYPES_SENSOR_H
