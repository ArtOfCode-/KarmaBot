from Module import Command
from ChatExchange3.chatexchange3.messages import Message
import re
from random import randint

module_name = "gtc"

last_room = None

def get_message_text(message):
    return re.sub(r'^:[0-9]+ ', '', message.content_source)

def new_gtc(bot):
    message_id = randint(1, 24300000)
    message = Message(message_id, bot.client)
    global last_room
    last_room = message.room
    return str.format("{0}: '{1}' said: {2}", message.time_stamp, message.owner, get_message_text(message))

def check_gtc(solution):
    if last_room is None:
        return "No running GTC challenge. Start one with `$PREFIXgtc`."
    else:
        try:
            if int(solution) == last_room.id:
                return "Correct!"
            else:
                return "Try again."
        except ValueError:
            if solution == last_room.name:
                return "Correct!"
            else:
                return "Try again."

def command_gtc(cmd, bot, args, msg, event):
    if(len(args) == 0):
        return new_gtc(bot)
    else:
        return check_gtc(args[0])

commands = [
    Command("gtc", command_gtc, "Guess the Chatroom game. Run `$PREFIXgtc` to start a new challenge, or `$PREFIXgtc "
            + "<solution>` to check your guess.")
]
