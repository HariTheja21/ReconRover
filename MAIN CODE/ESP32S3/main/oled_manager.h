/**
 * @file oled_manager.h
 * @brief Recon Rover V1 - OLED Manager
 *
 * Manages the PCA9548A I2C Multiplexer and the two SSD1306 OLED displays.
 */

#ifndef ROVER_OLED_MANAGER_H
#define ROVER_OLED_MANAGER_H

#include "driver_pca9548a.h"
#include "driver_ssd1306.h"

namespace rover {

/**
 * @class OLEDManager
 * @brief Plain C++ class that orchestrates the I2C Mux and OLEDs.
 */
class OLEDManager {
public:
    /**
     * @brief Constructs the manager.
     * @param mux Pointer to the I2C multiplexer driver.
     * @param left_eye Pointer to the SSD1306 driver for the left eye.
     * @param right_eye Pointer to the SSD1306 driver for the right eye.
     * @param mux_ch_left The MUX channel for the left eye.
     * @param mux_ch_right The MUX channel for the right eye.
     */
    OLEDManager(driver::DriverPca9548a* mux, 
                driver::DriverSsd1306* left_eye, 
                driver::DriverSsd1306* right_eye,
                uint8_t mux_ch_left,
                uint8_t mux_ch_right);

    /**
     * @brief Initializes the MUX and both OLED displays.
     */
    void init();

    /**
     * @brief Selects which display to send draw commands to.
     * @param is_left True for left eye, False for right eye.
     */
    void selectDisplay(bool is_left);

    /**
     * @brief Provides access to the currently selected display's drawing primitives.
     * @return Pointer to the active SSD1306 driver.
     */
    driver::DriverSsd1306* getActiveDisplay();

    /**
     * @brief Flushes the frame buffer of the currently selected display to hardware.
     */
    void update();

private:
    driver::DriverPca9548a* m_mux;
    driver::DriverSsd1306* m_left_eye;
    driver::DriverSsd1306* m_right_eye;
    
    uint8_t m_mux_ch_left;
    uint8_t m_mux_ch_right;
    bool m_is_left_active;
};

} // namespace rover

#endif // ROVER_OLED_MANAGER_H
