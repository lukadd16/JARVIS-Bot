# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# Filename: main.py
# Author: Lukadd.16#8870
# Purpose: Personal Discord Bot Project
# Changelog: V1.0: - Very basic bot functions (implemented from online code)
#            V1.01 - Fixed unresponsive commands
#            V1.02 - Re-installed discord.py with rewrite version (reworked commands again)
#            V1.03 - Added shutdown and uptime command
#            V1.04 - Added version command
#            V1.05 - Added help command (Released to RHBC server)
#            V1.06 - Added new dice command (uses NdN format)
#            ------------FORGOT TO UPDATE UNTIL THIS POINT--------------------------------------------------------------------------------------------------------------------------------------
#            V1.4 - Added jishaku
#            V1.41 - Added a background loop that continually updates the bot's status
#            V1.41a - Removed Jishaku functionality, started new BETA branch in the code which will contain new features
#            V1.5a - Cleaned up help command (completely restructured it, removed ironman command), added proper bot thumbnail
#                    to botinfo command, added user avatar as thumbnail in userinfo command, created variable for future bot invite link
#            V1.6a - Completely reworked ping command (also added websocket latency, with potential for database ping in future)
#                    Merged bot uptime with botinfo command and removed repeater command (which was long overdue)
#            V1.6b - Lots of code optimizations, introduced global error handling
#            V1.6c - Lots of code optimizations, released global error handler, finally added the ability to use
#                    userinfo cmd without having to ping self, new purge command
#            V1.61 - Very minor update, added aliases to popular commands and also to owner commands
#                    (which ended up killing the bot's 50 day uptime streak), changed permission requirements for purge command (later reverted)
#            V1.62 (not released) - New avatar command, reworked userinfo command, added multiple safeties to purge command, killed some notable bugs (purge one with multiple users),
#                    added new variables in config file
#            V1.6d - (FUTURE VERSION: hope to release moderation commands in this version; kick and ban + two-tier perm system using roles - introduce mod logging once db connected)
#            New Version Naming Scheme??? (would probably roll back to 0.6 and then plan what I want to get done with each version, with V1.0 being the end goal/final item)
#            Only add letters after version #s for quick hotfixes (i.e. "noticed an issue with purge command that allowed people to input -ve #s, pushed a quick fix in V.1.61a")
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Immediate To-Do:
#        - Update this list with items from Google Keep list
#        - Start work on a serverinfo command
#        - Start thinking about kick/ban commands and new perm system with roles
#        - Start framework for logging (first log bulk deletes)
#        - Entire restructuring of help command?
#        - Make each command response an embed when I see fit
#        - Convert each error message in both commands and global error handler to embeds (try to copy the purge cmd format)
#
# Less Important To-Do
#        - Create a RPS game for fun category
#        - Create a "create invite" command that takes input for length/limit of desired invite and outputs said link
#        - Mod/Admin commands
#        - Add server settings
#        - Add configurable member join messages (candidate for future database dependent, server specific feature/module disabling/enabling)
#        - [Meh]Implement a method of logging all errors, with the format of: Command Invoked, Whole Error String
#          (could be to a txt file, to a dedicated channel, etc.)
#
# DB To-Do:
#        - Learn PostgreSQL
#        - Create some proof-of-concept command first that just store basic data like userid or something
#        - Plan out how the table will look for an economy
#        - Need to figure out how to intialize bank accounts for users without forcing them to run a command
#          (need to initialize when added to a new server or when coming back online and detected new members)
#        - Planned Commands: balance, add-money, remove-money, give-money/pay, XX
# ----------------------------------------------------------------------------------------------

import asyncio
import config
import discord
import logging
import os
import random
import time

from discord.ext import commands, tasks
from datetime import datetime

# Every time that I make a change here (unless it involves the config file), immediately copy it over to the public branch which is
# where all server file updates will originate from in the future

# Legend:
# BT = Bot status message
# DB = Database status messages
# DEBUG = Detailed information, typically of interest only when diagnosing problems.
# INFO = Confirmation that things are working as expected.
# WARNING = An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
# ERROR = Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL = A serious error, indicating that the program itself may be unable to continue running.

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

# BOT IS NOW FUNCTIONAL AND LOGGING WORKS, FIND A WAY TO EITHER ADD ONTO EXISTING LOG FILES (not overwrite), CREATE A NEW FILE WITH EACH BOOT UP (with maybe a unique name like the date, etc.)

# Decide on setting logger mode to append or to just make backups of logs until a certain limit is reached and then delete the oldest log

# Research what exc_info is

class JARVIS(commands.Bot):
    def __init__(self):
        super().__init__(
        command_prefix=commands.when_mentioned_or(config.BOT_PREFIX),
        help_command=None,
        reconnect=True
        )

        self.config = config
        self.status_channel = None
        self.log_channel = None
        self.log_file_name = None
        self.launch_time = datetime.utcnow()
        self.cmdcount = 0
        self.guild_count = None # I think this line is obsolete now
        self.bot_status = None
        self.db_ready = False
        self.db = None # May or may not need this for SQL database, will need to figure out how to set db to be global here

        # Add db_connect() method call here
        self.bot_startup()

    def bot_startup(self):
        self.log_file_name = os.path.join(log_dir, f"JB_Primary.log") # Name ends up being NoneType because bot isn't logged in at this point, so either set the name to something static or more logger setup till after boot (somehow)

        level_text = self.config.LOG_LEVEL.upper()
        logging_levels = {
            "CRITICAL": logging.CRITICAL,
            "ERROR": logging.ERROR,
            "WARNING": logging.WARNING,
            "INFO": logging.INFO,
            "DEBUG": logging.DEBUG,
        }

        log_level = logging_levels.get(level_text)
        if log_level is None:
            log_level = logging.INFO
            level_text = "INFO"

        self.logger = logging.getLogger("JB.main")
        self.logger.setLevel(log_level)
        handler = logging.FileHandler(filename=f"{self.log_file_name}", encoding="utf-8", mode="a")
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s]: %(message)s"))
        self.logger.addHandler(handler)
        self.logger.debug("Sucessfully configured logging module with the following parameters.")
        self.logger.debug(f"Logging Level: {level_text}")
        self.logger.debug(f"File Name: {self.log_file_name}")

        # Load initial cogs defined in config file
        for extension in self.config.BOT_EXTENSIONS:
            try:
                self.load_extension(extension)
                print(f"[COG] SUCCESS - {extension}")

            except commands.ExtensionNotFound:
                print(f"[COG] FAILED - {extension}")

        #self.login(config.BOT_TOKEN)
        #self.connect()

    # Replace uptime calculator with botUtils one
    def bot_close(self):
        self.status_channel.send(f"`{self.user}` has been manually interrupted through keystroke")
        delta_uptime = datetime.utcnow() - self.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        self.status_channel.send(f"Total Uptime was: `{days}d, {hours}h, {minutes}m, {seconds}s`")
        print(f"\n[BT] Interrupt Shutdown Successful")
        self.logout()

    def run(self):
        try: 
            self.loop.run_until_complete(self.start(self.config.BOT_TOKEN)) #self.bot_startup()
        except KeyboardInterrupt:
            self.logger.critical("Keyboard Interrupt Detected")
        except discord.LoginFailure:
            self.logger.critical("Invalid Token")
        except Exception:
            self.logger.critical("Fatal Exception", exc_info=True)
            # Need to look up what exc_info does
        finally:
            # Insert other shutdown logic here (like the uptime calculator that will be moved to botUtils.py)
            self.logger.warning(" - Shutting down bot - ") # Is this really an error?
            self.loop.run_until_complete(self.logout())

            # for task in asyncio.all_tasks(self.loop):
            #     task.cancel()
            # try:
            #     self.loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(self.loop)))
            # except asyncio.CancelledError:
            #     logger.debug("All pending tasks has been cancelled.")
            # finally:
            #     self.loop.run_until_complete(self.session.close())
            #     logger.error(" - Shutting down bot - ")

    async def on_ready(self):
        # Fetch bot info (not sure if I still need to do this, will have to test)
        await self.application_info()

        # Set the logging and status channels
        self.status_channel = self.get_channel(self.config.STATUS_CHANNEL_ID)
        self.log_channel = self.get_channel(self.config.LOG_CHANNEL_ID)

        await self.status_channel.send(f"`{self.user}` has successfully connected to Discord")

        self.logger.info(" - ")
        self.logger.info("Client is ready.")
        self.logger.info(f"Logged in as {self.user.name} - ID: {self.user.id}")
        self.logger.info(f"Discord.py Version - {discord.__version__}")
        self.logger.info(f"Owner(s) - WIP")
        self.logger.info(f"Prefix - {self.config.BOT_PREFIX}")
        self.logger.info(" - ")

        print(f"\n[BT] Logged in as: {self.user.name} - {self.user.id}")
        print(f"[BT] Library Version: {discord.__version__}")

        print("\n[BT] I have access to the following guilds (as of bootup):")
        for guild in self.guilds:
            print(guild.name)
        
        # Default bot status
        self.bot_status = "The Iron Legion | " + str(len(self.guilds)) + "  Servers"    
        self.game = discord.Game(self.bot_status)
        await self.change_presence(status=discord.Status.online, activity=self.game)

        #self.reload_extension("cogs.background")
        #print("\n[BT] Manual flushing of status cog")

        # Connect to DB (refer to MrBot code)
        # try:
        # [Insert code here]

        # Insert database checks here for server configs (checks being to see if bot joined any new servers during downtime)
        # After checks complete, change db_ready to True
        # except: [Insert database connection failed error, exception as e]

    async def on_resume(self):
        await self.status_channel.send(f"`{self.user}'s` connection has been resumed.")
        print(f"\n[BT] Connection Resumed")

    async def on_disconnect(self):
        print(f"\n[BT] Disconnected")

    # Bot events that we respond to
    async def on_guild_join(self, guild):
        await self.log_channel.send(f"`{self.user}` has been added to `{guild}` with `{guild.member_count} members`")

    async def on_guild_remove(self, guild):
        await self.log_channel.send(f"`{self.user}` has been removed from `{guild}` :(")

JARVIS().run()