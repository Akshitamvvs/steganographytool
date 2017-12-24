from sys import argv
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from stegano import lsb
import time
import psutil
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
s = open(argv[1],'rb').read()

private_key = rsa.generate_private_key(
     public_exponent=65537,
     key_size=2048,
     backend=default_backend()
    )
public_key = private_key.public_key()
tic1 = time.process_time()
ciphertext = public_key.encrypt(
    s,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA1()),
        algorithm=hashes.SHA1(),
        label=None
    )
)
secret=lsb.hide("C:\\Users\\akshi\\OneDrive\\Defense\\logo.png",ciphertext)
secret.save(".\logo10.png")
toc1 = time.process_time()
print("Encrypt time: ",(toc1-tic1), "ms\n")
tic2 =time.process_time()
'''DECRYPT'''
clearmsg = lsb.reveal(".\logo10.png")
c1 = clearmsg.encode('utf-8')
f1 = open("output10.txt","wb")
pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)
pem_data = pem.splitlines()[0]
plaintext = private_key.decrypt(
   ciphertext,
   padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA1()),
        algorithm=hashes.SHA1(),
        label=None
    )
)
print(plaintext)
f1.write(plaintext)
f1.close()
toc2 = time.process_time()
print("Decrypt time: ",(toc2-tic2), "ms\n")
'''MEMORY USAGE'''
process = psutil.Process(os.getpid())
print(process.memory_info().rss)