import hashlib
import os

class OTAValidator:
    @staticmethod
    def validate_package(filepath: str, expected_checksum: str) -> bool:
        if not os.path.exists(filepath):
            return False
            
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest() == expected_checksum
        except Exception:
            return False
