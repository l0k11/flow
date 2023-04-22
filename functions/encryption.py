from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import NoEncryption, PrivateFormat,\
    Encoding, PublicFormat, load_pem_public_key, load_pem_private_key
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import pickle

# Aquí almaceno las funciones usadas para encriptar y desencriptar. Como considero que estas
# funciones son muy importantes, voy a explicarlas una por una. 

# Esta función genera los archivos de clave pública y privada tanto de cliente como de servidor
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
        encryption_algorithm = NoEncryption()
    )
    
    with open(f"{directory}public.key", "w") as file: file.write(serialized_public_key.decode())
    with open(f"{directory}private.key", "w") as file: file.write(serialized_private_key.decode())

# Esta función encripta mensajes mediante el uso de criptografía mixta. La función genera una clave
# única cada vez que se ejecuta y con esa clave encripta el mensaje. Luego, serializa la clave
# y la cifra con la clave pública del destinatario y devuelve una lista que contiene el mensaje 
# encriptado y la clave. 
def encrypt_message(message: bytes, public_key_file: str):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(message)
    
    with open(public_key_file, "rb") as file:
        public_key = load_pem_public_key(
            file.read(),
            backend = default_backend()
        )

    encrypted_key = public_key.encrypt(
        pickle.dumps(fernet),
        padding.OAEP (
            mgf = padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
        )
    )

    return [encrypted, encrypted_key]

# Esta función desencripta mensajes de la siguiente forma:
#   1. Desencripta la clave generada aleatoriamente con la clave privada
#   2. Usa la llave desencriptada para desencriptar el paquete 
def decrypt_message(encrypted_message: bytes, private_key_file, encrypted_key) -> str:
    with open(private_key_file, "rb") as file:
        private_key = load_pem_private_key(
            file.read(),
            backend = default_backend(),
            password = None
        )

    key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf = padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
        )
    )

    key = pickle.loads(key)
    return key.decrypt(encrypted_message).decode()