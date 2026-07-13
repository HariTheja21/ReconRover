/**
 * @file json_parser.cpp
 * @brief Recon Rover V1 - JSON Parser
 */

#include "json_parser.h"
#include "protocol_version.h"
#include <ArduinoJson.h>

namespace rover {
namespace comms {

bool JsonParser::parseCommand(const std::string& json, CommandPacket& packet) {
    StaticJsonDocument<512> doc;
    DeserializationError err = deserializeJson(doc, json);
    
    if (err) {
        return false;
    }

    // Version check
    if (!doc.containsKey("v_maj") || doc["v_maj"] != PROTOCOL_VERSION_MAJOR) {
        return false;
    }

    // Wipe old state
    packet = {};
    packet.sequence_num = doc["seq"] | 0;

    // Parse Motor Command
    if (doc.containsKey("mot")) {
        packet.has_motor_cmd = true;
        JsonObject mot = doc["mot"];
        packet.motor_cmd.left_velocity = mot["l"] | 0.0f;
        packet.motor_cmd.right_velocity = mot["r"] | 0.0f;
    }

    // Parse Servo Command
    if (doc.containsKey("srv")) {
        packet.has_servo_cmd = true;
        JsonObject srv = doc["srv"];
        packet.servo_cmd.pan_deg = srv["p"] | 90.0f;
        packet.servo_cmd.tilt_deg = srv["t"] | 90.0f;
    }

    // Parse Eye Command
    if (doc.containsKey("eye")) {
        packet.has_eye_cmd = true;
        packet.eye_cmd.animation_index = doc["eye"]["anim"] | 0;
    }

    // Parse LED Command
    if (doc.containsKey("led")) {
        packet.has_led_cmd = true;
        JsonObject led = doc["led"];
        packet.led_cmd.mode = static_cast<LedMode>(led["m"] | 0);
        packet.led_cmd.r = led["r"] | 0;
        packet.led_cmd.g = led["g"] | 0;
        packet.led_cmd.b = led["b"] | 0;
    }

    return true;
}

} // namespace comms
} // namespace rover
