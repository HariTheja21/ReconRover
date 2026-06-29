/**
 * @file hal_i2c.cpp
 * @brief Recon Rover V1 - ESP32 Hardware Abstraction Layer for I2C
 *
 * Implementation of the HalI2c class.
 */

#include "hal_i2c.h"
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

namespace rover {
namespace hal {

HalI2c::HalI2c() : m_port(I2C_NUM_0), m_initialized(false) {
}

HalI2c::~HalI2c() {
    if (m_initialized) {
        i2c_driver_delete(m_port);
    }
}

HalStatus HalI2c::init(const I2cConfig& config) {
    if (m_initialized) {
        return {HalError::ERR_ALREADY_INITIALIZED, ESP_OK};
    }

    m_port = config.port;

    i2c_config_t conf = {};
    conf.mode = I2C_MODE_MASTER;
    conf.sda_io_num = config.sda_pin;
    conf.scl_io_num = config.scl_pin;
    conf.sda_pullup_en = config.pullup_enable ? GPIO_PULLUP_ENABLE : GPIO_PULLUP_DISABLE;
    conf.scl_pullup_en = config.pullup_enable ? GPIO_PULLUP_ENABLE : GPIO_PULLUP_DISABLE;
    conf.master.clk_speed = config.frequency_hz;
    conf.clk_flags = 0; // standard clock

    esp_err_t err = i2c_param_config(m_port, &conf);
    if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }

    err = i2c_driver_install(m_port, conf.mode, 0, 0, 0);
    if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }

    m_initialized = true;
    return {HalError::OK, ESP_OK};
}

HalStatus HalI2c::write(uint8_t dev_addr, const uint8_t* data, size_t length, uint32_t timeout_ms) {
    if (!m_initialized) {
        return {HalError::ERR_NOT_INITIALIZED, ESP_OK};
    }
    if (data == nullptr || length == 0) {
        return {HalError::ERR_INVALID_ARG, ESP_OK};
    }

    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (dev_addr << 1) | I2C_MASTER_WRITE, true);
    i2c_master_write(cmd, data, length, true);
    i2c_master_stop(cmd);

    TickType_t ticks_to_wait = timeout_ms / portTICK_PERIOD_MS;
    esp_err_t err = i2c_master_cmd_begin(m_port, cmd, ticks_to_wait);
    i2c_cmd_link_delete(cmd);

    if (err == ESP_ERR_TIMEOUT) {
        return {HalError::ERR_TIMEOUT, err};
    } else if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }

    return {HalError::OK, ESP_OK};
}

HalStatus HalI2c::read(uint8_t dev_addr, uint8_t* data, size_t length, uint32_t timeout_ms) {
    if (!m_initialized) {
        return {HalError::ERR_NOT_INITIALIZED, ESP_OK};
    }
    if (data == nullptr || length == 0) {
        return {HalError::ERR_INVALID_ARG, ESP_OK};
    }

    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (dev_addr << 1) | I2C_MASTER_READ, true);
    if (length > 1) {
        i2c_master_read(cmd, data, length - 1, I2C_MASTER_ACK);
    }
    i2c_master_read_byte(cmd, data + length - 1, I2C_MASTER_NACK);
    i2c_master_stop(cmd);

    TickType_t ticks_to_wait = timeout_ms / portTICK_PERIOD_MS;
    esp_err_t err = i2c_master_cmd_begin(m_port, cmd, ticks_to_wait);
    i2c_cmd_link_delete(cmd);

    if (err == ESP_ERR_TIMEOUT) {
        return {HalError::ERR_TIMEOUT, err};
    } else if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }

    return {HalError::OK, ESP_OK};
}

HalStatus HalI2c::writeRead(uint8_t dev_addr, const uint8_t* write_data, size_t write_length, uint8_t* read_data, size_t read_length, uint32_t timeout_ms) {
    if (!m_initialized) {
        return {HalError::ERR_NOT_INITIALIZED, ESP_OK};
    }
    if (write_data == nullptr || write_length == 0 || read_data == nullptr || read_length == 0) {
        return {HalError::ERR_INVALID_ARG, ESP_OK};
    }

    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    
    // Write phase
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (dev_addr << 1) | I2C_MASTER_WRITE, true);
    i2c_master_write(cmd, write_data, write_length, true);
    
    // Repeated start for read phase
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (dev_addr << 1) | I2C_MASTER_READ, true);
    if (read_length > 1) {
        i2c_master_read(cmd, read_data, read_length - 1, I2C_MASTER_ACK);
    }
    i2c_master_read_byte(cmd, read_data + read_length - 1, I2C_MASTER_NACK);
    i2c_master_stop(cmd);

    TickType_t ticks_to_wait = timeout_ms / portTICK_PERIOD_MS;
    esp_err_t err = i2c_master_cmd_begin(m_port, cmd, ticks_to_wait);
    i2c_cmd_link_delete(cmd);

    if (err == ESP_ERR_TIMEOUT) {
        return {HalError::ERR_TIMEOUT, err};
    } else if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }

    return {HalError::OK, ESP_OK};
}

HalStatus HalI2c::scanBus(std::vector<uint8_t>& found_addresses) {
    if (!m_initialized) {
        return {HalError::ERR_NOT_INITIALIZED, ESP_OK};
    }

    found_addresses.clear();
    
    for (uint8_t addr = 1; addr < 127; addr++) {
        i2c_cmd_handle_t cmd = i2c_cmd_link_create();
        i2c_master_start(cmd);
        i2c_master_write_byte(cmd, (addr << 1) | I2C_MASTER_WRITE, true);
        i2c_master_stop(cmd);
        
        esp_err_t err = i2c_master_cmd_begin(m_port, cmd, 10 / portTICK_PERIOD_MS);
        i2c_cmd_link_delete(cmd);
        
        if (err == ESP_OK) {
            found_addresses.push_back(addr);
        }
    }

    return {HalError::OK, ESP_OK};
}

} // namespace hal
} // namespace rover
