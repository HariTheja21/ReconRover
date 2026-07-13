/**
 * @file health_manager.h
 * @brief Recon Rover V1 - Health Manager
 *
 * Aggregates and maintains the SystemHealth struct by pulling 
 * health statuses from other subsystems.
 */

#ifndef ROVER_HEALTH_MANAGER_H
#define ROVER_HEALTH_MANAGER_H

#include "health_system.h"

namespace rover {

/**
 * @class HealthManager
 * @brief Aggregates system health across all managers.
 */
class HealthManager {
public:
    HealthManager();
    
    /**
     * @brief Initializes the health manager state.
     */
    void init();

    /**
     * @brief Periodically updates the aggregate system health.
     * @param sensors Current SensorHealth block.
     * @param power Current PowerHealth block.
     * @param comms Current CommunicationHealth block.
     * @param uptime_ms Current system uptime.
     * @param free_heap Current free heap in bytes.
     */
    void updateHealth(const SensorHealth& sensors, const PowerHealth& power, 
                      const CommunicationHealth& comms, uint32_t uptime_ms, 
                      uint32_t free_heap);

    /**
     * @brief Gets the current aggregated SystemHealth.
     * @return Constant reference to the SystemHealth object.
     */
    const SystemHealth& getSystemHealth() const;

    /**
     * @brief Sets the safe mode active flag.
     * @param active True if safe mode is engaged.
     */
    void setSafeModeActive(bool active);

private:
    SystemHealth m_system_health;
};

} // namespace rover

#endif // ROVER_HEALTH_MANAGER_H
