/**
 * @file telemetry_builder.h
 * @brief Recon Rover V1 - ESP32 Firmware
 * 
 * Reads Sensor Queue, packs JSON, pushes to TX Queue
 */

#ifndef ROVER_TELEMETRY_BUILDER_H
#define ROVER_TELEMETRY_BUILDER_H

// TODO: Add required includes

namespace rover {

/**
 * @class TelemetryBuilder
 * @brief Reads Sensor Queue, packs JSON, pushes to TX Queue
 */
class TelemetryBuilder {
public:
    TelemetryBuilder();
    ~TelemetryBuilder();

    // TODO: Define public interface

private:
    // TODO: Define private members
};

} // namespace rover

#endif // ROVER_TELEMETRY_BUILDER_H
