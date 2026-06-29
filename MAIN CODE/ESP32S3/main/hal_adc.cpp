/**
 * @file hal_adc.cpp
 * @brief Recon Rover V1 - ESP32 Hardware Abstraction Layer for ADC
 *
 * Implementation of the HalAdc class.
 */

#include "hal_adc.h"

namespace rover {
namespace hal {

HalAdc::HalAdc() 
    : m_handle(nullptr), m_cali_handle(nullptr), m_initialized(false), m_calibrated(false) {
}

HalAdc::~HalAdc() {
    if (m_initialized && m_handle != nullptr) {
        adc_oneshot_del_unit(m_handle);
    }
    if (m_calibrated && m_cali_handle != nullptr) {
        adc_cali_delete_scheme_curve_fitting(m_cali_handle);
    }
}

HalStatus HalAdc::init(const AdcConfig& config) {
    if (m_initialized) {
        return {HalError::ERR_ALREADY_INITIALIZED, ESP_OK};
    }

    m_unit = config.unit;
    m_channel = config.channel;

    adc_oneshot_unit_init_cfg_t init_config = {};
    init_config.unit_id = m_unit;
    init_config.clk_src = ADC_DIGI_CLK_SRC_DEFAULT;
    
    esp_err_t err = adc_oneshot_new_unit(&init_config, &m_handle);
    if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }
    
    adc_oneshot_chan_cfg_t chan_config = {};
    chan_config.bitwidth = config.width;
    chan_config.atten = config.atten;

    err = adc_oneshot_config_channel(m_handle, m_channel, &chan_config);
    if (err != ESP_OK) {
        adc_oneshot_del_unit(m_handle);
        return {HalError::ERR_HARDWARE, err};
    }

    // Attempt to set up calibration (specifically Curve Fitting for ESP32-S3)
    adc_cali_curve_fitting_config_t cali_config = {};
    cali_config.unit_id = m_unit;
    cali_config.chan = m_channel;
    cali_config.atten = config.atten;
    cali_config.bitwidth = config.width;
    
    err = adc_cali_create_scheme_curve_fitting(&cali_config, &m_cali_handle);
    if (err == ESP_OK) {
        m_calibrated = true;
    } else {
        m_calibrated = false;
        // Not a critical failure, calibration might not be burnt into eFuse
    }

    m_initialized = true;
    return {HalError::OK, ESP_OK};
}

HalStatus HalAdc::readRaw(int& out_raw) {
    if (!m_initialized) {
        return {HalError::ERR_NOT_INITIALIZED, ESP_OK};
    }

    esp_err_t err = adc_oneshot_read(m_handle, m_channel, &out_raw);
    if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }

    return {HalError::OK, ESP_OK};
}

HalStatus HalAdc::readMilliVolts(int& out_mv) {
    if (!m_initialized) {
        return {HalError::ERR_NOT_INITIALIZED, ESP_OK};
    }

    int raw_val = 0;
    HalStatus status = readRaw(raw_val);
    if (!status.isOk()) {
        return status;
    }

    if (m_calibrated) {
        esp_err_t err = adc_cali_raw_to_voltage(m_cali_handle, raw_val, &out_mv);
        if (err != ESP_OK) {
            return {HalError::ERR_HARDWARE, err};
        }
    } else {
        // Fallback if not calibrated, though inaccurate
        return {HalError::ERR_NOT_SUPPORTED, ESP_OK};
    }

    return {HalError::OK, ESP_OK};
}

} // namespace hal
} // namespace rover
