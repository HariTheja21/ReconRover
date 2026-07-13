/**
 * @file led_manager.cpp
 * @brief Recon Rover V1 - LED Manager
 */

#include "led_manager.h"
#include "utils.h"

namespace rover {

LEDManager::LEDManager(driver::DriverWs2812* driver, uint16_t num_leds)
    : m_driver(driver), m_num_leds(num_leds), 
      m_brightness(1.0f), m_mode(LedMode::OFF),
      m_r(0), m_g(0), m_b(0) {
}

void LEDManager::init() {
    if (m_driver) {
        m_driver->init();
    }
}

void LEDManager::setColor(uint8_t r, uint8_t g, uint8_t b) {
    m_r = r;
    m_g = g;
    m_b = b;
    if (m_mode == LedMode::SOLID) {
        updateHardware();
    }
}

void LEDManager::setBrightness(float brightness) {
    m_brightness = utils::constrainFloat(brightness, 0.0f, 1.0f);
    updateHardware();
}

void LEDManager::runAnimation(LedMode mode) {
    m_mode = mode;
    if (m_mode == LedMode::OFF) {
        if (m_driver) {
            m_driver->clear();
            m_driver->show();
        }
    } else if (m_mode == LedMode::SOLID) {
        updateHardware();
    }
}

void LEDManager::tick() {
    // Advanced animations (Blink, Sweep, Breathe) would be processed here
    // using a state machine and timers. Left empty per strict phase rules 
    // against AI/application behaviour.
}

void LEDManager::updateHardware() {
    if (!m_driver) return;

    uint8_t scaled_r = static_cast<uint8_t>(m_r * m_brightness);
    uint8_t scaled_g = static_cast<uint8_t>(m_g * m_brightness);
    uint8_t scaled_b = static_cast<uint8_t>(m_b * m_brightness);

    for (uint16_t i = 0; i < m_num_leds; ++i) {
        m_driver->setPixel(i, scaled_r, scaled_g, scaled_b);
    }
    m_driver->show();
}

} // namespace rover
