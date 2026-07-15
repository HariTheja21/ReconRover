#include "runtime_manager.h"

namespace ReconRover {
namespace Runtime {

RuntimeManager::RuntimeManager(CommandDispatcher& dispatcher)
    : engine_(dispatcher) {}

void RuntimeManager::Init() {
    // UART initialization would happen here.
}

void RuntimeManager::OnUartData(const uint8_t* data, size_t length, uint32_t current_time_ms) {
    if (length > 0) {
        health_.RecordPacketArrival(current_time_ms);
        engine_.ProcessIncomingBytes(data, length);
    }
}

void RuntimeManager::Tick(uint32_t current_time_ms) {
    health_.UpdateHealth(current_time_ms);
    // In a real system, this tick might also pull from the dispatcher queue
    // to execute physical hardware commands if this task is unified,
    // or simply monitor health.
}

} // namespace Runtime
} // namespace ReconRover
