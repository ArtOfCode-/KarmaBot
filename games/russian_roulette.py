from Module import Command
from random import randint

gamestate = {
        "preparing" : False,
        "playing"   : False,
        "players"   : [],
        "duds"      : 0,
    }

def command_russian_roulette(cmd, bot, args, msg, event):
    if len(args) == 1:
        if args[0] == "prepare":
            return rr_prepare(cmd, bot, args, msg, event)
        if args[0] == "join":
            return rr_join(cmd, bot, args, msg, event)
        if args[0] == "start":
            return rr_start(cmd, bot, args, msg, event)
        if args[0] == "trigger":
            return rr_trigger(cmd, bot, args, msg, event)
        if args[0] == "stop":
            return rr_stop(cmd, bot, args, msg, event)
    return "I didn't understand your arguments. Use *help russian_roulette* to get more info."

def rr_prepare(cmd, bot, args, msg, event):
    global gamestate
    if gamestate["preparing"]:
        return "Already preparing, *join* already!"
    if gamestate["playing"]:
        return "Already playing, *trigger* already!"
    
    gamestate["preparing"] = True
    
    currentUsers

def rr_join(cmd, bot, args, msg, event):
    pass

def rr_start(cmd, bot, args, msg, event):
    pass

def rr_trigger(cmd, bot, args, msg, event):
    pass

def rr_stop(cmd, bot, args, msg, event):
    pass