// AUTO-GENERATED FILE. DO NOT MODIFY.
#ifndef ROVER_INTERFACES_H
#define ROVER_INTERFACES_H

#include <stdint.h>
#include <stddef.h>

class ISerializable {
public:
    virtual ~ISerializable() = default;
    
    // Serializes the object into a byte buffer. Returns bytes written.
    virtual size_t serialize(uint8_t* buffer, size_t max_len) const = 0;
    
    // Deserializes the object from a byte buffer. Returns bytes read.
    virtual size_t deserialize(const uint8_t* buffer, size_t len) = 0;
};

class IValidatable {
public:
    virtual ~IValidatable() = default;
    
    // Validates the internal state of the packet before processing
    virtual bool is_valid() const = 0;
};

class IEventPayload {
public:
    virtual ~IEventPayload() = default;
    
    // Returns the EventType enum cast to uint8_t
    virtual uint8_t get_event_type() const = 0;
};

#endif // ROVER_INTERFACES_H
