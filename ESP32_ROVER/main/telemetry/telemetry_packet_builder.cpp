#include "telemetry_packet_builder.h"

namespace ReconRover {
namespace Telemetry {

TelemetryPacketBuilder::TelemetryPacketBuilder(TelemetryEncoder& encoder, TelemetryStatistics& stats)
    : encoder_(encoder), stats_(stats), next_sequence_(0) {}

uint8_t TelemetryPacketBuilder::CalculateCRC(const uint8_t* data, uint8_t length) {
    uint8_t crc = 0;
    for (uint8_t i = 0; i < length; ++i) {
        crc ^= data[i];
    }
    return crc;
}

void TelemetryPacketBuilder::Build(const TelemetryEvent& event, TelemetryPacket& out_packet) {
    out_packet.buffer[0] = HEADER_1;
    out_packet.buffer[1] = HEADER_2;
    out_packet.buffer[2] = static_cast<uint8_t>(event.type);
    out_packet.buffer[3] = next_sequence_++;

    uint8_t payload_len = 0;
    // encoder writes into bytes 4,5,6,7
    encoder_.EncodePayload(event, &out_packet.buffer[4], payload_len);
    
    // Packet is rigidly 9 bytes matching Raspberry Pi structure
    out_packet.length = 9;
    out_packet.buffer[8] = CalculateCRC(out_packet.buffer, 8);

    stats_.packets_generated++;
    stats_.bytes_encoded += out_packet.length;
}

} // namespace Telemetry
} // namespace ReconRover
