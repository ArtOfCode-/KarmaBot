from Module import Command
import re
import math
from random import randint
import SaveIO

# Configuration
save_subdir = 'say'

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
        
def get_random_line(file):
    file = SaveIO.load(save_subdir,file,'txt')
    list_lines = file.splitlines()
    n_lines = len(list_lines)
    if n_lines>0:
	    message = list_lines[randint(0,n_lines-1)]
    else:
        message = "I am at loss for words. Contact my owner"
    return message    


def command_hi(cmd, bot, args, msg, event):
    return get_random_line('Greetings')
    	
    	
def command_thanks(cmd,bot,args,msg,event):
    return get_random_line('Thanks')
    
def command_emot(cmd,bot,args,msg,event):
    return get_random_line('Smile')

def command_bye(cmd,bot,args,msg,event):
    return get_random_line('Goodbye')

def command_say(cmd, bot, args, msg, event):
    try:
        message = re.sub(r'@', '', bot.command("read {{randomint 1 27532246}}", msg, event))
        while "message not found" in message:
            message = re.sub(r'@', '', bot.command("read {{randomint 1 27532246}}", msg, event))
        return message
    except:
        return "*Unavailable right now - try again.*"
        

def command_say_n(cmd, bot, args, msg, event):
    if len(args) < 1:
        return "Not enough arguments!"
    try:
        repeats = int(args[0])
    except:
        return "Argument #1 is not a number."
    messages = []
    for i in range(repeats):
        messages.append(command_say(cmd, bot, args, msg, event))
    return " ".join(messages)
    
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

def parse_repeat(cmd):
    if cmd.startswith('repeat '):
        return cmd[7:].split(' ', 1)
    else:
        return False

def command_repeat(cmd, bot, args, msg, event):
    if len(args) < 2:
        return "Not enough arguments. Syntax: `$PREFIXrepeat <num_repeat> <message>`."
    else:
        try:
            num_repeat = int(args[0])
        except ValueError:
            return "Argument #1 (num_repeat) is not an integer."
        return drop(-1, (args[1] + " ") * num_repeat)
        
def command_sup(cmd, bot, args, msg, event):
    return bot.command("cat {{hi}} {{say}} {{smile}}", msg, event)


def command_wiseman(cmd, bot, args, msg, event):
    return bot.command("cat A wise man says: '*{{say}}*', but a wiser man says: '*{{say}}*'", msg, event)
    
def command_duck(cmd, bot, args, msg, event):
    return "\n>(.)__\n_(___/____\|/"

commands = [
    Command('hi', command_hi, 'Greets you.', False, False, None, ['hello']),
    Command('bye', command_bye, 'Greets you.', False, False, None, ['ciao']),
    Command('thanks',command_thanks, 'Acknowledge your thanks',False,False,None,None),
    Command('smile', command_emot, 'Prints an emoticone/smile',False, False, None,None),
    Command('say', command_say, 'Says something to you. Picked at random from the chat network.', False, False, None, None),
    Command('repeat', command_repeat, 'Repeats what you supply to it <num_repeat> times. Syntax: `$PREFIXrepeat <num_repeat> <message>`.', False, False, parse_repeat, None, None, None),
    Command('say_n', command_say_n, '`$PREFIXsay`, but repeated *n* times and concatenated.', False, False, None, None),
    #Command('take', command_take, 'Takes *num_words* from the set of words you provide. Syntax: `$PREFIXtake <num_words> <words>`.', False, False, None,None),
    #Command('drop', command_drop, 'Drops words from the set of words you provide. Syntax: `$PREFIXdrop <num_words> <words>`.', False, False, None, None),
    Command('wise_man', command_wiseman, 'Tells you some wisdom.', False, False, None, None),
    Command('sup', command_sup, 'Ask Karma what\'s going on.', False, False, None, None),
    Command('duck', command_duck, 'Shows some ducks',False,False,None,None)
]

module_name = "say"
