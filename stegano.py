#####################################################################
#                                                                   #
#   Author: Christian J. Ramos Ortega                               #
#   Date: May 24 2023                                               #
#   Course: COTI4260 - Seguridad de la Informacion                  #
#   Purpose: This program uses steganography techniques             #
#       to encode and decode information in an image.               #
#                                                                   #
#####################################################################
import numpy as np
#Process images without the correct format
def process_img(steg_name):
    #OLD AND NEW FILES
    steg_path = './images/' + steg_name
    new_path = './images/alt/' + steg_name
    
    file = open(steg_path, "r")
    new_file = open(new_path, "w")
    
    #STORING EACH INDIVIDUAL VALUE OF OLD FILE IN A STRING
    temp = ""
    counter = 0
    for i in file.readlines():
        #HEADER
        if(counter < 3):
            if(i.find('#') < 0):
                temp += i
        #BODY
        else:
            if(len(i) > 0):
                temp += i + ' '
        counter+=1
    temp = temp.split()
    
    #WRITE THE NEW FILE
    count = 0
    count2 = 0
    for i in temp:
        #HEADER
        if(count < 4):
            if(count == 1):
                new_file.write(i + " ")
            else:
                new_file.write(i + "\n")
        #BODY
        else:
            #12th element
            if(count2 == 11):
                new_file.write(i + "\n")
                count2 = 0
            #Rest of elements
            else:
                new_file.write(i + " ")
                count2 += 1 
        count += 1
        
    
#Tries to parse a value to integer, returns a tuple with the value and
# a boolean value that determines if successfull.
# This is used to provide a way to not eliminate any bytes.
def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False
    
    
#Decodes image from steganography image
def decode_img(steg_name):
    steg_path =""
    
    #Check if converted
    converted = input("Is this photo converted to another type from the original? (Y) for yes (N) for no: ")
    if(converted == 'Y'):
        process_img(steg_name)
        steg_path = './images/alt/' + steg_name
    elif(converted == 'N'):
        steg_path = './images/' + steg_name
    else:
        raise Exception("Invalid entry.")     
    
    #Steganography image
    steg_header, steg_body = read_photo(steg_path)
    #print(steg_body)
    steg_body.pop()
    
    #NUMPY ARRAY
    steg_body = np.array(steg_body)
    
    #Original photo to compare to
    og_name = input('What is the name of the original photo file?: ')
    og_path = './images/' + og_name
    oh_header, og_body = read_photo(og_path)  
    og_body.pop()
    
    #NUMPY ARRAY
    og_body = np.array(og_body)
    
    #COMPARES EACH ITEM AND RETURNS A LIST OF BOOLEANS
    result_arr = steg_body == og_body
    
    #CREATE A BIT STRING BASED ON THE BOOLEANS
    bit_result = ""
    for i in result_arr:
        for j in i:
            #THEY ARE EQUAL
            if(j == True):
                bit_result += "0"
            #CHANGE HAS BEEN MADE
            elif(j == False):
                bit_result += "1"
                
    #VERIFY FOR THE DELIMITER END AND CUT THERE
    end_idx = bit_result.rindex('1')
    bit_result = bit_result[:end_idx+1]
    
    #ELIMINATE DELIMETER (";") or (00111011)
    bit_result = bit_result[:len(bit_result)-8]
    
    #REBUILD ENCODED IMG
    img = []
    for i in range(0,len(bit_result),8):
        img.append(str(int(bit_result[i:i+8],2)))
        
    #WITH AND HEIGHT
    img_width = img[0]
    img_height = img[1]
    
    #BODY
    img_body = img[2:len(img)]
    
    #NEW IMAGE HEADER
    new_img = []
    new_img.append("P3 " + str(img_width) + " " + str(img_height) + " " + "255 ")
    for i in img_body:
        new_img.append(i + " ")
    new_file = open('./images/' + 'deciphered.ppm', "w")
    new_file.writelines(new_img)
    
    
#Decodes text from steganography image
#The last line of the file is lost (pop()) in order to create the numpy array
# which allows me to compare each one of the items
def decode_txt(steg_name):
    steg_path = './images/'+ steg_name
    #Steganography image
    steg_header, steg_body = read_photo(steg_path)
    steg_body.pop()
    
    #NUMPY ARRAY
    steg_body = np.array(steg_body)
    
    #Original photo to compare to
    og_name = input('What is the name of the original photo file?: ')
    og_path = './images/' + og_name
    oh_header, og_body = read_photo(og_path)
    og_body.pop()
    
    #NUMPY ARRAY
    og_body = np.array(og_body)
    
    #COMPARES EACH ITEM AND RETURNS A LIST OF BOOLEANS
    result_arr = steg_body == og_body
    
    #CREATE A BIT STRING BASED ON THE BOOLEANS
    bit_result = ""
    for i in result_arr:
        for j in i:
            
            #THEY ARE EQUAL
            if(j == True):
                bit_result += "0"
                
            #CHANGE HAS BEEN MADE
            elif(j == False):
                bit_result += "1"
                
    #VERIFY FOR THE DELIMITER END AND CUT THERE
    end_idx = bit_result.rindex('1')
    bit_result = bit_result[:end_idx+1]
    
    #ELIMINATE DELIMETER (";") or (00111011)
    bit_result = bit_result[:len(bit_result)-8]
    
    #RETURN MESSAGE
    msg = ""
    for i in range(0,len(bit_result),8):
        msg += chr(int(bit_result[i:i+8],2))
    print(msg)


#Decodes a steganography image
def decode(filename):
    selection = int(input('What is inside this image? (1) for text or (2) for an image: '))
    if(selection == 1):
        decode_txt(filename)
    elif(selection == 2):
        decode_img(filename)
    
    
#Returns the binary string of the image to be encoded
def binary_img(width, height, img_body):
    binary = []
    binary.extend(format(width,"08b"))
    binary.extend(format(height,"08b"))
    for line in img_body:
        for val in line:
            binary.extend(format(val,"08b"))
    return binary


#Writes the new image with the new name given by the user
def write_img(new_name, final_lst):
    new_name = './images/' + new_name
    new_img = open(new_name, "w")
    counter = 0
    for val in final_lst:
        
        #HEADER
        if(counter < 3):
            for num in val:
                new_img.write(num)
                
        #BODY
        else:
            for num in val:
                new_img.write(num + ' ')
        new_img.write("\n")
        counter += 1

    
#Merges any binary string to the body of the key image
# by incrementing by 1 if binary is 1
# and leaving number as is if binary is 0
#
# O(n) = len(body) * 12
def img_merge(header, body, binary):
    result =[]
    
    #ADD HEADER INFO TO THE RESULTING LIST
    result.extend(header)
    binary_idx = 0
    
    #LINES
    for i in range(len(body)):
        temp = []
        
        #12 PIXELS PER LINE
        #EACH W AN RGB VALUE,
        #EACH RGB VALUE IS A GROUP OF 3 INT
        for j in range(len(body[i])):
            
            #MESSAGE TO ENCODE
            if(binary_idx < len(binary)):
                
                #0 or 1
                if(binary[binary_idx] == "1"):
                    if(body[i][j] < 254):
                        temp.append(body[i][j]+1)
                    else:
                        temp.append(body[i][j]-1)
                else:
                    temp.append(body[i][j])
                binary_idx += 1
                
            #MESSAGE COMPLETELY ENCODED
            else:
                temp.append(body[i][j])
        temp = [str(i) for i in temp]
        result.append(temp)
    return result

    
#Reads the photo information
#returns two lists, one for the header information of the image
# and the second one for the image itself
def read_photo(path):
    header = []
    body = []
    file = open(path, 'r')
    
    counter = 0
    for line in file.readlines():
        line = line.replace('\n', '')
        line = line.strip()
        if(counter < 3):
            if(line.find('#') > -1):
                pass
            header.append(line)
        else:
            
            line = list(line.split(" "))
            value, flag = intTryParse(line[-1])
            if(flag):
                pass
            else:
                line.pop()
            line = list(map(int, line))
            body.append(line)
        counter += 1
    return(header,body)
    

#Changes text to binary string
def text_to_bin(txt):   
        #ord(char) returns the ascii
        return ''.join([format(ord(char), "08b") for char in txt]) 
        

#Encrypt a text message in an image
def encode_txt():
    #FILE
    filename = str(input('Enter the file name of the key photo with the extension: '))
    path = './images/' + filename
    
    #ReadPhoto
    header, body = read_photo(path)

    #MESSAGE TO BE ENCRYPTED
    # ";" -> 00111011
    msg = str(input('Enter the message to be encrypted: ')) + ";"
    #MESSAGE TO BINARY
    msg_bin = text_to_bin(msg)
    
    #POSSIBLE TO MERGE MESSAGE IN IMAGE
    width, height = list(map(int, header[1].split(" ")))
    img_bit_len = width*height
    
    msg_bit_len = len(msg)*8
    
    if(msg_bit_len > img_bit_len):
        raise Exception("Cannot fit message into image")
    
    #MERGE IMAGE AND MESSAGE
    final_lst = img_merge(header, body, msg_bin)
    
    #WRITE NEW IMAGE
    new_name = input('Please enter the new filename: ')
    write_img(new_name, final_lst)
    
    
def encode_img():
    #KEY IMAGE
    key_filename = str(input('Enter the file name of the key photo with the extension: '))
    key_path = './images/' + key_filename
    
    #ReadKeyPhoto
    key_header, key_body = read_photo(key_path)
    
    #KEY WIDTH AND HEIGHT
    key_width, key_height = list(map(int, key_header[1].split(" ")))
    key_area = key_width*key_height
    
    #IMAGE TO BE ENCODED
    img_filename = str(input('Enter the file name of the photo to be hidden: '))
    img_path = './images/' + img_filename
    
    #ReadEncodeImg
    img_header, img_body = read_photo(img_path)
    
    #IMAGE WIDTH AND HEIGHT
    img_width, img_height = list(map(int, img_header[1].split(" ")))
    img_area = img_width*img_height
    
    #BINARY OF IMAGE
    img_binary = binary_img(img_width, img_height, img_body)
    
    
    #ADDING DELIMITER
    # ";" -> 00111011
    img_binary.extend(format(ord(';'), '08b'))
    
    #POSSIBLE TO MERGE MESSAGE IN IMAGE
    if(img_area > key_area):
        raise Exception("Cannot encode image in the key photo, too big.")
    
    #MERGE BOTH IMAGES
    final_lst = img_merge(key_header, key_body, img_binary)
    
    #WRITE NEW IMAGE
    new_name = input('Please enter the new filename: ')
    write_img(new_name, final_lst)
    

#Main entry point for the program
def main():
    while(True):
        ans = int(input('(1) for text encryption, (2) for image encryption, (3) for decryption'))
        
        if(ans == 1):
            print('Encoding text in an image...')
            encode_txt()
        elif(ans == 2):
            print('Encoding an image in an image...')
            encode_img()
        elif(ans == 3):
            encoded_filename = input('Enter the filename with the extension: ')
            print('Decoding image...')
            decode(encoded_filename)
        else:
            return 0


if __name__ == "__main__":
    main()
