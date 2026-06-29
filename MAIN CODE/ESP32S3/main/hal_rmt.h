/**
 * @file hal_rmt.h
 * @brief Recon Rover V1 - RMT (Remote Control) TX HAL
 * 
 * Hardware Abstraction for the ESP32 RMT peripheral, specifically
 * designed for transmitting LED strip pulse trains.
 */

#ifndef ROVER_HAL_RMT_H
#define ROVER_HAL_RMT_H

#include "hal_types.h"
#include "driver/gpio.h"
#include "driver/rmt_tx.h"
#include <cstdint>

namespace rover {
namespace hal {

/**
 * @struct LedStripEncoderConfig
 * @brief Configuration for a WS2812-compatible RMT encoder.
 */
struct LedStripEncoderConfig {
    uint32_t resolution_hz;
};

/**
 * @class HalRmtTx
 * @brief RMT Transmit abstraction for driving LEDs.
 */
class HalRmtTx {
public:
    HalRmtTx();
    ~HalRmtTx();

    /**
     * @brief Initializes the RMT TX channel on a specific pin.
     * @param pin The GPIO pin to output the RMT signal.
     * @param max_leds Maximum number of LEDs (used for memory sizing).
     * @param resolution_hz Clock resolution for the RMT channel.
     * @return HalStatus indicating success or failure.
     */
    HalStatus init(gpio_num_t pin, uint32_t max_leds, uint32_t resolution_hz = 10000000); // 10MHz default

    /**
     * @brief Transmits a buffer of RGB pixels.
     * @param pixels Pointer to the GRB byte array (size must be num_leds * 3).
     * @param num_leds Number of LEDs to transmit.
     * @return HalStatus indicating success or failure.
     */
    HalStatus transmit(const uint8_t* pixels, uint32_t num_leds);

private:
    rmt_channel_handle_t m_tx_channel;
    rmt_encoder_handle_t m_encoder;
    bool m_initialized;
};

} // namespace hal
} // namespace rover

#endif // ROVER_HAL_RMT_H
