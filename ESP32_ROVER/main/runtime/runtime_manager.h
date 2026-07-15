#pragma once
#include "runtime_engine.h"
#include "runtime_health.h"

namespace ReconRover {
namespace Runtime {

// Simulates the FreeRTOS task manager for the Runtime Core.
// In actual ESP-IDF, this will contain xTaskCreate, Queue handles, and UART driver calls.
class RuntimeManager {
public:
    RuntimeManager(CommandDispatcher& dispatcher);

    // Initialization routine
    void Init();

    // Main loop iteration (called repeatedly or inside a FreeRTOS task)
    void Tick(uint32_t current_time_ms);

    // Inject bytes (normally called by the UART ISR or UART Read Task)
    void OnUartData(const uint8_t* data, size_t length, uint32_t current_time_ms);

    RuntimeEngine& GetEngine() { return engine_; }
    RuntimeHealth& GetHealth() { return health_; }

private:
    RuntimeEngine engine_;
    RuntimeHealth health_;
};

} // namespace Runtime
} // namespace ReconRover
