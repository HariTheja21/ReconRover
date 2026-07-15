# Phase 4.3: Serial Transport Layer - Implementation Plan

## Executive Summary
Phase 4.3 constitutes the final software boundary on the Raspberry Pi: The Serial Transport Layer. This module is responsible exclusively for the literal, physical transmission of verified binary packets across UART/SPI boundaries to the downstream microcontrollers (e.g., ESP32), and the reception of hardware telemetry.

## Objectives
- Implement `SerialPort` to establish a non-blocking asynchronous connection to `/dev/serial0`.
- Develop `SerialTransportManager` running at $50$Hz ($0.02s$ loop) to coordinate rapid UART TX/RX cycles.
- Create a `PacketSender` with queue manipulation that forces `HardwareStopPacket` (E-Stop) to the immediate front of the transmission line.
- Create a `PacketReceiver` combined with a `PacketFramer` to ingest stream fragments and parse valid `0xAA55` packets safely without blocking.

## Architecture
- `serial_transport_manager.py`: The 50Hz daemon orchestrating EventBus $\leftrightarrow$ UART translation.
- `serial_transport_engine.py`: Manages the physical connection and invokes the sender/receiver pipelines.
- `serial_port.py`: A non-blocking wrapper around the `pyserial` library.
- `packet_sender.py`: Thread-safe FIFO queue with a `force_front` override for Emergency Stops.
- `packet_receiver.py` & `packet_buffer.py`: Reassembles chunked UART streams into complete payloads.
- `packet_framer.py`: Scans byte arrays for headers and extracts exact 9-byte frames.

## Error Handling & Recovery
1. **Auto-Reconnect:** If the physical wire is pulled, `serial_port.py` throws an exception, unlatching the connection state. The manager will loop, wait 1.0 second, and re-attempt the connection indefinitely.
2. **Buffer Bloat:** `packet_sender.py` imposes a hard cap (100 packets). If the queue fills (e.g., disconnected hardware), it silently drops the oldest packet to guarantee the most recent target is eventually sent.
3. **Framing Errors:** If the hardware sends malformed data (noise on the SPI/UART line), `PacketFramer` drops unrecognized bytes up to the next valid `0xAA55` header, preventing indefinite lock-up.

## EventBus Integration
**Consumes:** `HardwareCommandPacket`, `HardwareStopPacket`
**Publishes:** `SerialPacketSent`, `SerialPacketReceived`, `SerialConnected`, `SerialDisconnected`, `SerialHealthUpdated`
