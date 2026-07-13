/**
 * @file driver_pca9548a.h
 * @brief Recon Rover V1 - PCA9548A I2C Multiplexer Driver
 *
 * Hardware driver for the PCA9548A 8-channel I2C multiplexer.
 */

#ifndef ROVER_DRIVER_PCA9548A_H
#define ROVER_DRIVER_PCA9548A_H

#include <cstdint>
#include <vector>
#include "hal_i2c.h"

namespace rover {
namespace driver {

/**
 * @brief Default I2C address for PCA9548A.
 */
constexpr uint8_t PCA9548A_ADDR = 0x70;

/**
 * @class DriverPca9548a
 * @brief Driver class for the PCA9548A I2C Multiplexer.
 */
class DriverPca9548a {
public:
    /**
     * @brief Constructs the driver.
     * @param i2c Pointer to an initialized HalI2c instance.
     */
    explicit DriverPca9548a(hal::HalI2c* i2c);

    /**
     * @brief Initializes the multiplexer (verifies presence and disables all channels).
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus init();

    /**
     * @brief Selects a specific downstream I2C channel.
     * @param channel Channel index (0 to 7).
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus selectChannel(uint8_t channel);

    /**
     * @brief Disables all downstream I2C channels.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus disableAllChannels();

    /**
     * @brief Scans a specific downstream channel for devices.
     * @param channel Channel index (0 to 7).
     * @param[out] found_addresses Vector to store the addresses found on this channel.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus scanChannel(uint8_t channel, std::vector<uint8_t>& found_addresses);

    /**
     * @brief Verifies the multiplexer hardware is reachable.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus checkHealth();

private:
    hal::HalI2c* m_i2c; /**< Pointer to the I2C HAL */
};

} // namespace driver
} // namespace rover

#endif // ROVER_DRIVER_PCA9548A_H
