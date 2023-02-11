import re
import base64
import argparse

def decode_base64(data):
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'=' * missing_padding
    return base64.b64decode(data)

def find_base64_encoded_strings(file_path):
    encoded_strings = []
    pattern = re.compile(br'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?')
    with open(file_path, 'rb') as f:
        data = f.read()
        matches = re.findall(pattern, data)
        for encoded_string in matches:
            try:
                decoded_string = decode_base64(encoded_string).decode("latin-1")
                encoded_strings.append((encoded_string, decoded_string))
            except:
                pass
    return encoded_strings

def clean_file(filename, output_filename):
    with open(filename, 'r', encoding='latin-1') as file:
        contents = file.read()
        cleaned_contents = re.sub(r'[^A-Za-z0-9]+', '.', contents)
        
    with open(output_filename, 'w') as output_file:
        output_file.write(cleaned_contents)

if __name__ == '__main__':
    print("""
    
     _        _             _                     __   _  _   
 ___| |_ _ __(_)_ __   __ _| |__   __ _ ___  ___ / /_ | || |  
/ __| __| '__| | '_ \ / _` | '_ \ / _` / __|/ _ \ '_ \| || |_ 
\__ \ |_| |  | | | | | (_| | |_) | (_| \__ \  __/ (_) |__   _|
|___/\__|_|  |_|_| |_|\__, |_.__/ \__,_|___/\___|\___/   |_|  
                      |___/                                   
                                   by Hamza Haroon (TheGr1ffyn)
                                   github.com/thegr1ffyn

    """)
    parser = argparse.ArgumentParser(description='Find base64 encoded strings in a file, remove non-alphanumeric characters, and save the encoded and decoded strings output into the output file')
    parser.add_argument('file_path', type=str, help='Path to the file to be processed')
    parser.add_argument('output_filename', type=str, help='The file to write the cleaned contents and encoded/decoded strings to')
    args = parser.parse_args()

    clean_file(args.file_path, args.output_filename)

    encoded_strings = find_base64_encoded_strings(args.output_filename)
    with open(args.output_filename, 'a') as output_file:
        output_file.truncate(0)
        for encoded_string, decoded_string in encoded_strings:
            if decoded_string:
                output_file.write("Encoded String: " + str(encoded_string) + "\n")
                output_file.write("Decoded String: " + decoded_string + "\n\n")
    print("Getting your work done........\nAlmost done.....\nDecoded successfully :) ")
    print("\n\nYour decoded Base-64 data is saved in " + args.output_filename )
