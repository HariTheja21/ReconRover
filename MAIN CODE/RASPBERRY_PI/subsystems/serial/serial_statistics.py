"""
serial_statistics.py
Recon Rover V1 - Serial Communication Manager

Tracks immutable snapshots of connection metrics.
"""

from dataclasses import dataclass
import time

@dataclass
class SerialStatsSnapshot:
    rx_packets: int = 0
    tx_packets: int = 0
    rx_bytes: int = 0
    tx_bytes: int = 0
    crc_failures: int = 0
    dropped_packets: int = 0
    reconnects: int = 0
    uptime_sec: float = 0.0

class SerialStatistics:
    def __init__(self):
        self._rx_packets = 0
        self._tx_packets = 0
        self._rx_bytes = 0
        self._tx_bytes = 0
        self._crc_failures = 0
        self._dropped_packets = 0
        self._reconnects = 0
        self._start_time = time.time()

    def record_rx(self, bytes_len: int):
        self._rx_packets += 1
        self._rx_bytes += bytes_len

    def record_tx(self, bytes_len: int):
        self._tx_packets += 1
        self._tx_bytes += bytes_len

    def record_crc_failure(self):
        self._crc_failures += 1

    def record_dropped(self):
        self._dropped_packets += 1

    def record_reconnect(self):
        self._reconnects += 1
        self._start_time = time.time()  # reset uptime on reconnect

    def get_snapshot(self) -> SerialStatsSnapshot:
        return SerialStatsSnapshot(
            rx_packets=self._rx_packets,
            tx_packets=self._tx_packets,
            rx_bytes=self._rx_bytes,
            tx_bytes=self._tx_bytes,
            crc_failures=self._crc_failures,
            dropped_packets=self._dropped_packets,
            reconnects=self._reconnects,
            uptime_sec=time.time() - self._start_time
        )
