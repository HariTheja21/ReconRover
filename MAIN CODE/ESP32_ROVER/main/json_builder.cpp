/**
 * @file json_builder.cpp
 * @brief Recon Rover V1 - JSON Builder
 */

#include "json_builder.h"
#include "protocol_version.h"
#include <ArduinoJson.h>

namespace rover {
namespace comms {

std::string JsonBuilder::buildTelemetry(const TelemetryPacket& packet) {
    // 512 bytes is sufficient for our telemetry fields without dynamic allocation
    StaticJsonDocument<512> doc;
    
    doc["type"] = "telemetry";
    doc["v_maj"] = PROTOCOL_VERSION_MAJOR;
    doc["v_min"] = PROTOCOL_VERSION_MINOR;
    
    doc["ts"] = packet.timestamp_ms;
    doc["state"] = static_cast<uint8_t>(packet.state);
    
    JsonObject imu = doc.createNestedObject("imu");
    imu["ax"] = packet.imu.accel_x_g;
    imu["ay"] = packet.imu.accel_y_g;
    imu["az"] = packet.imu.accel_z_g;
    imu["gx"] = packet.imu.gyro_x_dps;
    imu["gy"] = packet.imu.gyro_y_dps;
    imu["gz"] = packet.imu.gyro_z_dps;
    
    doc["tof"] = packet.tof.distance_mm;
    doc["sonar"] = packet.sonar.distance_cm;
    doc["gas"] = packet.gas.voltage_mv;
    
    JsonObject pwr = doc.createNestedObject("pwr");
    pwr["v"] = packet.power.bus_voltage_v;
    pwr["i"] = packet.power.current_ma;
    
    doc["faults"] = packet.active_faults;

    std::string output;
    serializeJson(doc, output);
    return output;
}

std::string JsonBuilder::buildHealth(const SystemHealth& health) {
    StaticJsonDocument<256> doc;
    
    doc["type"] = "health";
    doc["ts"] = health.uptime_ms;
    doc["heap"] = health.free_heap_bytes;
    doc["safe"] = health.safe_mode_active;
    
    // Simplistic breakdown for brevity in JSON payload
    doc["s_fail"] = health.sensors.mpu6050.failure_count + health.sensors.vl53l0x.failure_count;
    doc["p_fail"] = health.power.ina219.failure_count;
    doc["bat_low"] = health.power.battery_low;
    doc["over_i"] = health.power.overcurrent;

    std::string output;
    serializeJson(doc, output);
    return output;
}

std::string JsonBuilder::buildFault(const Error& fault) {
    StaticJsonDocument<128> doc;
    
    doc["type"] = "fault";
    doc["sys"] = static_cast<uint8_t>(fault.subsystem);
    doc["code"] = static_cast<uint8_t>(fault.code);
    
    std::string output;
    serializeJson(doc, output);
    return output;
}

} // namespace comms
} // namespace rover
