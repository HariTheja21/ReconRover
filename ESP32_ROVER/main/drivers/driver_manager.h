#pragma once
#include "../runtime/runtime_events.h"
#include "motor_driver.h"
#include "servo_driver.h"
#include "oled_driver.h"
#include "rgb_driver.h"
#include "buzzer_driver.h"
#include "driver_health.h"

namespace ReconRover {
namespace Drivers {

// The DriverManager binds the abstract RuntimeEvents to concrete driver instances.
class DriverManager {
public:
    DriverManager();

    void InitAll();

    // Event handlers mapping RuntimeEvents to driver operations
    void HandleMotorCommand(const Runtime::MotorCommandEvent& event);
    void HandleServoCommand(const Runtime::ServoCommandEvent& event);
    void HandleOLEDCommand(const Runtime::OLEDCommandEvent& event);
    void HandleRGBCommand(const Runtime::RGBCommandEvent& event);
    void HandleBuzzerCommand(const Runtime::BuzzerCommandEvent& event);
    void HandleEmergencyStop(const Runtime::EmergencyStopEvent& event);

    DriverStatistics& GetStatistics() { return stats_; }
    DriverHealth& GetHealth() { return health_; }

private:
    DriverStatistics stats_;
    DriverHealth health_;
    
    MotorDriver motor_driver_;
    ServoDriver servo_driver_;
    OLEDDriver oled_driver_;
    RGBDriver rgb_driver_;
    BuzzerDriver buzzer_driver_;
};

} // namespace Drivers
} // namespace ReconRover
