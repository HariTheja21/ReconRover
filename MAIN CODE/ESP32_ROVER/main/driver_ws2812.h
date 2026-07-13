/**
 * @file driver_ws2812.h
 * @brief Recon Rover V1 - WS2812 LED Driver
 *
 * Hardware driver for the WS2812B Addressable LEDs.
 * Uses the RMT HAL for precise timing.
 */

#ifndef ROVER_DRIVER_WS2812_H
#define ROVER_DRIVER_WS2812_H

#include "hal_rmt.h"
#include <cstdint>

namespace rover {
namespace driver {

/**
 * @class DriverWs2812
 * @brief Driver class for WS2812B addressable LEDs.
 */
class DriverWs2812 {
public:
    /**
     * @brief Constructs the driver.
     * @param rmt Pointer to the RMT HAL instance.
     * @param num_leds The number of LEDs in the strip.
     */
    DriverWs2812(hal::HalRmtTx* rmt, uint16_t num_leds);
    ~DriverWs2812();

    /**
     * @brief Initializes the driver and allocates pixel buffers.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus init();

    /**
     * @brief Sets the color of a specific LED.
     * @param index The index of the LED (0-based).
     * @param r Red component (0-255).
     * @param g Green component (0-255).
     * @param b Blue component (0-255).
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus setPixel(uint16_t index, uint8_t r, uint8_t g, uint8_t b);

    /**
     * @brief Pushes the pixel buffer to the hardware.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus show();

    /**
     * @brief Clears all pixels to black (does not show automatically).
     */
    void clear();

private:
    hal::HalRmtTx* m_rmt;
    uint16_t m_num_leds;
    uint8_t* m_pixels; // dynamically allocated buffer, size = m_num_leds * 3
};

} // namespace driver
} // namespace rover

#endif // ROVER_DRIVER_WS2812_H
