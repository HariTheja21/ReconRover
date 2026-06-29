/**
 * @file watchdog.h
 * @brief Recon Rover V1 - ESP32 Firmware
 * 
 * Monitors task heartbeats, triggers safe mode
 */

#ifndef ROVER_WATCHDOG_H
#define ROVER_WATCHDOG_H

// TODO: Add required includes

namespace rover {

/**
 * @class Watchdog
 * @brief Monitors task heartbeats, triggers safe mode
 */
class Watchdog {
public:
    Watchdog();
    ~Watchdog();

    // TODO: Define public interface

private:
    // TODO: Define private members
};

} // namespace rover

#endif // ROVER_WATCHDOG_H
