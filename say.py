from Module import Command
import re
import math


def drop(n, l):
     if n >= 0:
         return l[n:]
     else:
         return l[:n]


def take(n, l):
    if n >= 0:
        return l[:n]
    else:
        return l[n:]


def command_say(cmd, bot, args, msg, event):
    try:
        message = re.sub(r'@', '', bot.command("read {{randomint 1 27532246}}", msg, event))
        while "message not found" in message:
            message = re.sub(r'@', '', bot.command("read {{randomint 1 27532246}}", msg, event))
        return message
    except:
        return "*Unavailable right now - try again.*"
        

def command_take(cmd, bot, args, msg, event):
    if len(args) < 2:
        return "Not enough arguments. Syntax: `$PREFIXtake <num_words> <word_set>`."
    else:
        words = args[1:]
        try:
            num_words = int(args[0])
        except ValueError:
            return "Argument #1 (num_words) is not an integer."
        return " ".join(take(num_words, words))

def command_drop(cmd, bot, args, msg, event):
    if len(args) < 2:
        return "Not enough arguments. Syntax: `$PREFIXtake <num_words> <word_set>`."
    else:
        words = args[1:]
        try:
            num_words = int(args[0])
        except ValueError:
            return "Argument #1 (num_words) is not an integer."
        return " ".join(drop(num_words, words))


commands = [
    Command('say', command_say, 'Says something to you. Picked at random from the chat network.', False, False, None, None),
    Command('take', command_take, 'Takes *num_words* from the set of words you provide. Syntax: `$PREFIXtake <num_words> <words>`.', False, False, None, None),
    Command('drop', command_drop, 'Drops words from the set of words you provide.', False, False, None, None)
]

module_name = "say"
