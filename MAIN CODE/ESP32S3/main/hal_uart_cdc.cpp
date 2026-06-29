/**
 * @file hal_uart_cdc.cpp
 * @brief Recon Rover V1 - ESP32 Hardware Abstraction Layer for USB CDC UART
 *
 * Implementation of the HalUartCdc class.
 */

#include "hal_uart_cdc.h"
#include <cstring>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

namespace rover {
namespace hal {

HalUartCdc::HalUartCdc() : m_initialized(false) {
}

HalUartCdc::~HalUartCdc() {
    if (m_initialized) {
        // Driver uninstallation is not typically required/supported for usb_serial_jtag 
        // in standard operation, but could be added if esp-idf provides it.
    }
}

HalStatus HalUartCdc::init(size_t rx_buffer_size, size_t tx_buffer_size) {
    if (m_initialized) {
        return {HalError::ERR_ALREADY_INITIALIZED, ESP_OK};
    }

    usb_serial_jtag_driver_config_t config = {};
    config.tx_buffer_size = tx_buffer_size;
    config.rx_buffer_size = rx_buffer_size;

    esp_err_t err = usb_serial_jtag_driver_install(&config);
    if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }

    m_initialized = true;
    m_rx_line_buf.reserve(256); // Reserve enough for typical command packet
    return {HalError::OK, ESP_OK};
}

HalStatus HalUartCdc::write(const uint8_t* data, size_t length) {
    if (!m_initialized) {
        return {HalError::ERR_NOT_INITIALIZED, ESP_OK};
    }
    if (data == nullptr || length == 0) {
        return {HalError::ERR_INVALID_ARG, ESP_OK};
    }

    int bytes_written = usb_serial_jtag_write_bytes(data, length, 50 / portTICK_PERIOD_MS);
    if (bytes_written < 0) {
        return {HalError::ERR_HARDWARE, ESP_FAIL};
    }
    
    // We can also trigger a push to host if needed, but hardware buffers usually handle it.
    
    return {HalError::OK, ESP_OK};
}

HalStatus HalUartCdc::read(uint8_t* buffer, size_t buffer_size, size_t& bytes_read) {
    bytes_read = 0;
    if (!m_initialized) {
        return {HalError::ERR_NOT_INITIALIZED, ESP_OK};
    }
    if (buffer == nullptr || buffer_size == 0) {
        return {HalError::ERR_INVALID_ARG, ESP_OK};
    }

    int read_len = usb_serial_jtag_read_bytes(buffer, buffer_size, 0); // Non-blocking
    if (read_len < 0) {
        return {HalError::ERR_HARDWARE, ESP_FAIL};
    }

    bytes_read = static_cast<size_t>(read_len);
    return {HalError::OK, ESP_OK};
}

HalStatus HalUartCdc::writeLine(const char* line) {
    if (!m_initialized) {
        return {HalError::ERR_NOT_INITIALIZED, ESP_OK};
    }
    if (line == nullptr) {
        return {HalError::ERR_INVALID_ARG, ESP_OK};
    }

    size_t len = std::strlen(line);
    HalStatus st = write(reinterpret_cast<const uint8_t*>(line), len);
    if (!st.isOk()) {
        return st;
    }

    const uint8_t newline = '\n';
    return write(&newline, 1);
}

HalStatus HalUartCdc::readLine(char* line_buffer, size_t max_length, bool& line_ready) {
    line_ready = false;
    if (!m_initialized) {
        return {HalError::ERR_NOT_INITIALIZED, ESP_OK};
    }
    if (line_buffer == nullptr || max_length == 0) {
        return {HalError::ERR_INVALID_ARG, ESP_OK};
    }

    uint8_t temp_buf[64];
    size_t bytes_read = 0;

    // Read available bytes into the internal string buffer
    HalStatus st = read(temp_buf, sizeof(temp_buf), bytes_read);
    if (!st.isOk()) {
        return st;
    }

    if (bytes_read > 0) {
        m_rx_line_buf.append(reinterpret_cast<const char*>(temp_buf), bytes_read);
    }

    // Check if we have a newline
    size_t pos = m_rx_line_buf.find('\n');
    if (pos != std::string::npos) {
        // We have a full line. Ensure it fits in the user's buffer.
        size_t copy_len = pos; // Doesn't include the newline
        if (copy_len >= max_length) {
            copy_len = max_length - 1; // Truncate to fit
        }

        std::memcpy(line_buffer, m_rx_line_buf.data(), copy_len);
        line_buffer[copy_len] = '\0';
        line_ready = true;

        // Erase the extracted line from the internal buffer
        m_rx_line_buf.erase(0, pos + 1);
    }

    // Prevent internal buffer from growing infinitely on garbage data
    if (m_rx_line_buf.size() > max_length * 2) {
        m_rx_line_buf.clear(); // Drop everything to recover
    }

    return {HalError::OK, ESP_OK};
}

} // namespace hal
} // namespace rover
