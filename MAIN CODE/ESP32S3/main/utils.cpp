/**
 * @file utils.cpp
 * @brief Recon Rover V1 - Common Utilities
 *
 * Implementation of standalone utility functions.
 */

#include "utils.h"

namespace rover {
namespace utils {

uint16_t crc16(const uint8_t* data, size_t length) {
    uint16_t crc = 0xFFFF; // Initial value commonly used

    for (size_t i = 0; i < length; ++i) {
        crc ^= (static_cast<uint16_t>(data[i]) << 8);
        for (uint8_t bit = 0; bit < 8; ++bit) {
            if (crc & 0x8000) {
                crc = (crc << 1) ^ 0x1021; // Polynomial
            } else {
                crc = (crc << 1);
            }
        }
    }
    return crc;
}

float mapFloat(float x, float in_min, float in_max, float out_min, float out_max) {
    if (in_max == in_min) {
        return out_min; // Avoid divide by zero
    }
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

float constrainFloat(float x, float min, float max) {
    if (x < min) return min;
    if (x > max) return max;
    return x;
}

} // namespace utils
} // namespace rover
