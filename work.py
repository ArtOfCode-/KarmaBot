from Module import Command
import threading
import time
from ChatExchange6.chatexchange6.events import MessagePosted, MessageEdited
from ChatExchange6.chatexchange6.messages import Message

#---------------------------------------------
grace_time  = 5*60
time_period = 60*60
max_msgs    = 14
min_msgs    = 5
max_in_time_period = 7
max_in_half_time = 4

class User:
    def __init__(self, name):
        self.name = name
        self.reset()
        
    def reset(self):
        self.one_hour = 0
        self.heuristic_start = time.time()
        self.last_action = time.time()
        self.count = []
    
    def update(self):
        #global same_action_delay
        #global warning_time
        global grace_time
        global time_period
        global max_msgs
        global min_msgs
        global max_in_time_period
        global max_in_half_time
        
        # Get current time
        current = time.time()
        
        # Orig
        #if (current - self.last_action) > same_action_delay:
        #    self.heuristic_start = current
        #
        #self.last_action = current
        #
        #should_warn = (self.last_action - self.heuristic_start) > warning_time
        #
        #if should_warn:
        #    self.heuristic_start = self.last_action
        
        # New
        #should_warn = (current - self.heuristic_start) > warning_time and (current - self.last_action) < same_action_delay
        #
        #if should_warn:
        #    self.heuristic_start = current
        #
        #return should_warn
        
        # We allow a grace time after starting the timer
        if current-self.heuristic_start < grace_time:
            return False
            
        # Add it to the list of actions    
        self.count.append(current)
        
        # Way too much chatting to be working
        if len(self.count) > max_msgs:
            self.reset()
            return True
            
        # Keep only the last 60 minutes
        at_least_an_hour = False
        n_msg = len(self.count)
        for n in range(n_msg):
            if current-self.count[0]>time_period:
                del self.count[0]
                at_least_an_hour = True
                
        # If an hour passed and only few messages were written, we restart it
        if len(self.count) < min_msgs and current-self.heuristic_start>time_period+grace_time:
            sum_worked = self.one_hour + current-self.heuristic_start
            self.reset()
            self.one_hour = sum_worked
            return False
            
        # Too active in the first 30 minutes
        if len(self.count)>max_in_half_time and current-self.heuristic_start<0.5*time_period:
            self.reset()
            return True
            
        # Too active within one hour
        if len(self.count)>max_in_time_period:
            self.reset()
            return True
            
        return False
    
    def status(self):
        time_in_min = int((time.time()-self.heuristic_start)/60.0) 
        hour_passed = int(self.one_hour/60.0)
        counts = len(self.count)
        
        if hour_passed == 0:
            if time_in_min<grace_time/60.0:
                return ", you should now start working."
            else:
                if counts < 2:
                    return "Dear {0}, you are supposed to be working since {1} minutes.".format(self.name,time_in_min)
                else:
                    return "Dear {0}, you are supposed to be working since {1} minutes. And I have counted {2} messages already.".format(self.name,time_in_min,counts)
        else:
            return ", you have been working since {0} minutes. Don't lose the momentum. You now stand at {1} counts.".format(time_in_min+hour_passed,counts)
        
            
#---------------------------------------------

thread_lock = threading.Lock()
#same_action_delay = 5*60            # MAGIC NUMBER Time between two actions to belong together. Should be high enough to account for typing.
#warning_time =      6*60           # MAGIC NUMBER If user is chatting longer than this Karma issues a warning
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
        return "I need arguments! Use *help work*"
    
    if args[0] == "start":
        return work_start(bot, args, msg, event)
    
    if args[0] == "stop":
        return work_stop(bot, args, msg, event)
    
    if args[0] == "pause":
        return work_pause(bot, args, msg, event)
    
    if args[0] == "unpause":
        return work_start(bot, args, msg, event)
    
    if args[0] == "status":
        return work_status(bot, args, msg, event)
        
    if args[0] == "list":
        return work_list(bot, args, msg, event)
   
    if len(args) >= 2:
        if args[0] == "plugin":
            if args[1] == "start":
                return work_plugin_start(bot, args, msg, event)
            if args[1] == "stop":
                return work_plugin_stop(bot, args, msg, event)
            if args[1] == "status":
                return work_plugin_status(bot, args, msg, event)
     
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
    
    return "has been added to the list. Now, get to work..."

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
    
def work_status(bot, args, msg, event):
    global work_vars
    global thread_lock
    
    thread_lock.acquire()
    if event.user.name not in work_vars['working']:
        thread_lock.release()
        return "Were you supposed to be working? You did not tell me!"
    message = work_vars['working'][event.user.name].status()
    thread_lock.release()
    return message+" But shouldn't you be working instead of asking me?"
    
def work_list(bot, args, msg, event):
    global work_vars
    global thread_lock
    
    message = "If you see the following users, remind them that they ought to be working: "
    for user in work_vars['working']:
        message += user+", "
    return message

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
    Command('work', command_work, 'Use *{0} start* and *{0} stop* to join Karma, *{0} pause* / *{0} unpause* to take a break, *{0} status* to know where you stand. *{0} plugin start* / *{0} plugin stop* to control the plugin and *{0} plugin status* to get the current status of the plugin.'.format("work"), False, False, None, None)
]

module_name = "work"