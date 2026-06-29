/**
 * @file command_parser.h
 * @brief Recon Rover V1 - ESP32 Firmware
 * 
 * Parses JSON from Command Queue, dispatches to Actuator Queues
 */

#ifndef ROVER_COMMAND_PARSER_H
#define ROVER_COMMAND_PARSER_H

// TODO: Add required includes

namespace rover {

/**
 * @class CommandParser
 * @brief Parses JSON from Command Queue, dispatches to Actuator Queues
 */
class CommandParser {
public:
    CommandParser();
    ~CommandParser();

    // TODO: Define public interface

private:
    // TODO: Define private members
};

} // namespace rover

#endif // ROVER_COMMAND_PARSER_H
