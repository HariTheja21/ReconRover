/**
 * @file driver_ws2812.cpp
 * @brief Recon Rover V1 - WS2812 LED Driver
 *
 * Implementation of the DriverWs2812 class.
 */

#include "driver_ws2812.h"

namespace rover {
namespace driver {

DriverWs2812::DriverWs2812(hal::HalRmtTx* rmt, uint16_t num_leds)
    : m_rmt(rmt), m_num_leds(num_leds), m_pixels(nullptr) {
}

DriverWs2812::~DriverWs2812() {
    if (m_pixels) {
        delete[] m_pixels;
    }
}

hal::HalStatus DriverWs2812::init() {
    if (m_rmt == nullptr || m_num_leds == 0) {
        return {hal::HalError::ERR_INVALID_ARG, 0};
    }

    m_pixels = new uint8_t[m_num_leds * 3];
    if (m_pixels == nullptr) {
        return {hal::HalError::ERR_NO_MEMORY, 0};
    }

    clear();
    return show(); // Turn off LEDs on init
}

hal::HalStatus DriverWs2812::setPixel(uint16_t index, uint8_t r, uint8_t g, uint8_t b) {
    if (index >= m_num_leds || m_pixels == nullptr) {
        return {hal::HalError::ERR_INVALID_ARG, 0};
    }

    // WS2812 typically expects GRB order
    uint32_t offset = index * 3;
    m_pixels[offset]     = g;
    m_pixels[offset + 1] = r;
    m_pixels[offset + 2] = b;

    return {hal::HalError::OK, 0};
}

hal::HalStatus DriverWs2812::show() {
    if (m_rmt == nullptr || m_pixels == nullptr) {
        return {hal::HalError::ERR_INVALID_STATE, 0};
    }

    return m_rmt->transmit(m_pixels, m_num_leds);
}

void DriverWs2812::clear() {
    if (m_pixels) {
        for (uint16_t i = 0; i < m_num_leds * 3; ++i) {
            m_pixels[i] = 0;
        }
    }
}

} // namespace driver
} // namespace rover
