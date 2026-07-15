#pragma once

namespace ReconRover {
namespace Drivers {

class DriverHealth {
public:
    DriverHealth() : motor_fault_(false), i2c_fault_(false) {}

    void SetMotorFault(bool fault) { motor_fault_ = fault; }
    void SetI2CFault(bool fault) { i2c_fault_ = fault; }

    bool IsHealthy() const {
        return !motor_fault_ && !i2c_fault_;
    }

private:
    bool motor_fault_;
    bool i2c_fault_;
};

} // namespace Drivers
} // namespace ReconRover
