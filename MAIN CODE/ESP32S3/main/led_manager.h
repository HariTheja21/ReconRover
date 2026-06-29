/**
 * @file led_manager.h
 * @brief Recon Rover V1 - LED Manager
 *
 * Manages the WS2812 driver for the status/underglow LEDs.
 */

#ifndef ROVER_LED_MANAGER_H
#define ROVER_LED_MANAGER_H

#include "driver_ws2812.h"
#include "types_actuator.h"

namespace rover {

/**
 * @class LEDManager
 * @brief Plain C++ class that owns and orchestrates the LED driver.
 */
class LEDManager {
public:
    /**
     * @brief Constructs the manager.
     * @param driver Pointer to the WS2812 driver.
     * @param num_leds Number of LEDs in the strip.
     */
    LEDManager(driver::DriverWs2812* driver, uint16_t num_leds);

    /**
     * @brief Initializes the LED hardware.
     */
    void init();

    /**
     * @brief Sets all LEDs to a specific solid color.
     * @param r Red component (0-255).
     * @param g Green component (0-255).
     * @param b Blue component (0-255).
     */
    void setColor(uint8_t r, uint8_t g, uint8_t b);

    /**
     * @brief Sets the global brightness multiplier.
     * @param brightness Multiplier from 0.0 to 1.0.
     */
    void setBrightness(float brightness);

    /**
     * @brief Configures the active animation mode.
     * @param mode The desired LedMode.
     */
    void runAnimation(LedMode mode);

    /**
     * @brief Should be called periodically to process the active animation.
     */
    void tick();

private:
    driver::DriverWs2812* m_driver;
    uint16_t m_num_leds;
    float m_brightness;
    LedMode m_mode;
    
    // Basic state for solid color
    uint8_t m_r;
    uint8_t m_g;
    uint8_t m_b;

    void updateHardware();
};

} // namespace rover

#endif // ROVER_LED_MANAGER_H
