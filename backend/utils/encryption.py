import base64
import hashlib
from typing import Optional

from cryptography.fernet import Fernet


class Encryption:
    """
    Simple Encryption Utility for LIAO AI Assistant

    Use cases:
    - Secure sensitive data
    - Encode/Decode strings
    - Future memory protection layer
    """

    def __init__(self, secret_key: Optional[str] = None):
        """
        If no key provided, generate internal safe key
        """
        if secret_key:
            self.key = self._generate_key(secret_key)
        else:
            self.key = Fernet.generate_key()

        self.cipher = Fernet(self.key)

    # --------------------------------------
    # KEY GENERATION
    # --------------------------------------
    def _generate_key(self, secret: str) -> bytes:
        """
        Convert any string into secure encryption key
        """
        hashed = hashlib.sha256(secret.encode()).digest()
        return base64.urlsafe_b64encode(hashed)

    # --------------------------------------
    # ENCRYPT TEXT
    # --------------------------------------
    def encrypt(self, data: str) -> str:
        """
        Encrypt string data
        """
        if not data:
            return ""

        encrypted = self.cipher.encrypt(data.encode())
        return encrypted.decode()

    # --------------------------------------
    # DECRYPT TEXT
    # --------------------------------------
    def decrypt(self, token: str) -> str:
        """
        Decrypt encrypted string
        """
        if not token:
            return ""

        try:
            decrypted = self.cipher.decrypt(token.encode())
            return decrypted.decode()

        except Exception:
            return ""

    # --------------------------------------
    # HASH (ONE-WAY)
    # --------------------------------------
    def hash_text(self, text: str) -> str:
        """
        One-way hashing (for passwords, IDs)
        """
        return hashlib.sha256(text.encode()).hexdigest()


# --------------------------------------
# TEST RUN (optional)
# --------------------------------------
if __name__ == "__main__":
    enc = Encryption("liao-secret-key")

    original = "Hello LIAO AI"

    encrypted = enc.encrypt(original)
    decrypted = enc.decrypt(encrypted)

    print("Original :", original)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)