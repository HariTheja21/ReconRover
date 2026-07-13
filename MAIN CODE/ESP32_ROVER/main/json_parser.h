/**
 * @file json_parser.h
 * @brief Recon Rover V1 - JSON Parser
 *
 * Safely converts JSON strings into internal C++ CommandPacket structures.
 */

#ifndef ROVER_JSON_PARSER_H
#define ROVER_JSON_PARSER_H

#include "types_protocol.h"
#include <string>

namespace rover {
namespace comms {

/**
 * @class JsonParser
 * @brief Handles JSON deserialization of inbound packets.
 */
class JsonParser {
public:
    /**
     * @brief Parses a JSON string into a CommandPacket.
     * @param json The JSON string to parse.
     * @param[out] packet The output packet structure.
     * @return True if parsing succeeded and required fields were found.
     */
    static bool parseCommand(const std::string& json, CommandPacket& packet);
};

} // namespace comms
} // namespace rover

#endif // ROVER_JSON_PARSER_H
