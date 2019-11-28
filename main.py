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
#            ------------FORGOT TO UPDATE UNTIL THIS POINT-----------------
#            V1.4 - Added jishaku
#            V1.41 - Added a background loop that continually updates the bot's status
#            V1.41a - Removed Jishaku functionality, started new BETA branch in the code which will contain new features
#            V1.5a - Cleaned up help command (completely restructured it, removed ironman command), added proper bot thumbnail
#                    to botinfo command, added user avatar as thumbnail in userinfo command, created variable for future bot invite link
#            V1.6a - Completely reworked ping command (also added websocket latency, with potential for database ping in future)
#                    Merged bot uptime with botinfo command and removed repeater command (which was long overdue)
#            V1.6b - Lots of code optimizations, introduced global error handling
#            V1.6c - Lots of code optimizations, released global error handler, finally added the ability to use userinfo cmd without having to ping self, new purge command
#            V1.61 - Very minor update, added aliases to popular commands and also to owner commands (which ended up killing the bot's 50 day uptime streak), also changed permission requirements for purge command
#            V1.6d - (FUTURE VERSION: hope to release moderation commands in this version; kick and ban + two-tier perm system using roles - introduce mod logging once db connected)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# Immediate To-Do:
#        - Update this list with items from Google Keep list
#        - Start work on a serverinfo command
#        - Start thinking about kick/ban commands and new perm system with roles
#        - *Continue to refine help command, decide if want to add blank space above "Fun" header and consider shrinking list entirely
#           and maybe adding help subcommands
#        - **Decide on what stats/info to add to userinfo command
#        - Make each command response an embed when I see fit
#        - Convert each error message in both commands and global error handler to embeds (try to copy the purge cmd format)
#        - Start thinking about market-specific commands and how I would go about making them

# Less Important To-Do
#        - Create a RPS game for fun category
#        - Implement a bot invite command (not sure if needed anymore as link is now attached to JARVIS name in embeds)
#        - Create a "create invite" command that takes input for length/limit of desired invite and outputs said link
#        - Mod/Admin commands
#        - Add server settings
#        - Add configurable member join messages (candidate for future database dependent, server specific feature/module disabling/enabling)
#        - [Meh]Implement a method of logging all errors, with the format of: Command Invoked, Whole Error String
#          (could be to a txt file, to a dedicated channel, etc.)
# ----------------------------------------------------------------------------------------------

# Import required modules
import time
import random
import os
import config
import discord
from discord.ext import commands
from datetime import datetime

class JARVIS(commands.Bot):
    
    def __init__(self):
        super().__init__(command_prefix=config.BOT_PREFIX, help_command=None, reconnect=True)

        self.config = config
        self.status_channel = None
        self.log_channel = None
        self.launch_time = datetime.utcnow()
        self.guild_count = None
        self.bot_status = None
        self.db_ready = False
        self.db = None # May or may not need this for SQL database, will need to figure out how to set db to be global here

        # Load cogs
        for extension in self.config.BOT_EXTENSIONS:
            try:
                self.load_extension(extension)
                print(f"[COG] SUCCESS - {extension}")

            except commands.ExtensionNotFound:
                print(f"[COG] FAILED - {extension}")

    async def bot_startup(self):
        await self.login(config.BOT_TOKEN)
        await self.connect()

    # Use in shutdown command
    # ...
    async def bot_close(self):
        await self.status_channel.send(f"`{self.user}` has been disconnected")
        # Very hacky way of doing it but it'll do for now
        delta_uptime = datetime.utcnow() - self.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await self.status_channel.send(f"Total Uptime was: `{days}d, {hours}h, {minutes}m, {seconds}s`")
        print(f"\n[BT] Disconnected Gracefully")
        await self.logout()

    def run(self):
        try: 
            self.loop.run_until_complete(self.bot_startup())

        except KeyboardInterrupt:
            self.loop.run_until_complete(self.bot_close())

    # In print functions BT refers to Bot status message, DB refers to Database status messages
    async def on_ready(self):
        # Fetch bot info (not sure if I still need to do this, will have to test)
        await self.application_info()

        # Set the logging and status channels
        self.status_channel = self.get_channel(self.config.STATUS_CHANNEL_ID)
        self.log_channel = self.get_channel(self.config.LOG_CHANNEL_ID)

        # Send a message mentioning that the bot is ready
        await self.status_channel.send(f"`{self.user}` has successfully connected to Discord")
        print(f"\n[BT] Logged in as: {self.user.name} - {self.user.id}")
        print(f"[BT] Library Version: {discord.__version__}")

        #self.guild_count = 0
        print("\n[BT] I have access to the following guilds:")
        for guild in self.guilds:
            #self.guild_count += 1
            print(guild.name)
        
        # Default bot status
        self.bot_status = "The Iron Legion | " + str(len(self.guilds)) + "  Servers"    
        self.game = discord.Game(self.bot_status)
        await self.change_presence(status=discord.Status.online, activity=self.game) # Figure out how to do watching, listening status'

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
        #await self.status_channel.send(f"`{self.user}` has been disconnected")
        print(f"\n[BT] Disconnected")

# get_channel() # retrieve channel for logging (future update)
# Setup different levels of logging (debugging, etc.) and print each to a .log file and into
# a pre-set channel
# Also try to setup (completely different) logging for server occurences (kick, ban, etc.)

JARVIS().run()