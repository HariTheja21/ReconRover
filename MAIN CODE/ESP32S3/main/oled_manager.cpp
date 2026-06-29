/**
 * @file oled_manager.cpp
 * @brief Recon Rover V1 - OLED Manager
 */

#include "oled_manager.h"

namespace rover {

OLEDManager::OLEDManager(driver::DriverPca9548a* mux, 
                         driver::DriverSsd1306* left_eye, 
                         driver::DriverSsd1306* right_eye,
                         uint8_t mux_ch_left, uint8_t mux_ch_right)
    : m_mux(mux), m_left_eye(left_eye), m_right_eye(right_eye),
      m_mux_ch_left(mux_ch_left), m_mux_ch_right(mux_ch_right),
      m_is_left_active(true) {
}

void OLEDManager::init() {
    if (m_mux) {
        m_mux->init();
    }
    
    // Init Left
    if (m_mux && m_left_eye) {
        m_mux->selectChannel(m_mux_ch_left);
        m_left_eye->init();
        m_left_eye->clear();
        m_left_eye->update();
    }

    // Init Right
    if (m_mux && m_right_eye) {
        m_mux->selectChannel(m_mux_ch_right);
        m_right_eye->init();
        m_right_eye->clear();
        m_right_eye->update();
    }
}

void OLEDManager::selectDisplay(bool is_left) {
    if (!m_mux) return;
    
    m_is_left_active = is_left;
    if (m_is_left_active) {
        m_mux->selectChannel(m_mux_ch_left);
    } else {
        m_mux->selectChannel(m_mux_ch_right);
    }
}

driver::DriverSsd1306* OLEDManager::getActiveDisplay() {
    return m_is_left_active ? m_left_eye : m_right_eye;
}

void OLEDManager::update() {
    driver::DriverSsd1306* active = getActiveDisplay();
    if (active) {
        active->update();
    }
}

} // namespace rover
