// AUTO-GENERATED FILE. DO NOT MODIFY.

export interface ISerializable {
    serialize(): Uint8Array;
}

export interface IDeserializable<T> {
    deserialize(data: Uint8Array): T;
}

export interface IValidatable {
    isValid(): boolean;
}

export interface IEventPayload {
    getEventType(): number;
}
