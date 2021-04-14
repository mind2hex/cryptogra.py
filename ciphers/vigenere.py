
import argparse

# si key tiene caracteres de espacio, entonces estos van a ser borrados.
# si key tiene caracteres que no estan en el alfabeto, estos van a ser borrados.

def argument_parser():
    parser = argparse.ArgumentParser(prog="vigenere.py", description="vigenere cipher python tool... Le chiffre indechiffrable", \
                                     usage="./vigenere.py {-e|-d|-b} {-t <str>|-f <filename>} {-k <key>} [-h|--output <f>|...]")
    parser.add_argument("-k", "--key", type=str, required=True, \
                        help="Specify key to encrypt/decrypt the message", metavar="k")
    out_group = parser.add_mutually_exclusive_group(required=False)
    out_group.add_argument("--output", default=False, required=False, metavar="filename", \
                        help="Specify output file to save the result of the program")
    out_group.add_argument("--overwrite", default=False, action="store_true", required=False, \
                        help="If file mode specified as input, then overwrite this file with ciphered output ",)

    parser.add_argument("--dictionary", type=open, metavar="file", help="Specify dictionary file to use with brute mode")
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
        ERROR("argument_parser", "specified file doesn't exist")

    try:
        result.text=" ".join(result.text)
    except:
        pass

    return { "key":result.key, "target":{ "text":result.text, "file":result.file.name }, "dict":result.dictionary, \
           "mode":{ "encrypt":result.encrypt, "decrypt":result.decrypt, "brute":result.brute }, \
           "output":result.output, "abc":result.abecedary.lower(), "overwrite":result.overwrite }

def generate_vigenere_table(abc="abcdefghijklmnopqrstuvwxyz"):
    """ generate_vigenere_table(abc="abcdefghijklmnopqrstuvwxyz")

    This function generates vigenere table and return a list with the table
    [a, b, c]
    [b, c, a]
    [c, a, b]

    """
    lista = []
    aux = []
    for i in range(len(abc)):
        for j in range(len(abc)):
            aux.append(abc[(i+j)%len(abc)])
        lista.append(aux)
        aux = []
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

if __name__ == "__main__":
    arguments = argument_parser()

    if arguments["mode"]["encrypt"] == True:
        if arguments["target"]["text"] != None:   # enc text
            print(encrypt_decrypt_text(arguments["target"]["text"], arguments["key"], abc=arguments["abc"]))
            if arguments["output"] != False:
                with open(arguments["output"], "w") as handler:
                    handler.write(encrypt_decrypt_text(arguments["target"]["text"], arguments["key"], abc=arguments["abc"]))

        elif arguments["target"]["file"] != None:
            info = open(arguments["target"]["file"]).read()
            print(encrypt_decrypt_text(info, arguments["key"], abc=arguments["abc"]))
            if arguments["overwrite"] == True:
                with open(arguments["target"]["file"], "w") as handler:
                    handler.write(encrypt_decrypt_text(info, arguments["key"], abc=arguments["abc"]))

    elif arguments["mode"]["decrypt"] == True:
        if arguments["target"]["text"] != None:
            print(encrypt_decrypt_text(arguments["target"]["text"], arguments["key"], mode="dec", abc=arguments["abc"]))
            if arguments["output"] != False:
                with open(arguments["output"], "w") as handler:
                    handler.write(encrypt_decrypt_text(arguments["target"]["text"], arguments["key"], mode="dec", abc=arguments["abc"]))

        elif arguments["target"]["file"] != None:
            info = open(arguments["target"]["file"]).read()
            print(encrypt_decrypt_text(info, arguments["key"], mode="dec", abc=arguments["abc"]))
            if arguments["overwrite"] == True:
                with open(arguments["target"]["file"], "w") as handler:
                    handler.write(encrypt_decrypt_text(info, arguments["key"], mode="dec", abc=arguments["abc"]))
