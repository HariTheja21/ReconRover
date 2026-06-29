/**
 * @file driver_ssd1306.h
 * @brief Recon Rover V1 - SSD1306 OLED Display Driver
 *
 * Hardware driver for the SSD1306 128x64 OLED display.
 * Responsible only for primitive drawing operations and display updates.
 */

#ifndef ROVER_DRIVER_SSD1306_H
#define ROVER_DRIVER_SSD1306_H

#include <cstdint>
#include <cstring>
#include "hal_i2c.h"

namespace rover {
namespace driver {

/**
 * @brief Default I2C address for SSD1306.
 */
constexpr uint8_t SSD1306_ADDR = 0x3C;

/**
 * @class DriverSsd1306
 * @brief Driver class for the SSD1306 OLED.
 */
class DriverSsd1306 {
public:
    /**
     * @brief Constructs the driver.
     * @param i2c Pointer to an initialized HalI2c instance.
     */
    explicit DriverSsd1306(hal::HalI2c* i2c);

    /**
     * @brief Initializes the display (power on, set multiplex, charge pump, etc.).
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus init();

    /**
     * @brief Clears the internal frame buffer.
     * @note Does not update the physical display until update() is called.
     */
    void clear();

    /**
     * @brief Pushes the internal frame buffer to the physical display.
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus update();

    /**
     * @brief Sets the display brightness (contrast control).
     * @param brightness Brightness level (0-255).
     * @return HalStatus indicating success or failure.
     */
    hal::HalStatus setBrightness(uint8_t brightness);

    /**
     * @brief Draws a single pixel in the buffer.
     * @param x X coordinate (0-127).
     * @param y Y coordinate (0-63).
     * @param white True to draw white pixel, false to clear it.
     */
    void drawPixel(int x, int y, bool white = true);

    /**
     * @brief Draws a line using Bresenham's algorithm.
     * @param x0 Start X.
     * @param y0 Start Y.
     * @param x1 End X.
     * @param y1 End Y.
     * @param white True for white, false for black.
     */
    void drawLine(int x0, int y0, int x1, int y1, bool white = true);

    /**
     * @brief Draws an unfilled rectangle.
     * @param x Top-left X.
     * @param y Top-left Y.
     * @param w Width.
     * @param h Height.
     * @param white True for white, false for black.
     */
    void drawRect(int x, int y, int w, int h, bool white = true);

    /**
     * @brief Draws a circle using midpoint circle algorithm.
     * @param xc Center X.
     * @param yc Center Y.
     * @param r Radius.
     * @param white True for white, false for black.
     */
    void drawCircle(int xc, int yc, int r, bool white = true);

    /**
     * @brief Draws a bitmap image from PROGMEM or RAM.
     * @param x Top-left X.
     * @param y Top-left Y.
     * @param bitmap Pointer to the raw byte array (horizontal 1bpp).
     * @param w Width of bitmap in pixels.
     * @param h Height of bitmap in pixels.
     * @param white True to draw set bits as white.
     */
    void drawBitmap(int x, int y, const uint8_t* bitmap, int w, int h, bool white = true);

    /**
     * @brief Draws a text string (using a simple built-in 5x7 font or similar).
     * @param x Top-left X.
     * @param y Top-left Y.
     * @param text Null-terminated string to draw.
     * @param white True for white text.
     */
    void drawText(int x, int y, const char* text, bool white = true);

private:
    hal::HalI2c* m_i2c;                  /**< Pointer to the I2C HAL */
    uint8_t m_buffer[1024];              /**< 128x64 / 8 = 1024 byte frame buffer */

    /**
     * @brief Sends a single command byte to the display.
     * @param cmd Command byte.
     * @return HalStatus
     */
    hal::HalStatus sendCommand(uint8_t cmd);
};

} // namespace driver
} // namespace rover

#endif // ROVER_DRIVER_SSD1306_H
