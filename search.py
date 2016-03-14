from Module import Command
import re
import requests
import json

# Configuration
save_subdir = 'say'

def command_search(cmd,bot,args,msg,event):
    
    ddg_api = "https://api.duckduckgo.com/?q="
    format_style = "&format=json"
    search_term = "+".join(args)
    
    url = ddg_api + search_term + format_style
    resp = requests.get(url)
    
    message = " Powered by https://api.duckduckgo.com/api\n"
    
    if resp.status_code == 200:
        data = json.loads(resp.text)
        if data["Abstract"] == '':
            if len(data["RelatedTopics"]) == 0:
                return "Sorry, I did not find any answer for that request. You could consider to try manually: https://duckduckgo.com/?q=" + search_term 
            else:
                message += data["RelatedTopics"][0]["Text"] + " " + data["RelatedTopics"][0]["FirstURL"]
        else:
            message += data["Abstract"] + " \n[Source:"+data["AbstractSource"]+" ] "+data["AbstractURL"]
    else:
        return "Error connecting to the duck"
    return message

commands = [
    Command('search', command_search, 'Search the web via DDG.', False, False, None, None),
]

module_name = "search"
