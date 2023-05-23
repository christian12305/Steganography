
# try block to handle exception
try:
    # take path of image as a input
    path = input(r'Enter path of Image : ')

    # taking encryption key as input
    key = int(input('Enter Key for encryption of Image : '))

    # print path of image file and encryption key that
    # we are using
    print('The path of file : ', path)
    print('Key for encryption : ', key)

    # open file for reading purpose
    fin = open(path, 'rb')

    # storing image data in variable "image"
    image = fin.read()
    fin.close()

    # converting image into byte array to
    # perform encryption easily on numeric data
    image = bytearray(image)

    # performing XOR operation on each value of bytearray
    for index, values in enumerate(image):
        image[index] = values ^ key

    # opening file for writing purpose
    fin = open(path, 'wb')

    # writing encrypted data in image
    fin.write(image)
    fin.close()
    print('Encryption Done...')


except Exception:
    print('Error caught : ', Exception.__name__)






#Encrypt a text message in an image
def encrypt_txt():
    #FILE
    filename = str(input("Enter the file path: "))
    file = open(filename, 'r')

    #MESSAGE TO BE ENCRYPTED
    msg = str(input("Enter the message to be encrypted: "))



def main():

    ans = int(input("(1) for text encryption, (2) for image encryption, (3) for decryption"))

    match ans:
        case 1:
            print("Encrypting text in an image...")
            encrypt_txt()
        case 2:
            print("Encrypting img in an img")
        case 3:
            print("Decrypting...")
