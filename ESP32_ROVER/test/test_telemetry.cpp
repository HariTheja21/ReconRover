#include <iostream>
#include <vector>
#include <iomanip>
#include "telemetry/telemetry_manager.h"

using namespace ReconRover::Telemetry;

static std::vector<std::vector<uint8_t>> transmitted_packets;

void MockUartTx(const uint8_t* data, uint8_t length) {
    std::vector<uint8_t> pkt(data, data + length);
    transmitted_packets.push_back(pkt);
}

int main() {
    std::cout << "Starting ESP32 Telemetry System Internal Tests..." << std::endl;

    TelemetryManager manager(MockUartTx);
    manager.Init();

    std::cout << "Test 1: Heartbeat Generation & Scheduling" << std::endl;
    // Tick at 100ms - shouldn't trigger heartbeat (requires 1000ms)
    manager.Tick(100);
    // But motor status is 100ms, so 1 packet sent
    if (transmitted_packets.size() == 1) {
        std::cout << "  PASS (Motor)" << std::endl;
    } else {
        std::cout << "  FAIL" << std::endl; return 1;
    }

    manager.Tick(1000); // 1000ms - triggers heartbeat AND motor
    if (transmitted_packets.size() == 3) {
        std::cout << "  PASS (Heartbeat + Motor)" << std::endl;
    } else {
        std::cout << "  FAIL" << std::endl; return 1;
    }

    std::cout << "Test 2: Packet Encoding & CRC" << std::endl;
    auto last_pkt = transmitted_packets.back();
    if (last_pkt.size() == 9 && last_pkt[0] == 0xAA && last_pkt[1] == 0x55) {
        std::cout << "  PASS (Headers)" << std::endl;
    } else {
        std::cout << "  FAIL" << std::endl; return 1;
    }
    
    // Validate CRC of the last packet
    uint8_t crc = 0;
    for (int i=0; i<8; i++) crc ^= last_pkt[i];
    
    if (crc == last_pkt[8]) {
        std::cout << "  PASS (CRC Correct)" << std::endl;
    } else {
        std::cout << "  FAIL (CRC Incorrect)" << std::endl; return 1;
    }

    std::cout << "Test 3: Sequence Rollover" << std::endl;
    uint8_t seq1 = transmitted_packets[0][3];
    uint8_t seq2 = transmitted_packets[1][3];
    uint8_t seq3 = transmitted_packets[2][3];
    if (seq2 == (uint8_t)(seq1 + 1) && seq3 == (uint8_t)(seq2 + 1)) {
        std::cout << "  PASS" << std::endl;
    } else {
        std::cout << "  FAIL" << std::endl; return 1;
    }
    
    std::cout << "All telemetry tests passed successfully!" << std::endl;
    return 0;
}
