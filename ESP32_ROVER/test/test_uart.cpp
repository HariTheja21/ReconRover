#include <iostream>
#include <vector>
#include <iomanip>
#include "uart/uart_manager.h"

using namespace ReconRover::UART;

static std::vector<UartPacket> rx_packets;
static std::vector<uint8_t> tx_bytes;

void MockRxCallback(const UartPacket& packet) {
    rx_packets.push_back(packet);
}

void MockTxCallback(uint8_t byte) {
    tx_bytes.push_back(byte);
}

int main() {
    std::cout << "Starting ESP32 UART Integration Internal Tests..." << std::endl;

    UartManager manager(MockRxCallback, MockTxCallback);
    manager.Init();

    std::cout << "Test 1: RX Packet Framing" << std::endl;
    // Simulate incoming command packet from Raspberry Pi
    uint8_t raw_rx[] = {0xAA, 0x55, 0x01, 0x00, 0x11, 0x22, 0x33, 0x44, 0x00};
    // Fix CRC for valid packet
    uint8_t crc = 0;
    for(int i=0; i<8; i++) crc ^= raw_rx[i];
    raw_rx[8] = crc;

    for(int i=0; i<9; i++) {
        manager.OnIsrByteReceived(raw_rx[i]);
    }

    if (rx_packets.size() == 1 && rx_packets[0].buffer[0] == 0xAA && rx_packets[0].buffer[1] == 0x55) {
        std::cout << "  PASS" << std::endl;
    } else {
        std::cout << "  FAIL" << std::endl; return 1;
    }

    std::cout << "Test 2: TX Buffer Queuing" << std::endl;
    UartPacket tx_pkt;
    tx_pkt.length = 9;
    for (int i=0; i<9; i++) tx_pkt.buffer[i] = i;
    
    manager.EnqueueTelemetryPacket(tx_pkt);
    
    // Nothing should be in tx_bytes until Tick() is called
    if (tx_bytes.size() == 0) {
        std::cout << "  PASS (Queued properly)" << std::endl;
    } else {
        std::cout << "  FAIL" << std::endl; return 1;
    }

    std::cout << "Test 3: TX Byte Flushing" << std::endl;
    manager.Tick(0);
    
    if (tx_bytes.size() == 9) {
        std::cout << "  PASS (Flushed 9 bytes)" << std::endl;
    } else {
        std::cout << "  FAIL" << std::endl; return 1;
    }

    std::cout << "Test 4: Framing Error Recovery" << std::endl;
    manager.OnIsrByteReceived(0xAA);
    manager.OnIsrByteReceived(0x00); // Invalid header 2 (not 0x55)
    manager.OnIsrByteReceived(0xAA);
    manager.OnIsrByteReceived(0x55);
    manager.OnIsrByteReceived(0x01);
    manager.OnIsrByteReceived(0x00);
    manager.OnIsrByteReceived(0x11);
    manager.OnIsrByteReceived(0x22);
    manager.OnIsrByteReceived(0x33);
    manager.OnIsrByteReceived(0x44);
    manager.OnIsrByteReceived(crc); // Reusing same crc for same payload
    
    if (rx_packets.size() == 2) {
        std::cout << "  PASS (Recovered from bad frame)" << std::endl;
    } else {
        std::cout << "  FAIL" << std::endl; return 1;
    }

    std::cout << "All UART tests passed successfully!" << std::endl;
    return 0;
}
