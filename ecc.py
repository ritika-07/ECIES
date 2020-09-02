from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt
import binascii

privKey = generate_eth_key()
privKeyHex = privKey.to_hex()
pubKeyHex = privKey.public_key.to_hex()

print("Encryption public key:", pubKeyHex)
print("\n")
print("Decryption private key:", privKeyHex)
print("\n")

plaintext = b'Oi Ritika, see if this works'
print("Plaintext:", plaintext)
print("\n")

encrypted = encrypt(pubKeyHex, plaintext)
print("Encrypted:", binascii.hexlify(encrypted))
print("\n")

decrypted = decrypt(privKeyHex, encrypted)
print("Decrypted:", decrypted)
print("\n")
