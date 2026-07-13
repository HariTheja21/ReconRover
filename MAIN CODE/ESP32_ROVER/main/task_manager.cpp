/**
 * @file task_manager.cpp
 * @brief Recon Rover V1 - RTOS Task Manager
 */

#include "task_manager.h"
#include "rtos_config.h"
#include "system_clock.h"

// Managers and Drivers needed for local instantiation
#include "sensor_manager.h"
#include "motor_manager.h"
#include "servo_manager.h"
#include "oled_manager.h"
#include "led_manager.h"
#include "health_manager.h"

// Communication layer
#include "protocol_serializer.h"
#include "protocol_deserializer.h"
#include "command_router.h"
#include "telemetry_router.h"
#include "packet_validator.h"

namespace rover {
namespace rtos {

TaskManager::TaskManager(QueueManager* q, WatchdogRegistry* w, ConfigurationManager* c)
    : m_queue(q), m_watchdog(w), m_config(c),
      t_watchdog(nullptr), t_serial(nullptr), t_motor(nullptr),
      t_sensor(nullptr), t_servo(nullptr), t_oled(nullptr),
      t_led(nullptr), t_telemetry(nullptr), t_health(nullptr),
      t_fault(nullptr) {
    m_ctx.queue = m_queue;
    m_ctx.watchdog = m_watchdog;
    m_ctx.config = m_config;
}

TaskManager::~TaskManager() {
    shutdownAllTasks();
}

bool TaskManager::spawnAllTasks() {
    BaseType_t res = pdPASS;

    // Spawn order is critical. Fault and Watchdog start first.
    res &= xTaskCreatePinnedToCore(watchdogTask, "Watchdog", STACK_WATCHDOG, &m_ctx, PRIORITY_WATCHDOG, &t_watchdog, CORE_0);
    res &= xTaskCreatePinnedToCore(faultTask, "Fault", STACK_FAULT, &m_ctx, PRIORITY_FAULT, &t_fault, CORE_0);

    // High Priority Control
    res &= xTaskCreatePinnedToCore(motorTask, "Motor", STACK_MOTOR, &m_ctx, PRIORITY_MOTOR, &t_motor, CORE_1);
    res &= xTaskCreatePinnedToCore(serialTask, "Serial", STACK_SERIAL, &m_ctx, PRIORITY_SERIAL, &t_serial, CORE_0);
    
    // Core Sensing
    res &= xTaskCreatePinnedToCore(sensorTask, "Sensor", STACK_SENSOR, &m_ctx, PRIORITY_SENSOR, &t_sensor, CORE_1);
    
    // Lower Priority Output
    res &= xTaskCreatePinnedToCore(servoTask, "Servo", STACK_SERVO, &m_ctx, PRIORITY_SERVO, &t_servo, CORE_1);
    res &= xTaskCreatePinnedToCore(oledTask, "OLED", STACK_OLED, &m_ctx, PRIORITY_OLED, &t_oled, CORE_0);
    res &= xTaskCreatePinnedToCore(ledTask, "LED", STACK_LED, &m_ctx, PRIORITY_LED, &t_led, CORE_0);
    
    // Background / Aggregation
    res &= xTaskCreatePinnedToCore(telemetryTask, "Telemetry", STACK_TELEMETRY, &m_ctx, PRIORITY_TELEMETRY, &t_telemetry, CORE_0);
    res &= xTaskCreatePinnedToCore(healthTask, "Health", STACK_HEALTH, &m_ctx, PRIORITY_HEALTH, &t_health, CORE_0);

    return (res == pdPASS);
}

void TaskManager::shutdownAllTasks() {
    // Reverse shutdown order to prevent dependency failures during teardown
    if (t_health) { vTaskDelete(t_health); t_health = nullptr; }
    if (t_telemetry) { vTaskDelete(t_telemetry); t_telemetry = nullptr; }
    
    if (t_led) { vTaskDelete(t_led); t_led = nullptr; }
    if (t_oled) { vTaskDelete(t_oled); t_oled = nullptr; }
    if (t_servo) { vTaskDelete(t_servo); t_servo = nullptr; }
    
    if (t_sensor) { vTaskDelete(t_sensor); t_sensor = nullptr; }
    if (t_serial) { vTaskDelete(t_serial); t_serial = nullptr; }
    if (t_motor) { vTaskDelete(t_motor); t_motor = nullptr; }
    
    if (t_fault) { vTaskDelete(t_fault); t_fault = nullptr; }
    if (t_watchdog) { vTaskDelete(t_watchdog); t_watchdog = nullptr; }
}

// =========================================================================
// Task Implementations
// =========================================================================

void TaskManager::watchdogTask(void* pvParameters) {
    TaskContext* ctx = static_cast<TaskContext*>(pvParameters);
    TickType_t last_wake = xTaskGetTickCount();
    
    while (1) {
        TaskId failed;
        if (!ctx->watchdog->checkAllTasks(SystemClock::millis(), failed)) {
            // A task missed its heartbeat. For now, report via SystemQueue (or FaultQueue)
            FaultEvent evt = {};
            evt.type = FaultType::SOFTWARE_STALL;
            evt.severity = FaultSeverity::CRITICAL;
            ctx->queue->sendFaultEvent(evt, 0);
        }
        vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(PERIOD_WATCHDOG_MS));
    }
}

void TaskManager::serialTask(void* pvParameters) {
    TaskContext* ctx = static_cast<TaskContext*>(pvParameters);
    comms::CommandRouter router(ctx->queue);
    
    ctx->watchdog->registerTask(TaskId::SERIAL, PERIOD_SERIAL_MS * 5);
    TickType_t last_wake = xTaskGetTickCount();
    
    char rx_buffer[comms::PacketValidator::MAX_PACKET_SIZE];
    size_t rx_idx = 0;
    
    while (1) {
        // Read incoming bytes (mocked CDC HAL read)
        // int c;
        // while ((c = hal_cdc_read_char()) >= 0 && rx_idx < sizeof(rx_buffer)) {
        //     rx_buffer[rx_idx++] = static_cast<char>(c);
        //     if (c == '$') { // End of frame
        //         CommandPacket cmd;
        //         if (comms::ProtocolDeserializer::deserializeCommand(rx_buffer, rx_idx, cmd)) {
        //             router.route(cmd);
        //         }
        //         rx_idx = 0;
        //     }
        // }
        
        TelemetryPacket packet;
        if (ctx->queue->receiveTelemetryEvent(packet, 0)) {
            std::string serialized = comms::ProtocolSerializer::serializeTelemetry(packet);
            // hal_cdc_write(serialized.c_str(), serialized.length());
        }
        
        ctx->watchdog->checkIn(TaskId::SERIAL);
        vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(PERIOD_SERIAL_MS));
    }
}

void TaskManager::motorTask(void* pvParameters) {
    TaskContext* ctx = static_cast<TaskContext*>(pvParameters);
    
    driver::DriverL298N driver;
    MotorManager manager(&driver, ctx->config);
    manager.init();
    
    ctx->watchdog->registerTask(TaskId::MOTOR, PERIOD_MOTOR_MS * 5);
    
    while (1) {
        CommandEvent cmd;
        if (ctx->queue->receiveMotorEvent(cmd, pdMS_TO_TICKS(PERIOD_MOTOR_MS))) {
            if (cmd.type == CommandType::MOVE_VELOCITY) {
                manager.setSpeed(cmd.payload.velocity.left, cmd.payload.velocity.right);
            } else if (cmd.type == CommandType::EMERGENCY_STOP) {
                manager.emergencyStop();
            }
        }
        ctx->watchdog->checkIn(TaskId::MOTOR);
    }
}

void TaskManager::sensorTask(void* pvParameters) {
    TaskContext* ctx = static_cast<TaskContext*>(pvParameters);
    
    driver::DriverMpu6050 mpu;
    driver::DriverVl53l0x tof1(0x29);
    driver::DriverVl53l0x tof2(0x29); // Real addresses would be remapped
    driver::DriverHcsr04 sonar_f, sonar_b, sonar_l, sonar_r;
    driver::DriverMq2 gas;
    driver::DriverIna219 ina;
    
    SensorManager manager(&mpu, &tof1, &tof2, &sonar_f, &sonar_b, &sonar_l, &sonar_r, &gas, &ina);
    manager.init();
    
    ctx->watchdog->registerTask(TaskId::SENSOR, PERIOD_SENSOR_MS * 5);
    TickType_t last_wake = xTaskGetTickCount();
    
    while (1) {
        manager.update(SystemClock::millis());
        
        SensorEvent evt;
        evt.timestamp_ms = SystemClock::millis();
        evt.imu = manager.getImuData();
        evt.tof_front = manager.getToF1Data();
        evt.gas = manager.getGasData();
        // Pack other sensors...
        
        ctx->queue->sendSensorEvent(evt, 0);
        
        ctx->watchdog->checkIn(TaskId::SENSOR);
        vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(PERIOD_SENSOR_MS));
    }
}

void TaskManager::servoTask(void* pvParameters) {
    TaskContext* ctx = static_cast<TaskContext*>(pvParameters);
    
    driver::DriverServo pan;
    driver::DriverServo tilt;
    ServoManager manager(&pan, &tilt);
    manager.init();
    
    ctx->watchdog->registerTask(TaskId::SERVO, PERIOD_SERVO_MS * 5);
    
    while (1) {
        CommandEvent cmd;
        if (ctx->queue->receiveServoEvent(cmd, pdMS_TO_TICKS(PERIOD_SERVO_MS))) {
            if (cmd.type == CommandType::SET_PAN_TILT) {
                manager.setPan(cmd.payload.servo.pan_deg);
                manager.setTilt(cmd.payload.servo.tilt_deg);
            }
        }
        ctx->watchdog->checkIn(TaskId::SERVO);
    }
}

void TaskManager::oledTask(void* pvParameters) {
    TaskContext* ctx = static_cast<TaskContext*>(pvParameters);
    
    driver::DriverPca9548a mux;
    driver::DriverSsd1306 left_eye, right_eye;
    OLEDManager manager(&mux, &left_eye, &right_eye, 0, 1);
    manager.init();
    
    ctx->watchdog->registerTask(TaskId::OLED, PERIOD_OLED_MS * 5);
    TickType_t last_wake = xTaskGetTickCount();
    
    while (1) {
        CommandEvent cmd;
        if (ctx->queue->receiveOledEvent(cmd, 0)) {
            // Process OLED commands (e.g., blink eyes)
        }
        
        manager.update();
        
        ctx->watchdog->checkIn(TaskId::OLED);
        vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(PERIOD_OLED_MS));
    }
}

void TaskManager::ledTask(void* pvParameters) {
    TaskContext* ctx = static_cast<TaskContext*>(pvParameters);
    
    driver::DriverWs2812 strip;
    LEDManager manager(&strip, 10); // Assume 10 LEDs
    manager.init();
    
    ctx->watchdog->registerTask(TaskId::LED, PERIOD_LED_MS * 5);
    TickType_t last_wake = xTaskGetTickCount();
    
    while (1) {
        CommandEvent cmd;
        if (ctx->queue->receiveLedEvent(cmd, 0)) {
            if (cmd.type == CommandType::SET_LED_MODE) {
                manager.runAnimation(cmd.payload.led.mode);
                manager.setColor(cmd.payload.led.r, cmd.payload.led.g, cmd.payload.led.b);
            }
        }
        
        manager.tick();
        
        ctx->watchdog->checkIn(TaskId::LED);
        vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(PERIOD_LED_MS));
    }
}

void TaskManager::telemetryTask(void* pvParameters) {
    TaskContext* ctx = static_cast<TaskContext*>(pvParameters);
    comms::TelemetryRouter router;
    
    ctx->watchdog->registerTask(TaskId::TELEMETRY, PERIOD_TELEMETRY_MS * 5);
    TickType_t last_wake = xTaskGetTickCount();
    
    while (1) {
        SensorEvent evt;
        if (ctx->queue->receiveSensorEvent(evt, 0)) {
            router.processSensorEvent(evt);
            const TelemetryPacket& packet = router.getPacket();
            ctx->queue->sendTelemetryEvent(packet, 0);
        }
        
        ctx->watchdog->checkIn(TaskId::TELEMETRY);
        vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(PERIOD_TELEMETRY_MS));
    }
}

void TaskManager::healthTask(void* pvParameters) {
    TaskContext* ctx = static_cast<TaskContext*>(pvParameters);
    
    HealthManager manager;
    manager.init();
    
    ctx->watchdog->registerTask(TaskId::HEALTH, PERIOD_HEALTH_MS * 5);
    TickType_t last_wake = xTaskGetTickCount();
    
    while (1) {
        // Collect health blocks (Mocked for now since Managers don't pass health via queue yet)
        // manager.updateHealth(...);
        SystemHealth hs = manager.getSystemHealth();
        ctx->queue->sendHealthEvent(hs, 0);
        
        ctx->watchdog->checkIn(TaskId::HEALTH);
        vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(PERIOD_HEALTH_MS));
    }
}

void TaskManager::faultTask(void* pvParameters) {
    TaskContext* ctx = static_cast<TaskContext*>(pvParameters);
    
    while (1) {
        FaultEvent evt;
        if (ctx->queue->receiveFaultEvent(evt, portMAX_DELAY)) {
            // Enter safe state on critical fault
            if (evt.severity == FaultSeverity::CRITICAL) {
                CommandEvent stop_cmd;
                stop_cmd.type = CommandType::EMERGENCY_STOP;
                ctx->queue->sendMotorEvent(stop_cmd, 0);
                
                CommandEvent led_cmd;
                led_cmd.type = CommandType::SET_LED_MODE;
                led_cmd.payload.led.mode = LedMode::BLINK;
                led_cmd.payload.led.r = 255;
                ctx->queue->sendLedEvent(led_cmd, 0);
            }
        }
    }
}

} // namespace rtos
} // namespace rover
