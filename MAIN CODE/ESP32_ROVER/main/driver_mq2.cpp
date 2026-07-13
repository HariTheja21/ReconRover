/**
 * @file driver_mq2.cpp
 * @brief Recon Rover V1 - MQ2 Gas Sensor Driver
 *
 * Implementation of the DriverMq2 class.
 */

#include "driver_mq2.h"

namespace rover {
namespace driver {

DriverMq2::DriverMq2(hal::HalAdc* adc) : m_adc(adc) {
}

hal::HalStatus DriverMq2::init() {
    if (m_adc == nullptr) {
        return {hal::HalError::ERR_INVALID_ARG, 0};
    }
    // HalAdc should be pre-initialized by the owner before passing here.
    return {hal::HalError::OK, 0};
}

hal::HalStatus DriverMq2::readRaw(int& raw_value) {
    return m_adc->readRaw(raw_value);
}

hal::HalStatus DriverMq2::readVoltage(int& voltage_mv) {
    return m_adc->readMilliVolts(voltage_mv);
}

hal::HalStatus DriverMq2::isHazardDetected(int threshold_mv, bool& is_hazardous) {
    int current_mv = 0;
    hal::HalStatus st = readVoltage(current_mv);
    if (!st.isOk()) {
        is_hazardous = false;
        return st;
    }

    is_hazardous = (current_mv >= threshold_mv);
    return {hal::HalError::OK, 0};
}

} // namespace driver
} // namespace rover
