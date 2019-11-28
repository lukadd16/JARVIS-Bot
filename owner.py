# ------------------------------------------------------------------------------------------------
# Description: Cog that houses owner only commands (cog related commmands inspired from EvieePy)
# ------------------------------------------------------------------------------------------------

import time
import discord
import asyncio
from discord.ext import commands
from datetime import datetime

class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def bog_load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command()
    @commands.is_owner()
    async def bog_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command()
    @commands.is_owner()
    async def bog_reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(aliases=["reload"])
    @commands.is_owner()
    async def bog_reload_all(self, ctx):
        try:
            for extension in self.bot.config.BOT_EXTENSIONS:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')
    
    @commands.command(aliases=["kill"])
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down...")
        await self.bot.status_channel.send(f"`{self.bot.user}` has been disconnected")
        # Very hacky way of doing it but it'll do for now
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await self.bot.status_channel.send(f"Total Uptime was: `{days}d, {hours}h, {minutes}m, {seconds}s`")
        print(f"\n[BT] Disconnected Gracefully")
        await self.bot.logout()


    # Temporarily disabled in order to test global error handler

    #@shutdown.error
    #async def shutdown_handler(self, ctx, error):
    #    if isinstance(error, commands.NotOwner):
    #        await ctx.send("Only my owner can issue this command!")

def setup(bot):
    bot.add_cog(OwnerCog(bot))
