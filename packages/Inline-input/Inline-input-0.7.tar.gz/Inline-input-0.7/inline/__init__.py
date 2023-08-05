from thefuzz import process, utils
from colorama import Fore, init
import msvcrt as m
import ctypes
import ctypes.wintypes as w
from time import time, sleep
init(autoreset=True)
commands = None
autoCompleteOnEnter = False
CF_UNICODETEXT = 13
u32 = ctypes.WinDLL('user32')
k32 = ctypes.WinDLL('kernel32')
OpenClipboard = u32.OpenClipboard
OpenClipboard.argtypes = w.HWND,
OpenClipboard.restype = w.BOOL
GetClipboardData = u32.GetClipboardData
GetClipboardData.argtypes = w.UINT,
GetClipboardData.restype = w.HANDLE
GlobalLock = k32.GlobalLock
GlobalLock.argtypes = w.HGLOBAL,
GlobalLock.restype = w.LPVOID
GlobalUnlock = k32.GlobalUnlock
GlobalUnlock.argtypes = w.HGLOBAL,
GlobalUnlock.restype = w.BOOL
CloseClipboard = u32.CloseClipboard
CloseClipboard.argtypes = None
CloseClipboard.restype = w.BOOL

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


def get_clip():
    if OpenClipboard(None):
        h_clip_mem = GetClipboardData(CF_UNICODETEXT)
        text = ctypes.wstring_at(GlobalLock(h_clip_mem))
        GlobalUnlock(h_clip_mem)
        CloseClipboard()
        return text
    else:
        return ""

def clear_console(pred, inp):
    if len(pred.split("\n")) > len(inp.split("\n")):
        text = pred
    else:
        text = inp
    if (text is None) or (len(text.split("\n")) == 0):
        print("\x1b[2K\r" + "\033[%d;A" % (1), end="\r")
    else:
        for i in range(len(text.split("\n"))-1):
            print("\x1b[2K\r" + "\033[%d;A" % (1), end="\r")

def input(prefix=">> ", free=True, minLength=0, maxLength=0, command=None, timeInfo=None):
    lastpred = ""
    print(prefix, end=f' \b')
    inp = ""
    pred = ""
    postfix = ""
    curposx = 0
    isprediction = True
    predvsinp = False
    isCleared = False
    isSelected = False

    s_time = time() - 0.1
    if timeInfo is None:
        timeInfo = 3 * 10 #3 sec
        ipostfix = timeInfo
    else:
        timeInfo = timeInfo * 10
        ipostfix = timeInfo

    if command is None:
        if commands is None:
            isprediction = False
        else:
            command = commands

    if minLength >= maxLength:
        if maxLength != 0:
            minLength = 0
            maxLength = 0

    while True:
        kbh = m.kbhit()
        if kbh or s_time + 0.1 < time():
            s_time = time()
            lentext = 0
            if kbh:
                key = m.getwch()
                skey = key.encode('utf-8')
                postfix = ""
                ipostfix = timeInfo
                s_time = time() - 0.1
                
            if not kbh:
                if ipostfix > 0 and len(postfix) > 5:
                    if postfix.endswith(f" ({(ipostfix+1) / 10}c)"):
                        postfix = postfix.replace(f" ({(ipostfix+1) / 10}c)", f" ({ipostfix / 10}c)")
                    else:
                        postfix += f" ({ipostfix / 10}c)"
                    ipostfix -= 1
                else:
                    postfix = ""

                key, skey = "", ""
            elif skey == b'\x01':
                if isSelected:
                    isSelected = False
                    postfix = "<F>Disable text select."
                elif len(inp) == 0:
                    postfix = "<F>No text to select."
                else:
                    isSelected = True
                    postfix = "All text selected."
            elif skey == b'\x16':
                cliptext = get_clip()
                if cliptext == "":
                    postfix = "<F>Clipboard is empty."
                else:
                    inp += cliptext
                    postfix = "Text pasted!"
                
            elif skey == b'\xc3\xa0' and key == "à":
                key = m.getwch()
                if key == "K":
                    if not (curposx >= len(inp)):
                        curposx += 1
                    else:
                        postfix = "<F>The cursor is already left."
                elif key == "M":
                    if not (curposx <= 0):
                        curposx -= 1
                    else:
                        postfix = "<F>The cursor is already right."
                elif key == "H":
                    postfix =  "<F>Can't move the cursor up."
                elif key == "P":
                    postfix =  "<F>Can't move the cursor down."
                elif key == "R":
                    postfix = "<F>Can't insert."
                elif key == "G":
                    postfix = "<F>Can't home."
                elif key == "I":
                    postfix = "<F>Can't Page Up."
                elif key == "S":
                        postfix = "<F>You can't delete."
                elif key == "O":
                    postfix = "<F>Can't end."
                elif key == "Q":
                    postfix = "<F>Can't Page Down."
                else:
                    postfix = "<F>Unknown key."

            elif skey == b'\x1b':
                postfix = "<F>You can't esc."
            elif skey == b"\x08":
                if isSelected:
                    if len(inp) != 0:
                        inp = ""
                    else:
                        postfix = "<F>You can't delete."
                else:
                    if curposx == 0:
                        if len(inp) != 0:
                            inp = inp[:-1]
                        else:
                            postfix = "<F>You can't delete."
                    else:
                        if len(inp[:-curposx]) != 0:
                            inp = inp[:-1-curposx] + inp[-curposx:]
                        else:
                            postfix = "<F>You can't delete."
            elif skey == b'\t':
                if pred != None:
                    inp = pred
                    postfix = "Autocompletion successfully."
                else:
                    postfix = "<F>No suggestion for autocompletion."
            elif skey == b'\r':
                if minLength == 0 or len(inp) >= minLength:
                    if maxLength == 0 or len(inp) <= maxLength:
                        if free:
                            if isCleared:
                                clear_console(lastpred, inp)
                                print("\x1b[2K\r", end='\r')
                            else:
                                isCleared = True
                            return inp
                        else:
                            if inp in command or autoCompleteOnEnter:
                                if isCleared:
                                    clear_console(lastpred, inp)
                                    print("\x1b[2K\r", end='\r')
                                else:
                                    isCleared = True
                                if autoCompleteOnEnter:
                                    return pred
                                else:
                                    return inp
                            else:
                                postfix =  "<F>Doesn't match commands."
                    else:
                        postfix =  f"<F>Max length is {maxLength} characters."
                else:
                    postfix =  f"<F>Min length is {minLength} characters."
            elif len(key) == 1:
                if isSelected:
                    inp = ""
                if curposx == 0:
                    inp += key
                else:
                    inp = inp[:-curposx] + key + inp[-curposx:]
            else:
                postfix = "<F>Unknown key."

            if skey != b'\x01':
                isSelected = False
                
            print("\x1b[2K\r" + "\033[1;A")
            if isprediction:
                pred, score = predict(inp, command)
            else:
                pred = None

            postfixlen = len(postfix.replace("<F>", ""))
            lentext += postfixlen
            if postfix.startswith("<F>"):
                colored_postfix = Fore.RED + postfix.replace("<F>", "")
            else:
                colored_postfix = Fore.GREEN + postfix
            if pred != None:
                if isCleared:
                    clear_console(lastpred, inp)
                else:
                    isCleared = True

                isSimilar = pred[:len(inp)].lower() == inp.lower()
                output = prefix + inp + Fore.LIGHTBLACK_EX + pred[len(inp):]

                if len(pred) - len(inp) > 0:
                    lentext += len(pred) - len(inp)

                if score > 0:
                    if isSimilar:
                        print(output + f" ({score}%) " + colored_postfix, end='\b' * (lentext + len(f" ({score}%) ") + curposx))
                    else:
                        if len(pred.split("\n")) > 0:
                            pred_ = pred.split("\n")[len(inp.split("\n"))-1].replace("\n", "")
                            print(output + f"  [{pred_}] - ({score}%) " + colored_postfix, end='\b' * (lentext + len(f"  [{pred_}] - ({score}%) ") + curposx))
                        else:
                            print(output + f"  [{pred}] - ({score}%) " + colored_postfix, end='\b' * (lentext + len(f"  [{pred}] - ({score}%) ") + curposx))
                else:
                    if isSimilar:
                        print(output + colored_postfix, end='\b' * lentext)
                    else:
                        print(output + f"  [{pred}] " + colored_postfix, end='\b' * (lentext + len(f"  [{pred}] ") + curposx))
                lastpred = pred
            else:
                if isCleared:
                    clear_console(lastpred, inp)
                else:
                    isCleared = True
                lastpred = ""
                curposx = 0

                print("\x1b[2K\r", end='\r')
                print(prefix + inp + "  " + colored_postfix, end='\b' * (postfixlen + len("  ")))