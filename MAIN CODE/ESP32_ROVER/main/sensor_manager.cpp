/**
 * @file sensor_manager.cpp
 * @brief Recon Rover V1 - Sensor Manager
 */

#include "sensor_manager.h"
#include "config.h"

namespace rover {

SensorManager::SensorManager(driver::DriverMpu6050* mpu,
                             driver::DriverVl53l0x* tof1, driver::DriverVl53l0x* tof2,
                             driver::DriverHcsr04* sonar_front, driver::DriverHcsr04* sonar_back,
                             driver::DriverHcsr04* sonar_left, driver::DriverHcsr04* sonar_right,
                             driver::DriverMq2* gas, driver::DriverIna219* ina)
    : m_mpu(mpu), m_tof1(tof1), m_tof2(tof2),
      m_sonar_front(sonar_front), m_sonar_back(sonar_back), 
      m_sonar_left(sonar_left), m_sonar_right(sonar_right),
      m_gas(gas), m_ina(ina),
      m_last_imu_ms(0), m_last_tof_ms(0), m_last_sonar_ms(0),
      m_last_gas_ms(0), m_last_power_ms(0) {
    
    m_sensor_health = {};
    m_power_health = {};
}

void SensorManager::init() {
    if (m_mpu) m_mpu->init();
    if (m_tof1) m_tof1->init();
    if (m_tof2) m_tof2->init();
    if (m_sonar_front) m_sonar_front->init();
    if (m_sonar_back) m_sonar_back->init();
    if (m_sonar_left) m_sonar_left->init();
    if (m_sonar_right) m_sonar_right->init();
    if (m_gas) m_gas->init();
    if (m_ina) m_ina->init();
}

void SensorManager::updateDeviceHealth(DeviceHealth& health, const hal::HalStatus& status, uint32_t current_time_ms) {
    health.last_check_ms = current_time_ms;
    health.is_online = status.isOk();
    if (!health.is_online) {
        health.failure_count++;
    }
}

void SensorManager::update(uint32_t current_time_ms) {
    
    // IMU Polling
    if (current_time_ms - m_last_imu_ms >= config::POLL_RATE_IMU_MS) {
        m_last_imu_ms = current_time_ms;
        if (m_mpu) {
            driver::Mpu6050Data raw;
            hal::HalStatus st = m_mpu->readAll(raw);
            updateDeviceHealth(m_sensor_health.mpu6050, st, current_time_ms);
            if (st.isOk()) {
                m_imu_data.accel_x_g = raw.accel_x_g;
                m_imu_data.accel_y_g = raw.accel_y_g;
                m_imu_data.accel_z_g = raw.accel_z_g;
                m_imu_data.gyro_x_dps = raw.gyro_x_dps;
                m_imu_data.gyro_y_dps = raw.gyro_y_dps;
                m_imu_data.gyro_z_dps = raw.gyro_z_dps;
                m_imu_data.temp_c = raw.temp_c;
            }
        }
    }

    // ToF Polling
    if (current_time_ms - m_last_tof_ms >= config::POLL_RATE_TOF_MS) {
        m_last_tof_ms = current_time_ms;
        // In a real system, we'd use non-blocking continuous reads here. 
        // For now, we mock the call flow.
        if (m_tof1) {
            hal::HalStatus st = m_tof1->readRangeContinuousMillimeters(m_tof1_data.distance_mm, 10);
            updateDeviceHealth(m_sensor_health.vl53l0x, st, current_time_ms);
            m_tof1_data.valid = st.isOk();
        }
    }

    // Sonar Polling
    if (current_time_ms - m_last_sonar_ms >= config::POLL_RATE_SONAR_MS) {
        m_last_sonar_ms = current_time_ms;
        if (m_sonar_front) {
            hal::HalStatus st = m_sonar_front->measureDistanceCm(m_sonar_f_data.distance_cm);
            updateDeviceHealth(m_sensor_health.hcsr04, st, current_time_ms);
            m_sonar_f_data.valid = st.isOk();
        }
    }

    // Gas Polling
    if (current_time_ms - m_last_gas_ms >= config::POLL_RATE_GAS_MS) {
        m_last_gas_ms = current_time_ms;
        if (m_gas) {
            int mv = 0;
            hal::HalStatus st = m_gas->readVoltage(mv);
            updateDeviceHealth(m_sensor_health.mq2, st, current_time_ms);
            if (st.isOk()) {
                m_gas_data.voltage_mv = mv;
                m_gas->readRaw(m_gas_data.raw_adc);
                m_gas->isHazardDetected(config::MQ2_HAZARD_THRESHOLD_MV, m_gas_data.hazard_detected);
            }
        }
    }

    // Power Polling
    if (current_time_ms - m_last_power_ms >= config::POLL_RATE_POWER_MS) {
        m_last_power_ms = current_time_ms;
        if (m_ina) {
            hal::HalStatus st = m_ina->getBusVoltage_V(m_power_data.bus_voltage_v);
            m_ina->getCurrent_mA(m_power_data.current_ma);
            m_ina->getPower_mW(m_power_data.power_mw);
            m_ina->getShuntVoltage_mV(m_power_data.shunt_mv);
            
            updateDeviceHealth(m_power_health.ina219, st, current_time_ms);
            m_power_health.battery_low = (m_power_data.bus_voltage_v < config::INA219_MIN_BUS_VOLTAGE_V);
            m_power_health.overcurrent = (m_power_data.current_ma > config::INA219_MAX_CURRENT_MA);
        }
    }
}

const IMUData& SensorManager::getImuData() const { return m_imu_data; }
const ToFData& SensorManager::getToF1Data() const { return m_tof1_data; }
const ToFData& SensorManager::getToF2Data() const { return m_tof2_data; }
const UltrasonicData& SensorManager::getSonarFrontData() const { return m_sonar_f_data; }
const UltrasonicData& SensorManager::getSonarBackData() const { return m_sonar_b_data; }
const UltrasonicData& SensorManager::getSonarLeftData() const { return m_sonar_l_data; }
const UltrasonicData& SensorManager::getSonarRightData() const { return m_sonar_r_data; }
const GasData& SensorManager::getGasData() const { return m_gas_data; }
const PowerData& SensorManager::getPowerData() const { return m_power_data; }
const SensorHealth& SensorManager::getSensorHealth() const { return m_sensor_health; }
const PowerHealth& SensorManager::getPowerHealth() const { return m_power_health; }

} // namespace rover
