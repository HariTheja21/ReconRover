/**
 * @file types_actuator.h
 * @brief Recon Rover V1 - Common Actuator Command Types
 *
 * Defines the standardized structures for commanding actuators
 * (motors, servos, LEDs, OLED).
 */

#ifndef ROVER_TYPES_ACTUATOR_H
#define ROVER_TYPES_ACTUATOR_H

#include <cstdint>

namespace rover {

/**
 * @struct ServoCommand
 * @brief Commands a servo to a specific angle.
 */
struct ServoCommand {
    uint8_t servo_id;     /**< Identifier for the servo (e.g., 0=Pan, 1=Tilt) */
    float target_angle;   /**< Target angle in degrees */
};

/**
 * @struct MotorCommand
 * @brief Commands the differential drive motors.
 */
struct MotorCommand {
    float left_speed;     /**< Left motor speed (-1.0 to 1.0) */
    float right_speed;    /**< Right motor speed (-1.0 to 1.0) */
};

/**
 * @enum EyeExpression
 * @brief Available expressions for the OLED robot eyes.
 */
enum class EyeExpression : uint8_t {
    NEUTRAL = 0,
    HAPPY,
    SAD,
    ANGRY,
    SURPRISED,
    BLINKING,
    SLEEPING
};

/**
 * @struct EyeCommand
 * @brief Commands the OLED renderer to display an expression.
 */
struct EyeCommand {
    EyeExpression expression; /**< The target expression to render */
};

/**
 * @enum LedMode
 * @brief Animation modes for the WS2812B LEDs.
 */
enum class LedMode : uint8_t {
    OFF = 0,
    SOLID,
    BLINK,
    SWEEP,
    BREATHE
};

/**
 * @struct LEDCommand
 * @brief Commands the LED controller.
 */
struct LEDCommand {
    LedMode mode;         /**< The animation mode */
    uint8_t red;          /**< Red color component (0-255) */
    uint8_t green;        /**< Green color component (0-255) */
    uint8_t blue;         /**< Blue color component (0-255) */
};

} // namespace rover

#endif // ROVER_TYPES_ACTUATOR_H
