"""
Telemetry Health Module
Recon Rover V2 - Phase 2.3

Tracks packet loss, heartbeat timeouts, and latency statistics for the telemetry pipeline.
"""

import time
import threading

class TelemetryHealth:
    """
    Maintains runtime statistics for the serial/telemetry connection.
    """
    
    def __init__(self):
        self._lock = threading.RLock()
        self._last_heartbeat_time = 0.0
        self._last_sequence_num = -1
        self._total_packets_received = 0
        self._dropped_packets = 0
        
        # Latency tracking
        self._latest_latency_ms = 0.0
        
        self._start_time = time.time()
        
    def record_packet(self, sequence_num: int, timestamp_ms: int):
        """
        Updates tracking stats based on a newly decoded packet header.
        """
        with self._lock:
            self._total_packets_received += 1
            
            # Check for sequence skips (packet loss)
            if self._last_sequence_num != -1:
                expected = (self._last_sequence_num + 1) % 65535
                if sequence_num != expected:
                    # Simple heuristic: if we jumped ahead, we lost packets.
                    if sequence_num > expected:
                        self._dropped_packets += (sequence_num - expected)
                    else:
                        # Sequence wrapped around
                        pass
                        
            self._last_sequence_num = sequence_num
            
            # Simple latency calc if the ESP32 and RPi clocks are somehow synced,
            # or more likely, we just track round-trip on PINGs. For this phase,
            # we just track local time delta since last packet.
            self._latest_latency_ms = (time.time() - self._last_heartbeat_time) * 1000
            
    def record_heartbeat(self):
        """
        Logs that a valid heartbeat payload was received.
        """
        with self._lock:
            self._last_heartbeat_time = time.time()
            
    def get_statistics(self) -> dict:
        """
        Calculates and returns current telemetry health metrics.
        """
        with self._lock:
            now = time.time()
            uptime = now - self._start_time
            pps = self._total_packets_received / uptime if uptime > 0 else 0
            
            loss_pct = 0.0
            total_expected = self._total_packets_received + self._dropped_packets
            if total_expected > 0:
                loss_pct = (self._dropped_packets / total_expected) * 100.0
                
            time_since_hb = now - self._last_heartbeat_time if self._last_heartbeat_time > 0 else -1
            
            # Healthy if heartbeat seen in last 2 seconds and loss under 5%
            is_healthy = (0 <= time_since_hb < 2.0) and (loss_pct < 5.0)
            
            return {
                "packet_loss_pct": loss_pct,
                "latency_ms": self._latest_latency_ms,
                "packets_per_second": pps,
                "is_healthy": is_healthy,
                "time_since_heartbeat": time_since_hb
            }
