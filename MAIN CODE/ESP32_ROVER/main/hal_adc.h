/**
 * @file hal_adc.h
 * @brief Recon Rover V1 - ESP32 Hardware Abstraction Layer for ADC
 *
 * Provides a clean C++ interface for ESP32 ADC oneshot reads, using the v5 driver.
 */

#ifndef ROVER_HAL_ADC_H
#define ROVER_HAL_ADC_H

#include <cstdint>
#include "hal_types.h"
#include "esp_adc/adc_oneshot.h"
#include "esp_adc/adc_cali.h"
#include "esp_adc/adc_cali_scheme.h"

namespace rover {
namespace hal {

/**
 * @struct AdcConfig
 * @brief Configuration for initializing an ADC channel.
 */
struct AdcConfig {
    adc_unit_t unit;        /**< ADC unit (e.g., ADC_UNIT_1) */
    adc_channel_t channel;  /**< ADC channel */
    adc_atten_t atten;      /**< Attenuation level */
    adc_bitwidth_t width;   /**< Bit capture width */
};

/**
 * @class HalAdc
 * @brief Hardware Abstraction Layer for the ESP32 ADC.
 *
 * Supports oneshot raw reading and calibrated voltage conversion.
 */
class HalAdc {
public:
    /**
     * @brief Constructs an uninitialized ADC object.
     */
    HalAdc();

    /**
     * @brief Destructor. Frees the ADC handle and calibration profiles.
     */
    ~HalAdc();

    /**
     * @brief Initializes the ADC channel with given configuration.
     * @param config The ADC configuration.
     * @return HalStatus indicating success or failure.
     */
    HalStatus init(const AdcConfig& config);

    /**
     * @brief Reads a single raw value from the configured ADC channel.
     * @param[out] out_raw The variable to store the raw ADC counts.
     * @return HalStatus indicating success or failure.
     */
    HalStatus readRaw(int& out_raw);

    /**
     * @brief Reads the ADC and converts the value to calibrated millivolts.
     * @param[out] out_mv The variable to store the calibrated voltage in mV.
     * @return HalStatus indicating success or failure.
     */
    HalStatus readMilliVolts(int& out_mv);

private:
    adc_oneshot_unit_handle_t m_handle;     /**< Oneshot ADC handle */
    adc_cali_handle_t m_cali_handle;        /**< Calibration profile handle */
    bool m_initialized;                     /**< True if oneshot ADC is active */
    bool m_calibrated;                      /**< True if calibration profile is created */
    
    adc_unit_t m_unit;
    adc_channel_t m_channel;
};

} // namespace hal
} // namespace rover

#endif // ROVER_HAL_ADC_H
