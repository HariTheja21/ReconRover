/**
 * @file hal_gpio.cpp
 * @brief Recon Rover V1 - ESP32 Hardware Abstraction Layer for GPIO
 *
 * Implementation of the HalGpio class.
 */

#include "hal_gpio.h"

namespace rover {
namespace hal {

bool HalGpio::s_isr_service_installed = false;

HalGpio::HalGpio(gpio_num_t pin)
    : m_pin(pin), m_initialized(false), m_isr_registered(false), m_current_level(false) {
}

HalGpio::~HalGpio() {
    if (m_initialized) {
        if (m_isr_registered) {
            gpio_isr_handler_remove(m_pin);
        }
        gpio_reset_pin(m_pin);
    }
}

HalStatus HalGpio::init(GpioMode mode, GpioPull pull) {
    if (m_initialized) {
        return {HalError::ERR_ALREADY_INITIALIZED, ESP_OK};
    }

    gpio_config_t io_conf = {};
    io_conf.pin_bit_mask = (1ULL << m_pin);
    io_conf.intr_type = GPIO_INTR_DISABLE;

    switch (mode) {
        case GpioMode::INPUT:
            io_conf.mode = GPIO_MODE_INPUT;
            break;
        case GpioMode::OUTPUT:
            io_conf.mode = GPIO_MODE_OUTPUT;
            break;
        case GpioMode::INPUT_OUTPUT:
            io_conf.mode = GPIO_MODE_INPUT_OUTPUT;
            break;
        default:
            return {HalError::ERR_INVALID_ARG, ESP_OK};
    }

    switch (pull) {
        case GpioPull::NONE:
            io_conf.pull_up_en = GPIO_PULLUP_DISABLE;
            io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
            break;
        case GpioPull::UP:
            io_conf.pull_up_en = GPIO_PULLUP_ENABLE;
            io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
            break;
        case GpioPull::DOWN:
            io_conf.pull_up_en = GPIO_PULLUP_DISABLE;
            io_conf.pull_down_en = GPIO_PULLDOWN_ENABLE;
            break;
        case GpioPull::UP_DOWN:
            io_conf.pull_up_en = GPIO_PULLUP_ENABLE;
            io_conf.pull_down_en = GPIO_PULLDOWN_ENABLE;
            break;
        default:
            return {HalError::ERR_INVALID_ARG, ESP_OK};
    }

    esp_err_t err = gpio_config(&io_conf);
    if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }

    m_initialized = true;
    m_current_level = false; // Default hardware state after config for output is 0
    return {HalError::OK, ESP_OK};
}

HalStatus HalGpio::read(bool& level) const {
    if (!m_initialized) {
        return {HalError::ERR_NOT_INITIALIZED, ESP_OK};
    }
    level = (gpio_get_level(m_pin) == 1);
    return {HalError::OK, ESP_OK};
}

HalStatus HalGpio::write(bool level) {
    if (!m_initialized) {
        return {HalError::ERR_NOT_INITIALIZED, ESP_OK};
    }
    esp_err_t err = gpio_set_level(m_pin, level ? 1 : 0);
    if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }
    m_current_level = level;
    return {HalError::OK, ESP_OK};
}

HalStatus HalGpio::toggle() {
    return write(!m_current_level);
}

HalStatus HalGpio::registerInterrupt(GpioInterruptType type, GpioIsrCallback callback, void* arg) {
    if (!m_initialized) {
        return {HalError::ERR_NOT_INITIALIZED, ESP_OK};
    }
    if (!s_isr_service_installed) {
        return {HalError::ERR_NOT_INITIALIZED, ESP_OK}; // Must install service first
    }
    if (callback == nullptr) {
        return {HalError::ERR_INVALID_ARG, ESP_OK};
    }

    gpio_int_type_t intr_type;
    switch (type) {
        case GpioInterruptType::NONE:         intr_type = GPIO_INTR_DISABLE; break;
        case GpioInterruptType::RISING_EDGE:  intr_type = GPIO_INTR_POSEDGE; break;
        case GpioInterruptType::FALLING_EDGE: intr_type = GPIO_INTR_NEGEDGE; break;
        case GpioInterruptType::ANY_EDGE:     intr_type = GPIO_INTR_ANYEDGE; break;
        case GpioInterruptType::LOW_LEVEL:    intr_type = GPIO_INTR_LOW_LEVEL; break;
        case GpioInterruptType::HIGH_LEVEL:   intr_type = GPIO_INTR_HIGH_LEVEL; break;
        default: return {HalError::ERR_INVALID_ARG, ESP_OK};
    }

    esp_err_t err = gpio_set_intr_type(m_pin, intr_type);
    if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }

    if (type != GpioInterruptType::NONE) {
        err = gpio_isr_handler_add(m_pin, callback, arg);
        if (err != ESP_OK) {
            return {HalError::ERR_HARDWARE, err};
        }
        m_isr_registered = true;
    } else if (m_isr_registered) {
        gpio_isr_handler_remove(m_pin);
        m_isr_registered = false;
    }

    return {HalError::OK, ESP_OK};
}

HalStatus HalGpio::installInterruptService() {
    if (s_isr_service_installed) {
        return {HalError::ERR_ALREADY_INITIALIZED, ESP_OK};
    }
    esp_err_t err = gpio_install_isr_service(0);
    if (err != ESP_OK) {
        return {HalError::ERR_HARDWARE, err};
    }
    s_isr_service_installed = true;
    return {HalError::OK, ESP_OK};
}

} // namespace hal
} // namespace rover
