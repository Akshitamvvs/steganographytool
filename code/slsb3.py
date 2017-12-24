from sys import argv
from PIL import Image
import time
import psutil
import os
from cryptography.hazmat.backends import default_backend
from sys import argv
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
def encode_image(img, msg):
    """
    use the red portion of an image (r, g, b) tuple to
    hide the msg string characters as ASCII values
    red value of the first pixel is used for length of string
    """
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
    """
    check the red portion of an image (r, g, b) tuple for
    hidden message characters (ASCII values)
    """
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
s = open(argv[1],'r').read()
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


if img_encoded:
    # save the image with the hidden text
    img_encoded.save(".\secret21.png")
    print("{} saved!".format(".\secret21.png"))
    # view the saved file, works with Windows only
    # behaves like double-clicking on the saved file
    import os
    os.startfile(".\secret21.png")
    print("encrypt time: ", toc1-tic1,"ms")
    
    
        # get the hidden text back ...
    tic2 = time.process_time()
    img2 = Image.open(".\secret21.png")
    hidden_text = decode_image(img2)
    f1 = open("output21.txt","wb")
    d = cipher.decryptor()
    d1 = d.update(ct) + d.finalize()
    f1.write(d1)
    f1.close()
    #print("Hidden text:\n{}".format(hidden_text))
    toc2 = time.process_time()
    print("decrypt time: ", toc2-tic2,"ms")

process = psutil.Process(os.getpid())
print(process.memory_info().rss)