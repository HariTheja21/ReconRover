/**
 * @file driver_pca9548a.cpp
 * @brief Recon Rover V1 - PCA9548A I2C Multiplexer Driver
 *
 * Implementation of the DriverPca9548a class.
 */

#include "driver_pca9548a.h"

namespace rover {
namespace driver {

DriverPca9548a::DriverPca9548a(hal::HalI2c* i2c) : m_i2c(i2c) {
}

hal::HalStatus DriverPca9548a::init() {
    if (m_i2c == nullptr) {
        return {hal::HalError::ERR_INVALID_ARG, 0};
    }
    
    hal::HalStatus st = checkHealth();
    if (!st.isOk()) {
        return st;
    }

    return disableAllChannels();
}

hal::HalStatus DriverPca9548a::selectChannel(uint8_t channel) {
    if (channel > 7) {
        return {hal::HalError::ERR_INVALID_ARG, 0};
    }

    uint8_t ctrl_byte = (1 << channel);
    return m_i2c->write(PCA9548A_ADDR, &ctrl_byte, 1);
}

hal::HalStatus DriverPca9548a::disableAllChannels() {
    uint8_t ctrl_byte = 0x00;
    return m_i2c->write(PCA9548A_ADDR, &ctrl_byte, 1);
}

hal::HalStatus DriverPca9548a::scanChannel(uint8_t channel, std::vector<uint8_t>& found_addresses) {
    hal::HalStatus st = selectChannel(channel);
    if (!st.isOk()) {
        return st;
    }

    return m_i2c->scanBus(found_addresses);
}

hal::HalStatus DriverPca9548a::checkHealth() {
    // Attempting a 0-byte read or reading the register
    // The PCA9548A can be read to get the current selected channel
    uint8_t current_channel = 0;
    return m_i2c->read(PCA9548A_ADDR, &current_channel, 1);
}

} // namespace driver
} // namespace rover
