#!/usr/bin/python3

import argparse
from sys import argv
from subprocess import check_output
from sys import platform
from os import system as command

AUTHOR="mind2hex"
VERSION="[v1.00]"
AVAILABLE_CIPHERS=["caesar"]

def banner():
    msg="""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⢣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                        __
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠎⡴⢦⠱⠀⠀⠀⠀⠀⠀⠀⠀⠀ ____________  ______  / /_____  ____ __________ _  ____  __  __
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢎⣜⣉⣉⣧⡱⡄⠀⠀⠀⠀⠀⠀⠀/ ___/ ___/ / / / __ \/ __/ __ \/ __ `/ ___/ __ `/ / __ \/ / / /
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢃⡞⠒⣒⣒⠒⢳⡘⣄⠀⠀⠀⠀⠀/ /__/ /  / /_/ / /_/ / /_/ /_/ / /_/ / /  / /_/ _ / /_/ / /_/ /
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⢡⣎⡩⠭⠤⠤⠭⢍⣱⡜⣆⠀⠀⠀⠀\___/_/   \__, / .___/\__/\____/\__, /_/   \__,_(_/ .___/\__, /
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⢡⡯⠴⢒⣈⣩⣉⣑⡒⠠⣹⡌⢦⠀⠀⠀         /____/_/              /____/            /_/    /____/
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡔⣡⣣⠔⡺⡋⡁⢀⡀⢈⠙⢟⠢⣝⣄⢢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡜⣰⡟⠁⢰⡓⢎⣀⣸⣿⣷⡱⢚⡆⠈⢻⣆⢣⡀⠀         https://github.com/mind2hex
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠎⡼⣇⠣⡀⠸⡄⢊⢿⣿⣿⡿⡑⢠⠇⢀⠜⣸⢧⠱⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢠⢋⢼⡙⢌⠳⣍⠲⢽⣄⣁⠂⠐⣈⣠⡯⠔⣡⠞⡡⢊⣧⡙⡄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⢃⣞⠣⡙⠦⡑⠦⣍⡒⠤⠬⠭⠭⠥⠤⢒⣩⠴⢊⠴⢋⠜⣳⡘⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣰⣃⣛⣚⣓⣚⣓⣚⣓⣒⣛⣛⣓⣒⣒⣚⣛⣛⣒⣚⣓⣚⣓⣚⣒⣛⣘⣆⠀⠀
    """
    print(msg)
    return 0

def argument_processor(arguments):
    global AVAILABLE_CIPHERS
    
    arguments.pop(0)
    if len(arguments) == 0:
        help_message()
    
    if arguments[0] == "-h" or arguments[0] == "--help":
        help_message()
    elif arguments[0] == "--list-ciphers":
        list_ciphers()
    elif arguments[0] == "--usage":
        usage()
    elif arguments[0] in AVAILABLE_CIPHERS:
        call_ciphers(arguments[0], arguments[1:])
    else:
        ERROR("argument_processor", "Unknown argument %s"%(arguments[0]))        
    

def help_message():
    print("usage: ./cryptogra.py {cipher} *args ")
    print("Positional arguments: ")
    print("  {ciphers}      ; Specify cipher \n")
    print("Optional arguments: ")
    print("  -h, --help     ; Print this help message")
    print("  --list-ciphers ; Print available ciphers")
    print("  --usage        ; Print usage messages")
    exit()

def list_ciphers():
    """ Just print currently available ciphers for this program and then the program is closed """
    global AVAILABLE_CIPHERS
    print("[!] Available ciphers: ")
    for i in range(len(AVAILABLE_CIPHERS)):
            print("         ----> %s.%s"%(i+1, AVAILABLE_CIPHERS[i]))
    exit()
            

def usage():
    """ as it's name tell us, just print usage messages """
    print("[1] Getting help from a cipher ")
    print("    ---> ./cryptogra.py caesar -h ")
    print("")

def ERROR(function_name, reason):
    print("[X] ERROR... ")
    print("[X] FUNCTION: ", function_name)
    print("[X] REASON: ", reason)
    print("----------------------")
    exit()    

######################
##  main functions  ##
######################

def call_ciphers(cipher, *args):
    """
    if platform == "linux":
        result = check_output(["which","python3"]).decode()
    elif platform == "windows":
        result = check_output(["where","python3"]).decode()
    """
    cmd=" ".join(args[0])
    command("./ciphers/%s.py %s"%(cipher, cmd))


if __name__ == "__main__":
    banner()
    argument_processor(argv)



# Improve ERROR function, it's output has an ugly format
