#include <iostream>
#include "drivers/driver_manager.h"

using namespace ReconRover::Drivers;
using namespace ReconRover::Runtime;

int main() {
    std::cout << "Starting ESP32 Hardware Drivers Internal Tests..." << std::endl;

    DriverManager manager;
    manager.InitAll();
    auto& stats = manager.GetStatistics();

    std::cout << "Test 1: Motor Direction & PWM Scaling" << std::endl;
    MotorCommandEvent motor_cmd = { 16383, -16383 }; // ~50% forward left, ~50% backward right
    manager.HandleMotorCommand(motor_cmd);
    if (stats.motor_commands_executed == 1) {
        std::cout << "  PASS" << std::endl;
    } else {
        std::cout << "  FAIL" << std::endl; return 1;
    }

    std::cout << "Test 2: Servo Angle Limiting" << std::endl;
    ServoCommandEvent servo_cmd = { 0, 90 };
    manager.HandleServoCommand(servo_cmd);
    if (stats.servo_commands_executed == 1) {
        std::cout << "  PASS" << std::endl;
    } else {
        std::cout << "  FAIL" << std::endl; return 1;
    }

    std::cout << "Test 3: OLED Updates" << std::endl;
    OLEDCommandEvent oled_cmd = { 1 };
    manager.HandleOLEDCommand(oled_cmd);
    if (stats.oled_updates == 1) {
        std::cout << "  PASS" << std::endl;
    } else {
        std::cout << "  FAIL" << std::endl; return 1;
    }

    std::cout << "Test 4: RGB Colors" << std::endl;
    RGBCommandEvent rgb_cmd = { 255, 128, 0 };
    manager.HandleRGBCommand(rgb_cmd);
    if (stats.rgb_updates == 1) {
        std::cout << "  PASS" << std::endl;
    } else {
        std::cout << "  FAIL" << std::endl; return 1;
    }

    std::cout << "Test 5: Buzzer Tones" << std::endl;
    BuzzerCommandEvent buzzer_cmd = { 440, 1000 };
    manager.HandleBuzzerCommand(buzzer_cmd);
    if (stats.buzzer_tones == 1) {
        std::cout << "  PASS" << std::endl;
    } else {
        std::cout << "  FAIL" << std::endl; return 1;
    }

    std::cout << "Test 6: Emergency Stop Overrides" << std::endl;
    EmergencyStopEvent estop_cmd = { 99 };
    manager.HandleEmergencyStop(estop_cmd);
    if (stats.estops_triggered == 1 && stats.rgb_updates == 2 && stats.buzzer_tones == 2) {
        std::cout << "  PASS" << std::endl;
    } else {
        std::cout << "  FAIL" << std::endl; return 1;
    }

    std::cout << "All driver tests passed successfully!" << std::endl;
    return 0;
}
