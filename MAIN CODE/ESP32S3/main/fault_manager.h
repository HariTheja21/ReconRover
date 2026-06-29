/**
 * @file fault_manager.h
 * @brief Recon Rover V1 - ESP32 Firmware
 * 
 * Reads Fault Queue, triggers safe mode, queues fault packets
 */

#ifndef ROVER_FAULT_MANAGER_H
#define ROVER_FAULT_MANAGER_H

// TODO: Add required includes

namespace rover {

/**
 * @class FaultManager
 * @brief Reads Fault Queue, triggers safe mode, queues fault packets
 */
class FaultManager {
public:
    FaultManager();
    ~FaultManager();

    // TODO: Define public interface

private:
    // TODO: Define private members
};

} // namespace rover

#endif // ROVER_FAULT_MANAGER_H
