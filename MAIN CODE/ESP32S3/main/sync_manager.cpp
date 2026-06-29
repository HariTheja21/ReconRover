/**
 * @file sync_manager.cpp
 * @brief Recon Rover V1 - RTOS Synchronization Manager
 */

#include "sync_manager.h"

namespace rover {
namespace rtos {

// =========================================================================
// Mutex
// =========================================================================
Mutex::Mutex() : m_handle(nullptr) {}

Mutex::~Mutex() {
    if (m_handle) vSemaphoreDelete(m_handle);
}

bool Mutex::init() {
    m_handle = xSemaphoreCreateMutex();
    return m_handle != nullptr;
}

bool Mutex::lock(uint32_t wait_ms) {
    if (!m_handle) return false;
    return xSemaphoreTake(m_handle, wait_ms == portMAX_DELAY ? portMAX_DELAY : pdMS_TO_TICKS(wait_ms)) == pdTRUE;
}

bool Mutex::unlock() {
    if (!m_handle) return false;
    return xSemaphoreGive(m_handle) == pdTRUE;
}

// =========================================================================
// RecursiveMutex
// =========================================================================
RecursiveMutex::RecursiveMutex() : m_handle(nullptr) {}

RecursiveMutex::~RecursiveMutex() {
    if (m_handle) vSemaphoreDelete(m_handle);
}

bool RecursiveMutex::init() {
    m_handle = xSemaphoreCreateRecursiveMutex();
    return m_handle != nullptr;
}

bool RecursiveMutex::lock(uint32_t wait_ms) {
    if (!m_handle) return false;
    return xSemaphoreTakeRecursive(m_handle, wait_ms == portMAX_DELAY ? portMAX_DELAY : pdMS_TO_TICKS(wait_ms)) == pdTRUE;
}

bool RecursiveMutex::unlock() {
    if (!m_handle) return false;
    return xSemaphoreGiveRecursive(m_handle) == pdTRUE;
}

// =========================================================================
// EventGroup
// =========================================================================
EventGroup::EventGroup() : m_handle(nullptr) {}

EventGroup::~EventGroup() {
    if (m_handle) vEventGroupDelete(m_handle);
}

bool EventGroup::init() {
    m_handle = xEventGroupCreate();
    return m_handle != nullptr;
}

void EventGroup::setBits(uint32_t bits) {
    if (m_handle) xEventGroupSetBits(m_handle, bits);
}

void EventGroup::clearBits(uint32_t bits) {
    if (m_handle) xEventGroupClearBits(m_handle, bits);
}

uint32_t EventGroup::waitBits(uint32_t bits, bool clear_on_exit, bool wait_for_all, uint32_t wait_ms) {
    if (!m_handle) return 0;
    return xEventGroupWaitBits(m_handle, bits, 
                               clear_on_exit ? pdTRUE : pdFALSE, 
                               wait_for_all ? pdTRUE : pdFALSE, 
                               wait_ms == portMAX_DELAY ? portMAX_DELAY : pdMS_TO_TICKS(wait_ms));
}

} // namespace rtos
} // namespace rover
