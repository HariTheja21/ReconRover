#pragma once
#include "runtime_events.h"

namespace ReconRover {
namespace Runtime {

class CommandDispatcher {
public:
    virtual ~CommandDispatcher() = default;

    // In a real ESP32 environment, this pushes to a FreeRTOS xQueue
    // For this generic backbone, we abstract the dispatch.
    virtual void Dispatch(const RuntimeEvent& event) = 0;
};

// Simple implementation for tests
class NullDispatcher : public CommandDispatcher {
public:
    void Dispatch(const RuntimeEvent& event) override {
        // Do nothing by default
    }
};

} // namespace Runtime
} // namespace ReconRover
