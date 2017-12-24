import time
import psutil
import os
from sys import argv
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from stegano import lsb

'''ENCRYPT'''
backend = default_backend()
key = os.urandom(24)
iv = os.urandom(8)
plain = open(argv[1],'rb').read()
length = len(plain)
'''print(length)'''
if(length %16 !=0):
    n = 16 -(length % 16)
    plain = plain + (b'x' * n)
tic1 = time.process_time()
cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=backend)
encryptor = cipher.encryptor()
ct = encryptor.update(plain) + encryptor.finalize()
secret=lsb.hide("C:\\Users\\akshi\\OneDrive\\Defense\\logo.png",ct)
secret.save(".\logo100.png")
toc1 = time.process_time()
print("Encrypt time: ",(toc1-tic1), "ms\n")
tic2 =time.process_time()
'''DECRYPT'''
clearmsg = lsb.reveal(".\logo100.png")
c1 = clearmsg.encode('utf-8')
f1 = open("output100.txt","wb")
d = cipher.decryptor()
d1 = d.update(ct) + d.finalize()
f1.write(d1)
f1.close()
toc2 = time.process_time()
print("Decrypt time: ",(toc2-tic2), "ms\n")
'''MEMORY USAGE'''
process = psutil.Process(os.getpid())
print(process.memory_info().rss)