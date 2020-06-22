# ---------------------------------------------------------------------------------------------------------------
# Description: Cog that creates a task the sends "!d bump" every 120 minutes (for use with the disboard bot)
# ---------------------------------------------------------------------------------------------------------------

import discord
from discord.ext import commands, tasks

# ID of test channel: 596080666169442361

class BumpLoop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.change_status.start()

    @tasks.loop(minutes=15.0, reconnect=True) # Can change loop interval in future
    async def change_status(self):
        presences = [discord.Activity(type=discord.ActivityType.listening, name=f"Use {self.bot.config.BOT_PREFIX}help | {len(self.bot.users)} Users"),
                    discord.Activity(type=discord.ActivityType.watching, name=f"The Iron Legion | {len(self.bot.guilds)} Servers"),
                    discord.Activity(type=discord.ActivityType.watching, name="your every move..."),
                    discord.Activity(type=discord.ActivityType.playing, name="The CyberTruck isn't ugly")
                    ]

        await self.bot.change_presence(activity=random.choice(presences))

    @change_status.before_loop
    async def before_change_status(self):
        await self.bot.wait_until_ready()

    #@change_status.after_loop
    #async def after_change_status(self):
    #    await self.bot.change_status()

def setup(bot):
    bot.add_cog(BumpLoop(bot))