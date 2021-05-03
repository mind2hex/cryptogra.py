#!/usr/bin/python3

import argparse

# si key tiene caracteres de espacio, entonces estos van a ser borrados.
# si key tiene caracteres que no estan en el alfabeto, estos van a ser borrados.

def argument_parser():
    parser = argparse.ArgumentParser(
        description  = "vigenere cipher python tool... Le chiffre indechiffrable", \
        epilog       = "", \
        prog         = "vigenere.py", \
        usage        = "./vigenere.py {-e|-d|-b} {-t <str>|-f <filename>} {-k <key>} [-h|--output <f>|...]", \
        add_help     = True, \
        argument_default = None \
        )

    # MODES
    encrypt_decrypt = parser.add_mutually_exclusive_group(required=True)
    encrypt_decrypt.add_argument("-e","--encrypt", default=False, action="store_true", \
                                 help="Encrypt text|file with the given rotation" )
    encrypt_decrypt.add_argument("-d","--decrypt", default=False, action="store_true", \
                                 help="Decrypt text|file with the given rotation" )
    encrypt_decrypt.add_argument("-b","--brute", default=False, action="store_true", \
                                 help="Iterates over all letters of the abecedary" )
    encrypt_decrypt.add_argument("--table", default=False, action="store_true", help=" Show vigenere table ")

    parser.add_argument("--abecedary", default="abcdefghijklmnopqrstuvwxyz", type=str, required=False, \
                        help="Specify custom abecedary, otherwise use the default", metavar="abc")    

    # Show table mode    
    result = parser.parse_known_args() 
    if result[0].table == True:
        generate_vigenere_table(result[0].abecedary, "print")
        exit()        
    
    # wordlist for bruteforce mode, single keyword for encrypt or decrypt mode
    keys_group = parser.add_mutually_exclusive_group(required=True)
    keys_group.add_argument("-k", "--key", type=str, help="Specify key to encrypt/decrypt the message", metavar="k", nargs="+")
    keys_group.add_argument("--wordlist", type=open, metavar="file", help="Specify wordlist of keys file to use with brute mode")

    # Output to a new file nor overwrite current file
    out_group = parser.add_mutually_exclusive_group(required=False)
    out_group.add_argument("--output", default=False, required=False, metavar="filename", \
                        help="Specify output file to save the result of the program")
    out_group.add_argument("--overwrite", default=False, action="store_true", required=False, \
                        help="If file mode specified as input, then overwrite this file with ciphered output ",)

    text_file = parser.add_mutually_exclusive_group(required=True)
    text_file.add_argument("-t","--text", type=str, metavar="str", \
                           help="Encrypt input text", nargs="+" )
    text_file.add_argument("-f","--file", type=open, metavar="file", \
                           help="Encrypt the given file")

    try:
        result = parser.parse_args()
    except FileNotFoundError:
        ERROR("argument_parser", "specified file doesn't exist")

    if result.brute == True:
        if result.wordlist == None:
            ERROR("argument_parser", "bruteforce mode specified, but no wordlist provided")

    try:
        result.text =" ".join(result.text)
    except:
        pass

    # if result.key == None, then its because is bruteforce mode
    if result.key != None: 
        result.key = " ".join(result.key)
        result.key = result.key.lower()
        result.key = result.key.replace(" ","")
        
        for i in result.key:
            if i not in result.abecedary.lower():
                ERROR("argument_parser", f"character {i} of the key is not in abecedary={result.abecedary}")

    return { "key":result.key, "target":{ "text":result.text, "file":result.file }, "wordlist":result.wordlist, \
           "mode":{ "encrypt":result.encrypt, "decrypt":result.decrypt, "brute":result.brute }, \
           "output":result.output, "abc":result.abecedary.lower(), "overwrite":result.overwrite }


def ERROR(function_name, reason):
    print("[X] ERROR...")
    print("[X] FUNCTION:", function_name)
    print("[X] REASON:  ", reason)
    print("----------------------")
    exit()

def generate_vigenere_table(abc="abcdefghijklmnopqrstuvwxyz", mode="return"):
    """ generate_vigenere_table(abc="abcdefghijklmnopqrstuvwxyz", ["return" || "print"])
    
    This function generates vigenere table and return a list with the table
    [a, b, c]
    [b, c, a]
    [c, a, b]

    and returns or print the table

    """
    lista = []
    aux = []
    for i in range(len(abc)):
        for j in range(len(abc)):
            aux.append(abc[(i+j)%len(abc)])
        lista.append(aux)
        aux = []

    if mode == "print":
        print("  ",end="")
        for i in range(len(lista)):
            print(" %s "%(str(i+1).zfill(2)), end="")
        print()
        for i in lista:
            print("%s"%(str(lista.index(i)+1).zfill(2)), end="")
            for j in i:
                print("  %s "%(j), end="")
            print()
            
    else:
        return lista

def encrypt_decrypt_text(text, key, mode="enc", abc="abcdefghijklmnopqrstuvwxyz"):
    key_index = 0
    result = ""
    if mode == "enc":
        for i in range(len(text)):
            if text[i] in abc:
                result += abc[(abc.index(key[key_index])+abc.index(text[i])) % len(abc)]
                key_index = (key_index + 1) % len(key)
            elif text[i].lower() in abc:
                result += abc[(abc.index(key[key_index])+abc.index(text[i].lower())) % len(abc)].upper()
                key_index = (key_index + 1) % len(key)
            else:
                result += text[i]
    else:
        for i in range(len(text)):
            if text[i] in abc:
                result += abc[abc.index(text[i]) - (abc.index(key[key_index])) % len(abc)]
                key_index = (key_index + 1) % len(key)
            elif text[i].lower() in abc:
                result += abc[abc.index(text[i].lower())-(abc.index(key[key_index])) % len(abc)].upper()
                key_index = (key_index + 1) % len(key)
            else:
                result += text[i]

    return result


def encrypt(text, key, abc="abcdefghijklmnopqrstuvwxyz", output=False):
    """ Call encrypt_decrypt_text function and print his output or save it in a file """
    result = encrypt_decrypt_text(text, key, abc=abc)
    print(result)
    if output != False:
        with open(output, "w") as handler:
            handler.write(result)

def decrypt(text, key, abc="abcdefghijklmnopqrstuvwxyz", output=False, ret=False):
    """ Call encrypt_decrypt_text function and print his output or save it in a file """
    result = encrypt_decrypt_text(text, key, mode="dec", abc=abc)
    if output != False:
        with open(output, "w") as handler:
            handler.write(result)

    if ret == True:
        return result
    else:
        print(result)    


if __name__ == "__main__":
    arguments = argument_parser()
    
    if arguments["mode"]["encrypt"] == True and arguments["target"]["text"] != None:     # Encrypt text mo
        if arguments["output"] == False:
            encrypt(arguments["target"]["text"], arguments["key"], abc=arguments["abc"])
        else:
            encrypt(arguments["target"]["text"], arguments["key"], abc=arguments["abc"], output=arguments["output"])
            
    if arguments["mode"]["encrypt"] == True and arguments["target"]["file"] != None:     # Encrypt file mode
        text = open(arguments["target"]["file"].name, "r").read()
        if arguments["overwrite"] == True:
            encrypt(text, arguments["key"], abc=arguments["abc"], output=arguments["target"]["file"].name)
        elif arguments["output"] != False:
            encrypt(text, arguments["key"], abc=arguments["abc"], output=arguments["output"])
        else:
            encrypt(text, arguments["key"], abc=arguments["abc"])

    ########
    ########

    if arguments["mode"]["decrypt"] == True and arguments["target"]["text"] != None:     # DEcrypt text mode
        if arguments["output"] == False:
            decrypt(arguments["target"]["text"], arguments["key"], abc=arguments["abc"])
        else:
            decrypt(arguments["target"]["text"], arguments["key"], abc=arguments["abc"], output=arguments["output"])

    if arguments["mode"]["decrypt"] == True and arguments["target"]["file"] != None:     # DEcrypt file mode
        text = open(arguments["target"]["file"].name, "r").read()
        if arguments["overwrite"] == True:
            decrypt(text, arguments["key"], abc=arguments["abc"], output=arguments["target"]["file"].name)
        elif arguments["output"] != False:
            decrypt(text, arguments["key"], abc=arguments["abc"], output=arguments["output"])
        else:
            decrypt(text, arguments["key"], abc=arguments["abc"])    

    if arguments["mode"]["brute"] == True:
        handler = open(arguments["wordlist"].name)
        with open(arguments["wordlist"].name, "r") as handler:
            for key in handler:
                if len(key) == 0 or key == "\n":
                    continue
                print("=====key=====> %s"%(key.rstrip("\n")))
                decrypt(arguments["target"]["text"], key.rstrip("\n"))
                print()
                
        if arguments["target"]["file"] != None:
            ERROR("__main__", "bruteforce vigenere ciphered files is not available yet")
