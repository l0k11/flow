from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import BestAvailableEncryption, PrivateFormat, Encoding, PublicFormat
from uuid import uuid4

# TODO: PUERTO DIFERENTES PARA CONEXIONES DE CONTROL Y MENSAJES

def generate_keys(directory):
    private_key = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 2048,
    )
    public_key = private_key.public_key()
    serialized_public_key = public_key.public_bytes(
        encoding = Encoding.PEM,
        format = PublicFormat.SubjectPublicKeyInfo
    )

    serialized_private_key = private_key.private_bytes(
        encoding = Encoding.PEM,
        format = PrivateFormat.PKCS8,
        encryption_algorithm = BestAvailableEncryption(uuid4().bytes)
    )
    with open(f"{directory}public.key", "w") as file: file.write(serialized_public_key.decode())
    with open(f"{directory}private.key", "w") as file: file.write(serialized_private_key.decode())

def encrypt_message(message, public_key: rsa.RSAPublicKey):
    return public_key.encrypt(
        message,
        padding.OAEP(
            mgf = padding.MGF1(algorithm=hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
        )
    )

def decrypt_message(encrypted_message, private_key: rsa.RSAPrivateKey):
    return private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf = padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
        )
    )

