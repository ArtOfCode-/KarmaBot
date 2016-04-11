# Copyright (C) 2015 Owen Jenkins                                                   #
#                                                                                   #
# This program is free software: you can redistribute it and/or modify              #
# it under the terms of the GNU General Public License as published by              #
# the Free Software Foundation, either version 3 of the License, or                 #
# (at your option) any later version.                                               #
#                                                                                   #
# This program is distributed in the hope that it will be useful,                   #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                    #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                     #
# GNU General Public License for more details.                                      #
#                                                                                   #
# You should have received a copy of the GNU General Public License                 #
# along with this program.  If not, see <http://www.gnu.org/copyleft/gpl.html>.     #

# imports
from Module import Command
import SaveIO

# config options
save_subdir = "points"

# data stores
Points = {
    # 'username': points
    'karmabot': 9999999999999999
}

Stars = {
    # msg_id: 'username'
}

Pins = {
    # msg_id: 'username'
}

# handlers
def on_bot_load(bot):
    global Points
    global Stars
    global Pins
    Points = SaveIO.load(save_subdir, 'Points_Data')
    Stars = SaveIO.load(save_subdir, 'Stars_Data')
    Pins = SaveIO.load(save_subdir, 'Pins_Data')

def on_bot_stop(bot):
    global Points
    global Stars
    global Pins
    SaveIO.save(Points, save_subdir, 'Points_Data')
    SaveIO.save(Stars, save_subdir, 'Stars_Data')
    SaveIO.save(Pins, save_subdir, 'Pins_Data')

# helper methods

def format_user_name(user):
    usr = user.replace(' ','')
    return usr.lower()

def change_points(user_raw, amount=0, is_admin=False, list_current_users=""):
    global Points

    user = format_user_name(user_raw)

    if user not in Points:
        Points[user] = 200
        return user + ' is given a welcome budget of 200 points'

    if not is_admin and Points[user] + amount < 0:
            return False

    Points[user] += amount

    try:
	    SaveIO.save(Points, save_subdir, 'Points_Data')
	    return "Changed points for " + user + " by " + str(amount) + ". New total: " + str(Points[user])
    except:
	    SaveIO.save(Points, save_subdir, 'Points_Data')
	    return "An error occurred, but the points transfer *has* taken place."


# commands

def give_points(cmd, bot, args, msg, event):
    if len(args) < 2:
        return "Not enough arguments."

    user = format_user_name(args[0])
    amount = args[1]

    if "-" in amount:
        return "You cannot take points from a user."
    try:
        amount = int(amount)
    except:
        return "Invalid amount."

    negAmount = -amount
    negUser = format_user_name(event.user.name)

    remove = change_points(negUser, negAmount)
    if remove == False:
        return "You do not have enough points to give that many away."
        
    if user in bot.command('getcurrentusers pingformat',msg,event).lower():
        result = change_points(user, amount)
        return result
    else:
        return 'I don\'t think I had the pleasure of meeting '+user


def admin_points(cmd, bot, args, msg, event):
    if len(args) < 2:
        return "Not enough arguments."

    user = format_user_name(args[0])
    amount = args[1]

    try:
        amount = int(amount)
    except:
        return "Invalid amount."

    result = change_points(user, amount, True)
    return result


def get_points(cmd, bot, args, msg, event):
    user = ""
    if len(args) == 0:
        user = format_user_name(event.user.name)
    elif len(args) >= 1:
        user = format_user_name(args[0])

	
    if user in Points:
        return str(Points[user])
    else:
        list_current_users = bot.command('getcurrentusers pingformat',msg,event).lower()
        if user in list_current_users:
	        return change_points(user)
        else:
	        return 'I am not sure I met ' + user


def show_points(cmd, bot, args, msg, event):
    message = "Here are the points collected by the users:"
    print_all = False
    
    if len(args) >= 1:
        if "all" in args[0].lower():
            print_all = True
            
    for user in Points:
        if Points[user] == 0 and not print_all:
            continue
        
        message = message + "\n " + str(user) + ": " + str(Points[user])
        
    return message

    
def prune_points(cmd, bot, args, msg, event):
    global Points
    users_to_delete = []
    for user in Points:
        if Points[user] == 0:
            users_to_delete.append(user)
    for u in range(len(users_to_delete)):
        del Points[users_to_delete[u]]
    return "User with 0 points have been removed from list"

def clear_points(cmd, bot, args, msg, event):
    global Points
    Points.clear()
    return "List of points cleared. You can start again."


def star(cmd, bot, args, msg, event):
    global Stars

    if len(args) < 1:
        return "Not enough arguments."
    id_ = args[0]
    user = format_user_name(event.user.name)

    try:
        id_ = int(id_)
    except:
        return "Invalid arguments."

    try:
        message = bot.client.get_message(id_)
    
        if not message.starred_by_you and id_ in Stars:
            return "This message cannot be starred because a moderator has removed votes."
        if message.starred_by_you or id_ in Stars:
            return "This message has already been starred by someone else."
        if message.owner.name == "KarmaBot":
            return "I can't star my own messages."
    
        result = change_points(user, -100)
    
        if not result:
            return "You don't have enough points to pin a message."
    
        message.star()
        Stars[id_] = user
        SaveIO.save(Stars, save_subdir, 'Stars_Data')
        return "Message starred. You have been charged 100 points."
    except: 
        return "Message not found."


def pin(cmd, bot, args, msg, event):
    global Pins
    if len(args) < 1:
        return "Not enough arguments."
    id_ = args[0]
    user = format_user_name(event.user.name)
    try:
        id_ = int(id_)
    except:
        return "Invalid arguments."
    try:
        message = bot.client.get_message(id_)
        
        if not message.pinned and id_ in Pins:
            return "This message cannot be pinned because a moderator has removed votes."
        if message.pinned or id_ in Pins:
            return "This message has already been pinned."
        if message.owner.name == 'KarmaBot':
            return "I can't pin my own messages. This is a design decision because of a bug in chat."
            
        result = change_points(user, -500)
        
        if not result:
            return "You don't have enough points to pin a message."
            
        message.pin()
        Pins[id_] = user
        SaveIO.save(Pins, save_subdir, 'Pins_Data')
        return "Message pinned. You have been charged 500 points."
        
    except: 
        return "Message not found"


def unstar(cmd, bot, args, msg, event):
    global Stars
    is_admin = False
    for i in bot.owners:
        if event.user.id == i["stackexchange.com"]:
            is_admin = True
        else:
            continue
    if len(args) < 1:
        return "Not enough arguments."
    id_ = args[0]
    user = format_user_name(event.user.name)
    try:
        id_ = int(id_)
    except:
        return "Invalid arguments."
    message = bot.client.get_message(id_)
    if not message.starred_by_you:
        if id_ in Stars:
            del Stars[id_]
            return "The stars on that message have been removed by a moderator. I had previously starred it, and I can't star it again."
        return "This message isn't starred."
    if not Stars[id_] == user and not is_admin:
        return "You cannot unstar a message someone else starred."
    message.star(False)
    del Stars[id_]
    SaveIO.save(Stars, save_subdir, 'Stars_Data')
    return "Message unstarred."


def unpin(cmd, bot, args, msg, event):
    global Pins
    is_admin = False
    for i in bot.owners:
        if event.user.id == i["stackexchange.com"]:
            is_admin = True
        else:
            continue
    if len(args) < 1:
        return "Not enough arguments."
    id_ = args[0]
    user = format_user_name(event.user.name)
    try:
        id_ = int(id_)
    except:
        return "Invalid arguments."
    message = bot.client.get_message(id_)
    if not message.pinned:
        if id_ in Pins:
            del Pins[id_]
            return "The pins on that message have been removed by a moderator. I had previously pinned it, and I can't do so again."
        return "This message isn't pinned."
    if not Pins[id_] == user and not is_admin:
        return "You cannot unpin a message someone else pinned."
    message.pin(False)
    del Pins[id_]
    SaveIO.save(Pins, save_subdir, 'Pins_Data')
    return "Message unpinned."


commands = [
    Command('givepoints', give_points, "Transfers points from you to another user. Syntax: `givepoints <user> <amount>",
            False),
    Command('adminpoints', admin_points,
            "Administrates points - like `givepoints` but without transfer or restriction.", True),
    Command('getpoints', get_points,
            "Tells you how many points someone has. Syntax: `getpoints` or `getpoints <user>`", False),
    Command('showpoints', show_points,
            "List all the points from all users. Syntax: `getpoints`", False),
    Command('prunepoints', prune_points,
            "Remove users from list when they have 0 points. Syntax: `prunepoints`", True),
    Command('star', star,
            "Stars a message. You can't star my messages or messages I've already starred. Syntax: `star <id>`", False),
    Command('pin', pin,
            "Pins a message. You can't pin a message that's already pinned. Syntax: `pin <id>`", False),
    Command('unstar', unstar,
            "Unstars a message. You can't unstar a message someone else starred. Syntax: `unstar <id>`", False),
    Command('unpin', unpin,
            "Unpins a message. You can't unpin a message someone else pinned. Syntax: `unpin <id>`", False),
    Command('clearpoints',clear_points,'Remove all users from the points list', True)
]