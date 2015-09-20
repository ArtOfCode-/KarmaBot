from Module import Command
import SaveIO

save_subdir = 'genius'

Medals = {
    # 'username': total
}

def on_bot_load(bot):
    global Medals
    Medals = SaveIO.load(save_subdir, "Medals_Data")


def on_bot_stop(bot):
    global Medals
    SaveIO.save(Medals, save_subdir, "Medals_Data")


def give_medal(cmd, bot, args, msg, event):
    global Medals
    if len(args) < 1:
        return "Not enough arguments."
    username = args[0]
    if username not in Medals:
        Medals[username] = 0
    Medals[username] += 1
    SaveIO.save(Medals, save_subdir, "Medals_Data")
    return str.format("Given {0} a genius medal. Total: {1}", username, Medals[username])


def print_medals(cmd, bot, args, msg, event):
    medal_list = "Who's Got Medals:\n"
    for k, v in Medals.items():
        medal_list += str.format("{0} has {1}\n", k, v)
    return medal_list


commands = [
    # Command( '<command name>', <command exec name>, '<help text>' (optional), <needs privilege> (= False) ),
    Command('givemedal', give_medal, "Gives a user a 'genius medal'. Privileged users only.", True),
    Command('showmedals', print_medals, "Prints a list of who's got how many medals.", False)
]