from Module import Command
import threading
import time
from ChatExchange6.chatexchange6.events import MessagePosted, MessageEdited
from ChatExchange6.chatexchange6.messages import Message

#---------------------------------------------
class User:
    def __init__(self, name):
        self.name = name
        self.heuristic_start = time.time()
        self.last_action = time.time()
    
    def update(self):
        global same_action_delay
        global warning_time
        
        current = time.time()
        if (current - self.last_action) > same_action_delay:
            self.heuristic_start = current
        
        self.last_action = current
        
        should_warn = (self.last_action - self.heuristic_start) > warning_time
        
        if should_warn:
            self.heuristic_start = self.last_action
        
        return should_warn
            
#---------------------------------------------

thread_lock = threading.Lock()
same_action_delay = 5*60            # MAGIC NUMBER Time between two actions to belong together. Should be high enough to account for typing.
warning_time =      30*60           # MAGIC NUMBER If user is chatting longer than this Karma issues a warning
work_vars = {
    'running':    False,
    'working':    dict(),
    'pausing':    dict(),
    'thread':     None,
    'bot':        None,
}

#---------------------------------------------

def command_work(cmd, bot, args, msg, event):
    if len(args) < 1:
        return "I need arguments! Use *work help*"
    
    if args[0] == "start":
        return work_start(bot, args, msg, event)
    
    if args[0] == "stop":
        return work_stop(bot, args, msg, event)
    
    if args[0] == "pause":
        return work_pause(bot, args, msg, event)
    
    if args[0] == "unpause":
        return work_start(bot, args, msg, event)
    
    if args[0] == "status":
        return work_plugin_status(bot, args, msg, event)
    
    if len(args) >= 2:
        if args[0] == "plugin":
            if args[1] == "start":
                return work_plugin_start(bot, args, msg, event)
            if args[1] == "stop":
                return work_plugin_stop(bot, args, msg, event)
    
    return "Sorry, I don't understand your arguments. Use *help work* to learn more."

#---------------------------------------------

def work_start(bot, args, msg, event):
    global work_vars
    global thread_lock
    
    thread_lock.acquire()                       # Lock acquire
    if not work_vars['running']:
        thread_lock.release()
        return "Plugin not running, use *plugin start* first."
    
    if event.user.name in work_vars['working']:
        thread_lock.release()                   # Lock release
        return "You're already in the list."
    if event.user.name in work_vars['pausing']:
        work_vars['working'][event.user.name] = work_vars['pausing'][event.user.name]
        del work_vars['pausing'][event.user.name]
        thread_lock.release()                   # Lock release
        return "You have been moved from *pausing* to *working*."
    work_vars['working'][event.user.name] = User(event.user.name)
    thread_lock.release()                       # Lock release
    
    return "has been added to the list. Is now a good time to get to work?"

def work_stop(bot, args, msg, event):
    global work_vars
    global thread_lock
    
    thread_lock.acquire()                       # Lock acquire
    if event.user.name not in work_vars['working'] and event.user.name not in work_vars['pausing']:
        thread_lock.release()                   # Lock release
        return "You were not registered."
    dic = work_vars['working'] if event.user.name in work_vars['working'] else work_vars['pausing']
    del dic[event.user.name]
    thread_lock.release()                       # Lock release
    
    return "You have been removed from the list."

def work_pause(bot, args, msg, event):
    global work_vars
    global thread_lock
    
    return "NYI"

def work_unpause(bot, args, msg, event):
    global work_vars
    global thread_lock
    
    return "NYI"

def work_plugin_start(bot, args, msg, event):
    global work_vars
    global thread_lock
    
    thread_lock.acquire()                       # Lock acquire
    if not work_vars['bot']:
        work_vars['bot'] = bot
    
    if work_vars['running']:
        thread_lock.release()                   # Lock release
        return "Work-Plugin already running."
    
    work_vars['thread'] = bot.room.watch_socket(on_event_work)
    work_vars['running'] = True
    thread_lock.release()                       # Lock release
    
    return "Work-Plugin started. Use *start* to subscribe to the plugin."

def work_plugin_stop(bot, args, msg, event):
    global work_vars
    global thread_lock
    
    thread_lock.acquire()                       # Lock acquire
    if not work_vars['running']:
        thread_lock.release()                   # Lock release
        return "Work-Plugin not running."
    
    work_vars['running']= False
    work_vars['thread'].close()
    work_vars['thread'] = None
    work_vars['working'].clear()
    work_vars['pausing'].clear()
    thread_lock.release()                       # Lock release
    
    return "Work-Plugin successfully stopped."

def work_plugin_status(bot, args, msg, event):
    global work_vars
    global thread_lock
    
    thread_lock.acquire()                       # Lock acquire
    status = work_vars['running']
    thread_lock.release()                       # Lock release
    
    if status:
        return "The work-plugin is currently running."
    else:
        return "The work-plugin is currently not running."

#---------------------------------------------

def on_event_work(event, client):
    global work_vars
    global thread_lock
    
    if not (isinstance(event, MessagePosted) or isinstance(event, MessageEdited)):
        return
    
    if event.user.name in work_vars['working']:
        thread_lock.acquire()                   # Lock acquire
        should_warn = work_vars['working'][event.user.name].update()
        
        if should_warn:
            work_vars['bot'].room.send_message("@{0} enough chatting, time to get back to work.".format(event.user.name))
        thread_lock.release()                   # Lock release

commands = [
    Command('work', command_work, 'Use *{0} start* and *{0} stop* to join Karma, *{0} pause* / *{0} unpause* to take a break, *{0} plugin start* / *{0} plugin stop* to control the plugin and *{0} status* to get the current status of the plugin.'.format("work"), False, False, None, None)
]

module_name = "work"