/**
 * @file sensor_manager.h
 * @brief Recon Rover V1 - Sensor Manager
 *
 * Manages the initialization, periodic polling, and data aggregation
 * of all hardware sensors.
 */

#ifndef ROVER_SENSOR_MANAGER_H
#define ROVER_SENSOR_MANAGER_H

#include "driver_mpu6050.h"
#include "driver_vl53l0x.h"
#include "driver_hcsr04.h"
#include "driver_mq2.h"
#include "driver_ina219.h"

#include "types_sensor.h"
#include "health_system.h"
#include "error_system.h"

namespace rover {

/**
 * @class SensorManager
 * @brief Plain C++ class that owns and orchestrates sensor drivers.
 */
class SensorManager {
public:
    /**
     * @brief Constructs the manager and injects dependencies.
     */
    SensorManager(driver::DriverMpu6050* mpu,
                  driver::DriverVl53l0x* tof1,
                  driver::DriverVl53l0x* tof2,
                  driver::DriverHcsr04* sonar_front,
                  driver::DriverHcsr04* sonar_back,
                  driver::DriverHcsr04* sonar_left,
                  driver::DriverHcsr04* sonar_right,
                  driver::DriverMq2* gas,
                  driver::DriverIna219* ina);

    /**
     * @brief Initializes all sensor hardware.
     */
    void init();

    /**
     * @brief Polls sensors that are due for reading based on elapsed time.
     * @param current_time_ms The current system time in ms.
     */
    void update(uint32_t current_time_ms);

    // Getters for latest aggregated data
    const IMUData& getImuData() const;
    const ToFData& getToF1Data() const;
    const ToFData& getToF2Data() const;
    const UltrasonicData& getSonarFrontData() const;
    const UltrasonicData& getSonarBackData() const;
    const UltrasonicData& getSonarLeftData() const;
    const UltrasonicData& getSonarRightData() const;
    const GasData& getGasData() const;
    const PowerData& getPowerData() const;
    const SensorHealth& getSensorHealth() const;
    const PowerHealth& getPowerHealth() const;

private:
    // Drivers
    driver::DriverMpu6050* m_mpu;
    driver::DriverVl53l0x* m_tof1;
    driver::DriverVl53l0x* m_tof2;
    driver::DriverHcsr04* m_sonar_front;
    driver::DriverHcsr04* m_sonar_back;
    driver::DriverHcsr04* m_sonar_left;
    driver::DriverHcsr04* m_sonar_right;
    driver::DriverMq2* m_gas;
    driver::DriverIna219* m_ina;

    // Data buffers
    IMUData m_imu_data;
    ToFData m_tof1_data;
    ToFData m_tof2_data;
    UltrasonicData m_sonar_f_data;
    UltrasonicData m_sonar_b_data;
    UltrasonicData m_sonar_l_data;
    UltrasonicData m_sonar_r_data;
    GasData m_gas_data;
    PowerData m_power_data;

    // Health structs
    SensorHealth m_sensor_health;
    PowerHealth m_power_health;

    // Timing state
    uint32_t m_last_imu_ms;
    uint32_t m_last_tof_ms;
    uint32_t m_last_sonar_ms;
    uint32_t m_last_gas_ms;
    uint32_t m_last_power_ms;

    void updateDeviceHealth(DeviceHealth& health, const hal::HalStatus& status, uint32_t current_time_ms);
};

} // namespace rover

#endif // ROVER_SENSOR_MANAGER_H
