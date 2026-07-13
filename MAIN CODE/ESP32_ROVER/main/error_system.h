/**
 * @file error_system.h
 * @brief Recon Rover V1 - Centralized Error Definitions
 *
 * Defines categories, severities, and specific error codes used by the
 * firmware managers to report faults.
 */

#ifndef ROVER_ERROR_SYSTEM_H
#define ROVER_ERROR_SYSTEM_H

#include <cstdint>

namespace rover {

/**
 * @enum ErrorCategory
 * @brief High-level classification of where the error occurred.
 */
enum class ErrorCategory : uint8_t {
    SYSTEM = 0,
    HARDWARE,
    COMMUNICATION,
    LOGIC,
    POWER
};

/**
 * @enum ErrorSeverity
 * @brief Indicates the impact of the error on system operation.
 */
enum class ErrorSeverity : uint8_t {
    INFO = 0,       /**< Informational, no action needed */
    WARNING,        /**< Degraded performance, operation continues */
    CRITICAL,       /**< Subsystem failure, enters Safe Mode */
    FATAL           /**< Entire system failure, requires reset */
};

/**
 * @enum ErrorCode
 * @brief Specific, unique identifiers for known faults.
 */
enum class ErrorCode : uint16_t {
    NONE = 0,
    
    // System Errors (1000-1999)
    SYS_INIT_FAILED = 1000,
    SYS_WATCHDOG_TIMEOUT = 1001,
    SYS_OUT_OF_MEMORY = 1002,

    // Hardware Errors (2000-2999)
    HW_I2C_BUS_HUNG = 2000,
    HW_MPU6050_FAULT = 2001,
    HW_VL53L0X_FAULT = 2002,
    HW_HCSR04_TIMEOUT = 2003,
    HW_SSD1306_FAULT = 2004,
    HW_MQ2_FAULT = 2005,
    HW_PCA9548A_FAULT = 2006,
    
    // Communication Errors (3000-3999)
    COMM_CDC_DISCONNECTED = 3000,
    COMM_PARSE_ERROR = 3001,
    COMM_CRC_MISMATCH = 3002,
    
    // Power Errors (4000-4999)
    PWR_LOW_BATTERY = 4000,
    PWR_OVERCURRENT = 4001
};

/**
 * @struct Error
 * @brief A comprehensive error object generated when a fault occurs.
 */
struct Error {
    ErrorCategory category;
    ErrorSeverity severity;
    ErrorCode code;
    uint32_t timestamp_ms;
    
    /**
     * @brief Creates a default empty error.
     */
    Error() : category(ErrorCategory::SYSTEM), severity(ErrorSeverity::INFO), code(ErrorCode::NONE), timestamp_ms(0) {}
    
    /**
     * @brief Creates a populated error object.
     */
    Error(ErrorCategory cat, ErrorSeverity sev, ErrorCode c, uint32_t ts) 
        : category(cat), severity(sev), code(c), timestamp_ms(ts) {}
};

} // namespace rover

#endif // ROVER_ERROR_SYSTEM_H
