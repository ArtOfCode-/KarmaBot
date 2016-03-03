from Module import Command
import re
import math
from random import randint
import SaveIO

# Configuration
save_subdir = 'say'


def command_hi(cmd, bot, args, msg, event):
    greetings = SaveIO.load(save_subdir,'Greetings','txt')
    list_greetings = greetings.splitlines()
    n_greetings = len(list_greetings)
    if n_greetings>0:
	    message = list_greetings[randint(0,n_greetings-1)]
    else:
        message = "I am at loss for words. Contact my owner"
    return message
    	


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


def command_wiseman(cmd, bot, args, msg, event):
    return bot.command("cat A wise man says: '*{{say}}*', but a wiser man says: '*{{say}}*'", msg, event)

commands = [
    Command('hi', command_hi, 'Greets you.', False, False, None, None),
    Command('say', command_say, 'Says something to you. Picked at random from the chat network.', False, False, None, None),
    Command('repeat', command_repeat, 'Repeats what you supply to it <num_repeat> times. Syntax: `$PREFIXrepeat <num_repeat> <message>`.', False, False, parse_repeat, None, None, None),
    Command('say_n', command_say_n, '`$PREFIXsay`, but repeated *n* times and concatenated.', False, False, None, None),
    Command('wise_man', command_wiseman, 'Tells you some wisdom.', False, False, None, None),
]

module_name = "say"
