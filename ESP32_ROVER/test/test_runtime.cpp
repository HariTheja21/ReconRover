#include <iostream>
#include <vector>
#include "runtime/runtime_manager.h"

using namespace ReconRover::Runtime;

// Mock Dispatcher to capture events
class TestDispatcher : public CommandDispatcher {
public:
    std::vector<RuntimeEvent> events;

    void Dispatch(const RuntimeEvent& event) override {
        events.push_back(event);
    }
};

int main() {
    std::cout << "Starting ESP32 Runtime Core Internal Tests..." << std::endl;

    TestDispatcher dispatcher;
    RuntimeManager manager(dispatcher);
    manager.Init();

    // Utility to run bytes
    auto send_bytes = [&](const std::vector<uint8_t>& bytes, uint32_t time_ms = 0) {
        manager.OnUartData(bytes.data(), bytes.size(), time_ms);
    };

    std::cout << "Test 1: Valid Packet Routing" << std::endl;
    // Header AA 55 | Cmd 01 | Seq 00 | Left 7F FF | Right 7F FF | CRC (computed)
    // 7F ^ FF ^ 7F ^ FF = 00.
    // Wait, CRC calculation includes headers.
    // 0xAA ^ 0x55 ^ 0x01 ^ 0x00 ^ 0x7F ^ 0xFF ^ 0x7F ^ 0xFF
    // AA ^ 55 = FF. FF ^ 01 = FE. FE ^ 00 = FE. FE ^ 7F = 81. 81 ^ FF = 7E. 7E ^ 7F = 01. 01 ^ FF = FE.
    std::vector<uint8_t> valid_packet = {0xAA, 0x55, 0x01, 0x00, 0x7F, 0xFF, 0x7F, 0xFF, 0xFE};
    send_bytes(valid_packet);

    if (dispatcher.events.size() == 1 && 
        dispatcher.events[0].type == EventType::MOTOR_COMMAND &&
        dispatcher.events[0].payload.motor.left_velocity == 32767) {
        std::cout << "  PASS" << std::endl;
    } else {
        std::cout << "  FAIL" << std::endl;
        return 1;
    }

    std::cout << "Test 2: Invalid CRC Rejection" << std::endl;
    std::vector<uint8_t> bad_crc_packet = {0xAA, 0x55, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0xFF}; // Wrong CRC
    send_bytes(bad_crc_packet);
    if (dispatcher.events.size() == 1 && manager.GetEngine().GetStatistics().packets_invalid_crc == 1) {
        std::cout << "  PASS" << std::endl;
    } else {
        std::cout << "  FAIL" << std::endl;
        return 1;
    }

    std::cout << "Test 3: Duplicate Sequence Rejection" << std::endl;
    // Resend the valid packet with seq 00
    send_bytes(valid_packet);
    if (dispatcher.events.size() == 1 && manager.GetEngine().GetStatistics().packets_dropped_duplicate == 1) {
        std::cout << "  PASS" << std::endl;
    } else {
        std::cout << "  FAIL" << std::endl;
        return 1;
    }

    std::cout << "Test 4: Fragmented Packet Reassembly" << std::endl;
    // Next valid packet, Seq = 02.
    // AA ^ 55 = FF. FF ^ 01 = FE. FE ^ 02 = FC. FC ^ 00 ^ 00 ^ 00 ^ 00 = FC.
    std::vector<uint8_t> frag1 = {0xAA, 0x55, 0x01, 0x02};
    std::vector<uint8_t> frag2 = {0x00, 0x00, 0x00, 0x00, 0xFC};
    send_bytes(frag1);
    // Should be no event yet
    if (dispatcher.events.size() == 1) {
        send_bytes(frag2);
        if (dispatcher.events.size() == 2) {
            std::cout << "  PASS" << std::endl;
        } else {
            std::cout << "  FAIL (Not reassembled)" << std::endl;
            return 1;
        }
    } else {
        std::cout << "  FAIL (Premature dispatch)" << std::endl;
        return 1;
    }

    std::cout << "Test 5: Runtime Health Timeout" << std::endl;
    manager.Tick(1500); // 1.5 seconds later
    if (!manager.GetHealth().IsHealthy()) {
        std::cout << "  PASS" << std::endl;
    } else {
        std::cout << "  FAIL" << std::endl;
        return 1;
    }

    std::cout << "All tests passed successfully!" << std::endl;
    return 0;
}
