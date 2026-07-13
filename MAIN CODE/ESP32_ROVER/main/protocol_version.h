/**
 * @file protocol_version.h
 * @brief Recon Rover V1 - Communication Protocol Version
 *
 * Defines the current protocol version. Any mismatch between ESP32
 * and Raspberry Pi should trigger a safe failure.
 */

#ifndef ROVER_PROTOCOL_VERSION_H
#define ROVER_PROTOCOL_VERSION_H

#include <cstdint>

namespace rover {
namespace comms {

constexpr uint8_t PROTOCOL_VERSION_MAJOR = 1;
constexpr uint8_t PROTOCOL_VERSION_MINOR = 0;
constexpr uint8_t PROTOCOL_VERSION_PATCH = 0;

} // namespace comms
} // namespace rover

#endif // ROVER_PROTOCOL_VERSION_H
