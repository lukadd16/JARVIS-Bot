# ----------------------------------------------------------------------------------------------
# Description: Cog that creates a task which switches the bot's status every X minutes
# ----------------------------------------------------------------------------------------------

# Rename to events, and re-do change_status event such that the status' are displayed in order (can't remember which modmail bot src had that implementation)

import asyncio
import discord
import random
import logging

from discord.ext import commands, tasks

class StatusLoop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.presence_index = 0 # For use in the counted loop
        self.presence_updater.start() # Ignore the error, it works

    async def set_presence(self):
        presences = [discord.Activity(type=discord.ActivityType.listening, name=f"Use {self.bot.config.BOT_PREFIX}help | {len(self.bot.users)} Users"),
            discord.Activity(type=discord.ActivityType.watching, name=f"The Iron Legion | {len(self.bot.guilds)} Servers"),
            discord.Activity(type=discord.ActivityType.playing, name="Plague Inc."),
            discord.Activity(type=discord.ActivityType.playing, name="Moving to Antarctica because of coronavirus")
            ]
        self.bot.logger.debug("Changing Bot Presence")
        #self.bot.logger.debug(len(presences))

        if self.presence_index == (len(presences) - 1):
            self.presence_index = 0
            self.bot.logger.debug("Resetting counter") # Never reaches this
        else:
            self.presence_index += 1
            #self.bot.logger.debug(self.presence_index)

        await self.bot.change_presence(activity=presences[self.presence_index])

    @tasks.loop(seconds=15, reconnect=True) # Change sleep times when publishing code
    async def presence_updater(self):
        self.bot.logger.debug("Switching to next presence.")
        await self.set_presence()

    @presence_updater.before_loop
    async def before_loop_presence(self):
        await self.bot.wait_until_ready()

        #await self.set_presence()

        await asyncio.sleep(15)
        self.bot.logger.info("Starting presence loop.")

    # Could potentially get rid of this entire cog and replace it with an events cog (for updating bot's stats to listing sites maybe?)
    # async def activity_updater(self):
    #     await self.bot.wait_until_ready()
    #     while True:
    #         if self.activity_index + 1 >= len(self.bot.config.activity):
    #             self.activity_index = 0
    #         else:
    #             self.activity_index = self.activity_index + 1
    #         await self.bot.change_presence(activity=discord.Game(name=self.bot.config.activity[self.activity_index]))
    #         await asyncio.sleep(12)

    #def cog_unload(self):
    #    self.bot.change_status.cancel()

    #@change_status.before_loop
    #async def before_change_status(self):
    #    await self.bot.wait_until_ready()

    #@change_status.after_loop
    #async def after_change_status(self):
    #    await self.bot.change_status()

def setup(bot):
    bot.add_cog(StatusLoop(bot))