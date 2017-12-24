from sys import argv
from PIL import Image
import time
import psutil
import os
from sys import argv
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encode_image(img, msg):
   
    length = len(msg)
    # limit length of message to 255
    #if length > 255:
     #   print("text too long! (don't exeed 255 characters)")
     #    return False
    '''if img.mode != 'RGB':
        print("image mode needs to be RGB")
        return False'''
    # use a copy of image to hide the text in
    encoded = img.copy()
    width, height = img.size
    index = 0
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            # first value is length of msg
            if row == 0 and col == 0 and index < length:
                asc = length
            elif index <= length:
                c = msg[index -1]
                #asc = ord(c)
                asc = c
            else:
                asc = b
            encoded.putpixel((col, row), (r, g , asc))
            index += 1
    return encoded
def decode_image(img):
    
    width, height = img.size
    msg = ""
    index = 0
    for row in range(height):
        for col in range(width):
            try:
                r, g, b = img.getpixel((col, row))
            except ValueError:
                # need to add transparency a for some .png files
                r, g, b, a = img.getpixel((col, row))		
            # first pixel r value is length of message
            if row == 0 and col == 0:
                length = b
            elif index <= length:
                msg += chr(b)
            index += 1
    return msg
# pick a .png or .bmp file you have in the working directory
# or give full path name
original_image_file = "C:/Users/akshi/OneDrive/Defense/Beach.png"
#original_image_file = "Beach7.bmp"
img = Image.open(original_image_file)
# image mode needs to be 'RGB'
print(img, img.mode)  # test

backend = default_backend()
key = os.urandom(32)
iv = os.urandom(16)
secret_msg = open(argv[1],'rb').read()
length = len(secret_msg)
if(length %16 !=0):
    n = 16 -(length % 16)
    secret_msg = secret_msg + (b'x' * n)
s1 = secret_msg.decode('utf-8')
tic1 = time.process_time()
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
encryptor = cipher.encryptor()
ct = encryptor.update(secret_msg) + encryptor.finalize()
img_encoded = encode_image(img, ct)
toc1 = time.process_time()
if img_encoded:
    # save the image with the hidden text
    img_encoded.save(".\secret10.png")
    print("{} saved!".format(".\secret10.png"))
    # view the saved file, works with Windows only
    # behaves like double-clicking on the saved file
    import os
    os.startfile(".\secret10.png")
    print("encrypt time: ", toc1-tic1,"ms")
    
    
        # get the hidden text back ...
    tic2 = time.process_time()
    img2 = Image.open(".\secret10.png")
    hidden_text = decode_image(img2)
    f1 = open("output10.txt","wb")
    d = cipher.decryptor()
    d1 = d.update(ct) + d.finalize()
    f1.write(d1)
    f1.close()
    #print("Hidden text:\n{}".format(hidden_text))
    toc2 = time.process_time()
    print("decrypt time: ", toc2-tic2,"ms")

process = psutil.Process(os.getpid())
print(process.memory_info().rss)