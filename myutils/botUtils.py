import discord
import os
import random
import time
import config
from datetime import datetime

# Put repeatedly used lines of code here, such as uptime calculation, ping calc, determining user status and returning the appropriate emoji, future guild tasks, etc.

# Used in error_handler cooldown, make it able to function with ping, uptime, about and shutdown commands/actions
def convert_seconds_friendly(second):
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    days = round(day)
    hours = round(hour)
    minutes = round(minute)
    seconds = round(second)
    if minutes == 0:
        return "%02ds" % (seconds)
    if hours == 0:
        return "%02dm %02ds" % (minutes, seconds)
    if days == 0:
        return "%02dh %02dm %02ds" % (hours, minutes, seconds)
    return "%02dd %02dh %02dm %02ds" % (days, hours, minutes, seconds)

def convert_time_friendly(datetime):
    pass
#def get_time_friendly(): # In weeks format for whois and serverinfo, maybe rename it to something else
#    pass

def get_member_status(member):
    if f'{member.status}'.lower() == "online":
        return f'{config.BOT_EMOJI_ONLINE}'
    elif f'{member.status}'.lower() == "idle":
        return f'{config.BOT_EMOJI_IDLE}'
    elif f'{member.status}'.lower() == "dnd":
        return f'{config.BOT_EMOJI_DND}'
    elif f'{member.status}'.lower() == "offline":
        return f'{config.BOT_EMOJI_OFFLINE}'
    else:
        return f'{config.BOT_EMOJI_STREAM}'

def bot_check(member):
    if member.bot is True:
        return f' {config.BOT_EMOJI_BTAG}'
    else:
        return ''