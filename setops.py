from Module import Command

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
        
        
def command_split(cmd, bot, args, msg, event):
    if len(args) < 1:
        return "Not enough arguments. Syntax: `$PREFIXsplit <text>`."
    else:
        return " ".join(list("".join(args)))
        

def command_join(cmd, bot, args, msg, event):
    if len(args) < 1:
        return "Not enough arguments. Syntax: `$PREFIXjoin <text>`."
    else:
        return "".join(args)
        
commands = [
    Command('take', command_take, 'Takes *num_words* from the set of words you provide. Syntax: `$PREFIXtake <num_words> <words>`.', False, False, None, None),
    Command('drop', command_drop, 'Drops words from the set of words you provide. Syntax: `$PREFIXdrop <num_words> <words>`.', False, False, None, None),
    Command('split', command_split, '$PREFIXsplit <text> splits the text at every character.', False, False, None, None),
    Command('join', command_join, 'Joins all text, effectively removing all whitespace.', False, False, None, None)
]

module_name = "setops"
