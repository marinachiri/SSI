import os
import hashlib
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

antet_hashes = []

# Generam o cheie aleatoare pentru a cripta continutul
key = os.urandom(32)  # Cheie de 256 de biți

for file_name in os.listdir("/content/sample_data/litere_originale"):
    file_path = os.path.join("/content/sample_data/litere_originale", file_name)

    # Deschidem fisierul si separam antetul de corp
    with open(file_path, 'rb') as file:
        antet = [] #primele 3 randuri sunt antetul pozei, restul sunt pixeli
        for _ in range(3):
            antet.append(file.readline())
        body = file.read()

        # Calculam hashul antetului
        #concatenam si decodam din binar in sir de caractere antetul
        antet_str = " ".join([line.decode().strip() for line in antet])
        #hashuim antetul dupa concatenare
        antet_hash = hashlib.sha256(antet_str.encode()).hexdigest()
        #il adaugam la lista noastra de antete hashuite
        antet_hashes.append(antet_hash)

        # Initializam cifrul AES in modul CTR
        nonce = os.urandom(16) #numar random folosit o sg data care ne trebuie pt folosirea modului CTR
        #generam cifrul AES cu cheia "key", in aes aceeasi cheie este folosita si pt criptare si pt decriptare
        cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
        encryptor = cipher.encryptor()

        # Padding si criptare, practic noi trebuie sa adaugam padding pentru a compensa lipsurile de la criptare
        padder = padding.PKCS7(128).padder()
        padded_body = padder.update(body) + padder.finalize()
        #criptamcontinutul
        ciphertext = encryptor.update(padded_body) + encryptor.finalize()

        # Scriem corpul criptat in fisierul de iesire
        final_path = os.path.join("/content/sample_data/criptate", file_name)
        with open(final_path, 'wb') as encrypted_file:
            encrypted_file.write(ciphertext)

# Afisam hashurile anteturilor
for h in antet_hashes:
    print(h + ',')
