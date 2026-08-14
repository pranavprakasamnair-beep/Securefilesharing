from cryptography.fernet import Fernet
import hashlib

class FileEncryption:
    @staticmethod
    def generate_key():
        return Fernet.generate_key()
    
    @staticmethod
    def encrypt_file(file_data, key=None):
        if key is None:
            key = FileEncryption.generate_key()
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(file_data)
        return encrypted_data, key
    
    @staticmethod
    def decrypt_file(encrypted_data, key):
        try:
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)
            return decrypted_data
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    @staticmethod
    def calculate_hash(file_data):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(file_data)
        return sha256_hash.hexdigest()
    
    @staticmethod
    def verify_hash(file_data, expected_hash):
        calculated_hash = FileEncryption.calculate_hash(file_data)
        return calculated_hash == expected_hash