/**
 * @file utils.h
 * @brief Recon Rover V1 - Common Utilities
 *
 * Provides standalone math, filtering, and data integrity helper functions.
 */

#ifndef ROVER_UTILS_H
#define ROVER_UTILS_H

#include <cstdint>
#include <cstddef>

namespace rover {
namespace utils {

/**
 * @brief Calculates the standard CCITT CRC-16 (polynomial 0x1021).
 * @param data Pointer to the data buffer.
 * @param length Length of the data in bytes.
 * @return The 16-bit CRC value.
 */
uint16_t crc16(const uint8_t* data, size_t length);

/**
 * @brief Linearly maps a value from one range to another.
 * @param x The input value.
 * @param in_min The minimum of the input range.
 * @param in_max The maximum of the input range.
 * @param out_min The minimum of the output range.
 * @param out_max The maximum of the output range.
 * @return The mapped value.
 */
float mapFloat(float x, float in_min, float in_max, float out_min, float out_max);

/**
 * @brief Constrains a value between a minimum and a maximum.
 * @param x The input value.
 * @param min The minimum allowed value.
 * @param max The maximum allowed value.
 * @return The constrained value.
 */
float constrainFloat(float x, float min, float max);

/**
 * @class SimpleMovingAverage
 * @brief Computes the moving average over a fixed window of floats.
 * 
 * @tparam N The size of the window.
 */
template <size_t N>
class SimpleMovingAverage {
public:
    SimpleMovingAverage() : sum(0.0f), count(0), index(0) {
        for (size_t i = 0; i < N; ++i) buffer[i] = 0.0f;
    }

    /**
     * @brief Adds a new value to the filter and returns the new average.
     */
    float add(float value) {
        sum -= buffer[index];
        buffer[index] = value;
        sum += value;
        
        index = (index + 1) % N;
        if (count < N) count++;
        
        return sum / static_cast<float>(count);
    }

    /**
     * @brief Returns the current average without adding a new value.
     */
    float getAverage() const {
        if (count == 0) return 0.0f;
        return sum / static_cast<float>(count);
    }

private:
    float buffer[N];
    float sum;
    size_t count;
    size_t index;
};

} // namespace utils
} // namespace rover

#endif // ROVER_UTILS_H
