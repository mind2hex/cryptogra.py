# cryptogra.py
_Simple cryptography command line tool

## Information
_The main program is cryptogra.py but every cipher is a program himself. Ciphers are located inside ciphers directory.

### Current ciphers available:
* caesar.py

### Basic usage
```
$ ./cryptogra.py -h
                         __
  ____________  ______  / /_____  ____ __________ _  ____  __  __
 / ___/ ___/ / / / __ \/ __/ __ \/ __ `/ ___/ __ `/ / __ \/ / / /
/ /__/ /  / /_/ / /_/ / /_/ /_/ / /_/ / /  / /_/ _ / /_/ / /_/ /
\___/_/   \__, / .___/\__/\____/\__, /_/   \__,_(_/ .___/\__, /
         /____/_/              /____/            /_/    /____/
               __...--~~~~~-._   _.-~~~~~--...__
             //               `V'               \
            //                 |                 \
           //__...--~~~~~~-._  |  _.-~~~~~~--...__\
          //__.....----~~~~._\ | /_.~~~~----.....__\
         ====================\|//====================
                         dwb `---`

usage: ./cryptogra.py {cipher} *args
Positional arguments:
  {ciphers}      ; Specify cipher

Optional arguments:
  -h, --help     ; Print this help message
  --list-ciphers ; Print available ciphers
  --usage        ; Print usage messages
  --quiet        ; Don't print banner
  
 $ ./criptogra.py --quiet caesar -h
 usage: ./caesar {-e|-d|-b} {-t <str>|-f <filename>} [-h|-r|--output <n>|...]

caesar cipher python tool

optional arguments:
  -h, --help            show this help message and exit
  -r n, --rotation n    Rotation shift value, should be an integer value
  --output filename     Specify output file, otherwise modify the original file
  --overwrite           If file mode specified as input, then overwrite this file with ciphered output
  --abecedary abc       Specify custom abecedary, otherwise use the default
  -t str [str ...], --text str [str ...]
                        Encrypt input text
  -f file, --file file  Encrypt the given file
  -e, --encrypt         Encrypt text|file with the given rotation
  -d, --decrypt         Decrypt text|file with the given rotation
  -b, --brute           Iterates over all letters of the abecedary
```
