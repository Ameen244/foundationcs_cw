
def is_bmp_file(file_path):
    
    if not file_path.lower().endswith(".bmp"):
        print("Error: Only BMP files are supported.")
        return False
    try:
       
        with open(file_path, "rb") as file:
            magic_number = file.read(2)
            if magic_number != b"BM":  
                print("Error: The file is not a valid BMP image.")
                return False
    except IOError:
        print("Error: Unable to read the file.")
        return False
    return True


def hide_message_in_image(image_path, message):
    if not is_bmp_file(image_path):
        return

    try:
        with open(image_path, "rb") as file:
            image_data = bytearray(file.read())
    except IOError:
        print("Error: Unable to read the image file.")
        return

    
    binary_message = ''.join(format(ord(char), '08b') for char in message + '\0')

    
    if len(binary_message) > len(image_data) - 54:  
        print("Error: The message is too large to hide in this image.")
        return

    
    for i in range(len(binary_message)):
        bit = int(binary_message[i])
        image_data[54 + i] = (image_data[54 + i] & 254) | bit


    new_image_path = "output_image.bmp"
    try:
        with open(new_image_path, "wb") as new_file:
            new_file.write(image_data)
        print(f"Message successfully hidden in {new_image_path}")
    except IOError:
        print("Error: Unable to save the new image file.")



def extract_message_from_image(image_path):
    if not is_bmp_file(image_path):
        return ""

    try:
        with open(image_path, "rb") as file:
            image_data = file.read()
    except IOError:
        print("Error: Unable to read the image file.")
        return ""

    binary_message = ""  
    message = ""  
   
    for byte in image_data[54:]:
        binary_message += str(byte & 1)

   
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        if len(byte) < 8:
            break
        char = chr(int(byte, 2))
        if char == '\0':  
            break
        message += char

    return message




if __name__ == "__main__":
    print("Welcome to BMP Steganography!")
    image_path = input("Enter the BMP image file path: ")
    choice = input("Do you want to hide a message (H) or extract a message (E)? ").upper()

    if choice == "H":
        message = input("Enter the message to hide: ")
        hide_message_in_image(image_path, message)
    elif choice == "E":
        extracted_message = extract_message_from_image(image_path)
        print("Extracted message:", extracted_message)
    else:
        print("Invalid choice. Please choose 'H' to hide or 'E' to extract.")
