/**
 * @file driver_mq2.h
 * @brief Recon Rover V1 - MQ2 Gas Sensor Driver
 *
 * Hardware driver for the MQ2 analog gas sensor.
 * Uses the ADC HAL for reading raw counts and converted voltages.
 */

#ifndef ROVER_DRIVER_MQ2_H
#define ROVER_DRIVER_MQ2_H

#include <cstdint>
#include "hal_adc.h"

namespace rover {
namespace driver {

/**
 * @class DriverMq2
 * @brief Driver class for the MQ2 sensor.
 */
class DriverMq2 {
public:
    /**
     * @brief Constructs the driver.
     * @param adc Pointer to an initialized HalAdc instance.
     */
    explicit DriverMq2(hal::HalAdc* adc);

    /**
     * @brief Initializes the driver and performs baseline read if necessary.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus init();

    /**
     * @brief Reads the raw ADC counts from the sensor.
     * @param[out] raw_value Raw ADC integer.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus readRaw(int& raw_value);

    /**
     * @brief Reads the calibrated voltage from the sensor.
     * @param[out] voltage_mv Voltage in millivolts.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus readVoltage(int& voltage_mv);

    /**
     * @brief Checks if the reading exceeds the hazard threshold.
     * @param threshold_mv Voltage threshold in millivolts indicating hazard.
     * @param[out] is_hazardous True if threshold exceeded.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus isHazardDetected(int threshold_mv, bool& is_hazardous);

private:
    hal::HalAdc* m_adc; /**< Pointer to the ADC HAL */
};

} // namespace driver
} // namespace rover

#endif // ROVER_DRIVER_MQ2_H
