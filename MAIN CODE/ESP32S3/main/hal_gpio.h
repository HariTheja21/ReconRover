/**
 * @file hal_gpio.h
 * @brief Recon Rover V1 - ESP32 Hardware Abstraction Layer for GPIO
 *
 * Provides a clean C++ interface for ESP32 GPIO configuration and manipulation.
 */

#ifndef ROVER_HAL_GPIO_H
#define ROVER_HAL_GPIO_H

#include <cstdint>
#include "hal_types.h"
#include "driver/gpio.h"

namespace rover {
namespace hal {

/**
 * @enum GpioMode
 * @brief GPIO operational modes.
 */
enum class GpioMode {
    INPUT,          /**< Input only */
    OUTPUT,         /**< Output only */
    INPUT_OUTPUT    /**< Bidirectional (Input and Output) */
};

/**
 * @enum GpioPull
 * @brief GPIO pull-up/pull-down resistor configurations.
 */
enum class GpioPull {
    NONE,           /**< No pull resistors enabled */
    UP,             /**< Internal pull-up resistor enabled */
    DOWN,           /**< Internal pull-down resistor enabled */
    UP_DOWN         /**< Both pull-up and pull-down enabled */
};

/**
 * @enum GpioInterruptType
 * @brief GPIO interrupt trigger conditions.
 */
enum class GpioInterruptType {
    NONE,           /**< Interrupt disabled */
    RISING_EDGE,    /**< Interrupt on rising edge */
    FALLING_EDGE,   /**< Interrupt on falling edge */
    ANY_EDGE,       /**< Interrupt on both rising and falling edges */
    LOW_LEVEL,      /**< Interrupt on low level */
    HIGH_LEVEL      /**< Interrupt on high level */
};

/**
 * @brief Type alias for GPIO interrupt service routine callbacks.
 * @param arg User-provided argument passed to the ISR.
 */
using GpioIsrCallback = void (*)(void* arg);

/**
 * @class HalGpio
 * @brief Hardware Abstraction Layer for a single GPIO pin.
 *
 * Wraps ESP-IDF GPIO functions to provide safe, RAII-compliant access to a GPIO pin.
 */
class HalGpio {
public:
    /**
     * @brief Constructs a GPIO object. Does not initialize the hardware.
     * @param pin The GPIO pin number.
     */
    explicit HalGpio(gpio_num_t pin);

    /**
     * @brief Destructor. Disables interrupts and resets the pin configuration.
     */
    ~HalGpio();

    /**
     * @brief Initializes the GPIO pin with the specified mode and pull configuration.
     * @param mode The operational mode (Input, Output, or Both).
     * @param pull The internal pull resistor configuration.
     * @return HalStatus indicating success or specific failure.
     */
    HalStatus init(GpioMode mode, GpioPull pull = GpioPull::NONE);

    /**
     * @brief Reads the current logic level of the GPIO pin.
     * @param[out] level Reference to store the read level (true = HIGH, false = LOW).
     * @return HalStatus indicating success or failure.
     */
    HalStatus read(bool& level) const;

    /**
     * @brief Sets the logic level of the GPIO pin.
     * @param level The desired logic level (true = HIGH, false = LOW).
     * @return HalStatus indicating success or failure.
     */
    HalStatus write(bool level);

    /**
     * @brief Toggles the current logic level of the GPIO pin.
     * @return HalStatus indicating success or failure.
     */
    HalStatus toggle();

    /**
     * @brief Registers an Interrupt Service Routine (ISR) for this pin.
     * @param type The trigger condition for the interrupt.
     * @param callback The function pointer to execute when triggered.
     * @param arg Optional user argument to pass to the callback.
     * @return HalStatus indicating success or failure.
     */
    HalStatus registerInterrupt(GpioInterruptType type, GpioIsrCallback callback, void* arg = nullptr);

    /**
     * @brief Globally enables the GPIO interrupt service.
     * @note This must be called once before any pin-specific interrupts will fire.
     * @return HalStatus indicating success or failure.
     */
    static HalStatus installInterruptService();

private:
    gpio_num_t m_pin;         /**< The GPIO pin number assigned to this instance */
    bool m_initialized;       /**< Tracks if the pin has been initialized */
    bool m_isr_registered;    /**< Tracks if an ISR is currently registered for this pin */
    bool m_current_level;     /**< Caches the last written level for toggling */
    
    static bool s_isr_service_installed; /**< Tracks if the global ISR service is installed */
};

} // namespace hal
} // namespace rover

#endif // ROVER_HAL_GPIO_H
