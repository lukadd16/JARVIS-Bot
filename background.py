# ----------------------------------------------------------------------------------------------
# Description: Cog that creates a task which switches the bot's status every X minutes
# ----------------------------------------------------------------------------------------------

import discord
from discord.ext import commands, tasks
import random

class StatusLoop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.change_status.start()

    @tasks.loop(minutes=15.0, reconnect=True) # Can change loop interval in future
    async def change_status(self):
        presences = [discord.Activity(type=discord.ActivityType.listening, name=f"Use {self.bot.config.BOT_PREFIX}help | {len(self.bot.users)} Users"),
                    discord.Activity(type=discord.ActivityType.watching, name=f"The Iron Legion | {len(self.bot.guilds)} Servers"),
                    discord.Activity(type=discord.ActivityType.watching, name="your every move..."),
                    discord.Activity(type=discord.ActivityType.watching, name="Roman commit war crimes")
                    ]

        await self.bot.change_presence(activity=random.choice(presences))

    @change_status.before_loop
    async def before_change_status(self):
        await self.bot.wait_until_ready()

    #@change_status.after_loop
    #async def after_change_status(self):
    #    await self.bot.change_status()

def setup(bot):
    bot.add_cog(StatusLoop(bot))