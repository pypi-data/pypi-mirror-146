from thefuzz import process, utils
from colorama import Fore, Back, Style, init
import msvcrt as m
init(autoreset=True)
commands = None

def predict(text, list=None):
    if list is None:
        if commands is None:
            return None, None
        else:
            list = commands

    if utils.full_process(text):
        pred, score = process.extractOne(text, list)
        return pred, score
    else:
        return None, None

def isCommand(text, command=None):
    if command is None:
        if commands is None:
            return False
        else:
            command = commands
    if text in command:
        return True
    else:
        return False

def input(prefix=">> ", free=True, minLength=0, command=None):
    inp = ""
    print(prefix, end=f' \b')
    pred = ""
    isprediction = True
    if command is None:
        if commands is None:
            isprediction = False
        else:
            command = commands
        
    while True:
        if m.kbhit():
            postfix = ""
            key = m.getwch()
            skey = key.encode('utf-8')
            if skey == b"\x08":
                inp = inp[:-1]
            elif skey == b'\t':
                if pred != None:
                    inp = pred
            elif skey == b'\r':
                if minLength == 0 or len(inp) >= minLength:
                    if free:
                        print('\x1b[2K\r', end='\r')
                        return inp
                    else:
                        if inp in command:
                            print('\x1b[2K\r', end='\r')
                            return inp
                        else:
                            postfix =  "Err: doesn't match commands."
                else:
                    postfix =  f"Err: min length is {minLength} characters."
            elif len(key) == 1:
                inp += key
            else:
                continue
            
            print('\x1b[2K', end='\r')
            if isprediction:
                pred, score = predict(inp, command)
            else:
                pred = None

            if pred != None:
                isSimilar = pred[:len(inp)].lower() == inp.lower()
                output = prefix + inp + Fore.LIGHTBLACK_EX + pred[len(inp):]

                if len(pred) - len(inp) <= 0:
                    lentext = 0
                else:
                    lentext = len(pred) - len(inp)

                lentext += len(postfix)
                postfix = Fore.RED + postfix

                if score > 0:
                    if isSimilar:
                        print(output + f" ({score}%) " + postfix, end='\b' * (lentext + len(f" ({score}%) ")))
                    else:
                        print(output + f"  [{pred}] - ({score}%) " + postfix, end='\b' * (lentext + len(f"  [{pred}] - ({score}%) ")))
                else:
                    if isSimilar:
                        print(output + postfix, end='\b' * lentext)
                    else:
                        print(output + f"  [{pred}]" + postfix, end='\b' * (lentext + len(f"  [{pred}]")))
            else:
                postfixlen = len(postfix + "  ")
                postfix = Fore.RED + postfix
                print(prefix + inp + "  " + postfix, end='\b' * postfixlen)