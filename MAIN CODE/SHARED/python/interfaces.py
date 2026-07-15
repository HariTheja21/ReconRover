# AUTO-GENERATED FILE. DO NOT MODIFY.
from abc import ABC, abstractmethod

class ISerializable(ABC):
    @abstractmethod
    def serialize(self) -> bytes:
        """Serializes the object into a byte buffer."""
        pass
        
    @classmethod
    @abstractmethod
    def deserialize(cls, data: bytes) -> 'ISerializable':
        """Deserializes the object from a byte buffer."""
        pass

class IValidatable(ABC):
    @abstractmethod
    def is_valid(self) -> bool:
        """Validates the internal state of the packet before processing."""
        pass

class IEventPayload(ABC):
    @abstractmethod
    def get_event_type(self) -> int:
        """Returns the EventType enum cast to an integer."""
        pass
