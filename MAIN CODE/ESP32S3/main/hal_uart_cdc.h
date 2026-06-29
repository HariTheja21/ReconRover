/**
 * @file hal_uart_cdc.h
 * @brief Recon Rover V1 - ESP32 Hardware Abstraction Layer for USB CDC UART
 *
 * Provides a clean C++ interface for ESP32-S3 native USB CDC UART communication.
 * Wraps the driver/usb_serial_jtag.h functionality.
 */

#ifndef ROVER_HAL_UART_CDC_H
#define ROVER_HAL_UART_CDC_H

#include <cstdint>
#include <string>
#include "hal_types.h"
#include "driver/usb_serial_jtag.h"

namespace rover {
namespace hal {

/**
 * @class HalUartCdc
 * @brief Hardware Abstraction Layer for the ESP32-S3 USB Serial/JTAG (CDC).
 *
 * Provides non-blocking read/write and line-buffered reads for JSON parsing.
 */
class HalUartCdc {
public:
    /**
     * @brief Constructs an uninitialized UART CDC object.
     */
    HalUartCdc();

    /**
     * @brief Destructor. Reverts the driver if initialized.
     */
    ~HalUartCdc();

    /**
     * @brief Initializes the USB CDC interface with TX/RX buffers.
     * @param rx_buffer_size Size of the internal RX ring buffer.
     * @param tx_buffer_size Size of the internal TX ring buffer.
     * @return HalStatus indicating success or failure.
     */
    HalStatus init(size_t rx_buffer_size = 1024, size_t tx_buffer_size = 1024);

    /**
     * @brief Writes a block of data to the CDC TX buffer.
     * @param data Pointer to the data.
     * @param length Number of bytes to write.
     * @return HalStatus indicating success or failure.
     */
    HalStatus write(const uint8_t* data, size_t length);

    /**
     * @brief Reads a block of data from the CDC RX buffer.
     * @param[out] buffer Pointer to the destination buffer.
     * @param buffer_size Maximum number of bytes to read.
     * @param[out] bytes_read Number of bytes actually read.
     * @return HalStatus indicating success or failure.
     */
    HalStatus read(uint8_t* buffer, size_t buffer_size, size_t& bytes_read);

    /**
     * @brief Writes a null-terminated string, automatically appending a newline.
     * @param line Null-terminated string.
     * @return HalStatus indicating success or failure.
     */
    HalStatus writeLine(const char* line);

    /**
     * @brief Reads from the RX buffer until a newline is found or the buffer is full.
     * @param[out] line_buffer Destination buffer for the string (will be null-terminated).
     * @param max_length Maximum length of the string, including null terminator.
     * @param[out] line_ready True if a complete newline-terminated string was read.
     * @return HalStatus indicating success or failure.
     */
    HalStatus readLine(char* line_buffer, size_t max_length, bool& line_ready);

private:
    bool m_initialized;         /**< Tracks initialization state */
    std::string m_rx_line_buf;  /**< Internal buffer for assembling lines */
};

} // namespace hal
} // namespace rover

#endif // ROVER_HAL_UART_CDC_H
