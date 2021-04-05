#!/usr/bin/python3

import itertools
import argparse

def argument_parser():
    parser = argparse.ArgumentParser(prog="caesar.py", description="caesar cipher python tool", \
                                     usage="./caesar {-e|-d|-b} {-t <str>|-f <filename>} [-h|-r|--output <n>|...]")
    parser.add_argument("-r", "--rotation", default=13, type=int, required=False, \
                        help="Rotation shift value, should be an integer value", metavar="n")
    parser.add_argument("--output", default=False, required=False, metavar="filename", \
                        help="Specify output file, otherwise modify the original file ")
    parser.add_argument("--overwrite", default=False, action="store_true", required=False, \
                        help="If file mode specified as input, then overwrite this file with ciphered output ",)
                        
    parser.add_argument("--abecedary", default="abcdefghijklmnopqrstuvwxyz", type=str, required=False, \
                        help="Specify custom abecedary, otherwise use the default", metavar="abc")
    
    text_file = parser.add_mutually_exclusive_group(required=True)
    text_file.add_argument("-t","--text", type=str, metavar="str", \
                           help="Encrypt input text", nargs="+" )
    text_file.add_argument("-f","--file", type=open, metavar="file", \
                           help="Encrypt the given file")

    encrypt_decrypt = parser.add_mutually_exclusive_group(required=True)
    encrypt_decrypt.add_argument("-e","--encrypt", default=False, action="store_true", \
                                 help="Encrypt text|file with the given rotation" )
    encrypt_decrypt.add_argument("-d","--decrypt", default=False, action="store_true", \
                                 help="Decrypt text|file with the given rotation" )
    encrypt_decrypt.add_argument("-b","--brute", default=False, action="store_true", \
                                 help="Iterates over all letters of the abecedary" )
    
    try:
        result = parser.parse_args()
    except FileNotFoundError:
        ERROR("argument_parser", "Specified file doesn't exist")

    # Fixing nargs
    try:
        result.text=" ".join(result.text)
    except:
        pass
    

    # Arguments list
    return { "rotation":result.rotation, "target":{ "text":result.text, "file":result.file }, \
             "mode":{ "encrypt":result.encrypt, "decrypt":result.decrypt, "brute":result.brute }, \
             "output":result.output, "abc":result.abecedary.lower(), "overwrite":result.overwrite}


def encrypt_decrypt_text(text, rot=13, abc="abcdefghijklmnopqrstuvwxyz", mode="encrypt"):
    """ cipher_text(text, rot=13, abc="abcdefghijklmnopqrstuvwxyz")
text = plain text to be ciphered
rot  = number of rotation used in caesar cipher
abc  = You can specify a custom abecedary, otherwise use the default

return values:
ciphered_text = text shifted n rotations to the right using the abc variable
    """
    # working with list bc str object doesn't support item assignment
    text=list(text)
    for i in range(len(text)):
        if text[i].isupper() == False:
            if text[i] in abc:
                if mode == "encrypt":
                    index = (abc.index(text[i].lower())+rot)%len(abc)
                elif mode == "decrypt":
                    index = (abc.index(text[i].lower())-rot)
                text[i] = abc[index]
        else:
            if text[i] in abc.upper():
                if mode == "encrypt":
                    index = (abc.index(text[i].lower())+rot)%len(abc)
                elif mode == "decrypt":
                    index = (abc.index(text[i].lower())-rot)
                text[i] = abc[index].upper()
                
    return "".join(text)
    
                                 
def ERROR(function_name, reason):
    print("[X] ERROR...")
    print("[X] FUNCTION:", function_name)
    print("[X] REASON:  ", reason)
    print("----------------------")
    exit()


if __name__ == "__main__":
    arguments = argument_parser()
    
    # encrypt mode
    if arguments["mode"]["encrypt"] == True:
        
        # encrypt text
        if arguments["target"]["text"] != None:

            # saving output if required
            if arguments["output"] != False:
                with open(arguments["output"], "w") as handler:
                    handler.write(encrypt_decrypt_text(arguments["target"]["text"], arguments["rotation"], arguments["abc"]))
                    print("[!] File %s created..."%(arguments["output"]))
                    
            print(encrypt_decrypt_text(arguments["target"]["text"], arguments["rotation"], arguments["abc"]))

        # encrypt file
        if arguments["target"]["file"] != None:
            info = arguments["target"]["file"].read()

            # saving output if required
            if arguments["output"] != False:
                with open(arguments["output"], "w") as handler:
                    handler.write(encrypt_decrypt_text(info, arguments["rotation"], arguments["abc"]))
                    print("[!] File %s created..."%(arguments["output"]))

            # overwritting file if required
            if arguments["overwrite"] == True:
                with open(arguments["target"]["file"].name, "w") as handler:
                    handler.write(encrypt_decrypt_text(info, arguments["rotation"], arguments["abc"]))
            
            print(encrypt_decrypt_text(info, arguments["rotation"], arguments["abc"]))

    # decrypt mode
    if arguments["mode"]["decrypt"] == True:

        # decrypt text
        if arguments["target"]["text"] != None:

            # saving output if required
            if arguments["output"] != False:
                with open(arguments["output"], "w") as handler:
                    info = encrypt_decrypt_text(arguments["target"]["text"], arguments["rotation"], arguments["abc"], mode="decrypt")
                    handler.write(info)
                    print("[!] File %s created..."%(arguments["output"]))
                          
            print(encrypt_decrypt_text(arguments["target"]["text"], arguments["rotation"], arguments["abc"], mode="decrypt"))

        # decrypt file
        if arguments["target"]["file"] != None:
            info = arguments["target"]["file"].read()

            # saving output if required
            if arguments["output"] != False:
                    handler.write(encrypt_decrypt_text(info, arguments["rotation"], arguments["abc"], mode="decrypt"))
                    print("[!] File %s created..."%(arguments["output"]))

            # overwitting file if required
            if arguments["overwrite"] == True:
                with open(arguments["target"]["file"].name, "w") as handler:
                    handler.write(encrypt_decrypt_text(info, arguments["rotation"], arguments["abc"], mode="decrypt"))
                    
            print(encrypt_decrypt_text(info, arguments["rotation"], arguments["abc"], mode="decrypt"))        
        
    # brute mode
    if arguments["mode"]["brute"] == True:
        if arguments["target"]["text"] != None:
            info = arguments["target"]["text"]
        elif arguments["target"]["file"] != None:
            info = arguments["target"]["file"].read()

        for i in range(len(arguments["abc"])):
            print(f"--------> ITERATION {i}")
            print(encrypt_decrypt_text(info, i, arguments["abc"]))
            print("")




## - Brute mode no has output and overwrite mode
## - Refactor the main function
## - sometimes, when i give the progam a custom abecedary, it do weird things






