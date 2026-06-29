/**
 * @file hal_types.h
 * @brief Recon Rover V1 - ESP32 Hardware Abstraction Layer Types
 *
 * Defines common types, error codes, and status objects used across all HAL components.
 */

#ifndef ROVER_HAL_TYPES_H
#define ROVER_HAL_TYPES_H

#include <cstdint>
#include "esp_err.h"

namespace rover {
namespace hal {

/**
 * @enum HalError
 * @brief Standardized error codes for HAL operations.
 */
enum class HalError : int32_t {
    OK = 0,                        /**< Operation completed successfully */
    ERR_INVALID_ARG = -1,          /**< Invalid argument provided to HAL function */
    ERR_TIMEOUT = -2,              /**< Operation timed out */
    ERR_NOT_INITIALIZED = -3,      /**< Component accessed before initialization */
    ERR_ALREADY_INITIALIZED = -4,  /**< Component initialized multiple times */
    ERR_HARDWARE = -5,             /**< Underlying hardware failure or ESP-IDF error */
    ERR_NO_MEMORY = -6,            /**< Memory allocation failed */
    ERR_NOT_SUPPORTED = -7         /**< Feature not supported by this hardware */
};

/**
 * @struct HalStatus
 * @brief Standardized return object for all HAL functions.
 *
 * Encapsulates the high-level HAL error code along with the underlying ESP-IDF
 * error code (if applicable) for detailed debugging.
 */
struct HalStatus {
    HalError error;        /**< The high-level HAL error code */
    esp_err_t esp_error;   /**< The underlying ESP-IDF error code, or ESP_OK */

    /**
     * @brief Checks if the status represents a successful operation.
     * @return true if error is HalError::OK, false otherwise.
     */
    bool isOk() const {
        return error == HalError::OK;
    }
};

} // namespace hal
} // namespace rover

#endif // ROVER_HAL_TYPES_H
