/**
 * @file hal_i2c.h
 * @brief Recon Rover V1 - ESP32 Hardware Abstraction Layer for I2C
 *
 * Provides a clean C++ interface for ESP32 I2C Master configuration and communication.
 * Wraps the legacy I2C driver (driver/i2c.h) compatible with ESP-IDF v5.
 */

#ifndef ROVER_HAL_I2C_H
#define ROVER_HAL_I2C_H

#include <cstdint>
#include <vector>
#include "hal_types.h"
#include "driver/i2c.h"
#include "driver/gpio.h"

namespace rover {
namespace hal {

/**
 * @struct I2cConfig
 * @brief Configuration parameters for I2C initialization.
 */
struct I2cConfig {
    i2c_port_t port;        /**< I2C port number (e.g., I2C_NUM_0) */
    gpio_num_t sda_pin;     /**< GPIO pin for SDA */
    gpio_num_t scl_pin;     /**< GPIO pin for SCL */
    uint32_t frequency_hz;  /**< I2C clock frequency in Hz */
    bool pullup_enable;     /**< True to enable internal pullups */
};

/**
 * @class HalI2c
 * @brief Hardware Abstraction Layer for an I2C master bus.
 *
 * Manages bus initialization, read/write operations, and device scanning.
 */
class HalI2c {
public:
    /**
     * @brief Constructs an uninitialized I2C HAL object.
     */
    HalI2c();

    /**
     * @brief Destructor. Deletes the I2C driver if initialized.
     */
    ~HalI2c();

    /**
     * @brief Initializes the I2C master bus with the given configuration.
     * @param config The I2C configuration parameters.
     * @return HalStatus indicating success or failure.
     */
    HalStatus init(const I2cConfig& config);

    /**
     * @brief Writes data to an I2C slave device.
     * @param dev_addr 7-bit device address.
     * @param data Pointer to the data buffer to write.
     * @param length Number of bytes to write.
     * @param timeout_ms Maximum time to wait for the transaction to complete.
     * @return HalStatus indicating success or failure.
     */
    HalStatus write(uint8_t dev_addr, const uint8_t* data, size_t length, uint32_t timeout_ms = 100);

    /**
     * @brief Reads data from an I2C slave device.
     * @param dev_addr 7-bit device address.
     * @param[out] data Pointer to the buffer where read data will be stored.
     * @param length Number of bytes to read.
     * @param timeout_ms Maximum time to wait for the transaction to complete.
     * @return HalStatus indicating success or failure.
     */
    HalStatus read(uint8_t dev_addr, uint8_t* data, size_t length, uint32_t timeout_ms = 100);

    /**
     * @brief Writes data to a slave, issues a repeated start, and then reads data.
     * Commonly used for reading from specific device registers.
     * @param dev_addr 7-bit device address.
     * @param write_data Pointer to the data to write (usually register address).
     * @param write_length Number of bytes to write.
     * @param[out] read_data Pointer to the buffer for read data.
     * @param read_length Number of bytes to read.
     * @param timeout_ms Maximum time to wait.
     * @return HalStatus indicating success or failure.
     */
    HalStatus writeRead(uint8_t dev_addr, const uint8_t* write_data, size_t write_length, uint8_t* read_data, size_t read_length, uint32_t timeout_ms = 100);

    /**
     * @brief Scans the I2C bus for active devices.
     * @param[out] found_addresses Vector to store the 7-bit addresses of found devices.
     * @return HalStatus indicating success or failure.
     */
    HalStatus scanBus(std::vector<uint8_t>& found_addresses);

private:
    i2c_port_t m_port;      /**< The I2C port used by this instance */
    bool m_initialized;     /**< Tracks if the bus has been initialized */
};

} // namespace hal
} // namespace rover

#endif // ROVER_HAL_I2C_H
