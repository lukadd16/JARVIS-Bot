# ------------------------------------------------------------------------------------------------
# Description: Cog that houses owner only commands (cog related commmands inspired from EvieePy)
# ------------------------------------------------------------------------------------------------

import asyncio
import copy # Found from ModMail, does what its name implies, it copies a an object unlike an assignment statement which only points to the other variable
import discord
import io
import textwrap
import time
import traceback

from contextlib import redirect_stdout # From ModMail, not sure exactly its purpose
from datetime import datetime
from discord.ext import commands
from importlib import reload as importlib_reload # Taken from ModMail Source Code, allows a previously imported *module* to be reloaded (like cogs) without having to restart the bot
from myutils import botUtils
from typing import Optional # Found from ModMail, allows for an optional arg in a function w/o having to put it at the end of all the other args

# From ModMail, for use in the eval command
def cleanup_code(content):
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:-1])
        return content.strip("` \n")

class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command(aliases=["load", "loadcog"])
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

    @commands.command(aliases=["unload", "unloadcog"])
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

    @commands.command(aliases=["reload", "reloadcog"])
    @commands.is_owner()
    async def bog_reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            self.bot.reload_extension(cog)

        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command()
    @commands.is_owner()
    async def reloadconf(self, ctx):
        # Reloads config file w/o needing terminate the bot (finally!)
        try:
            importlib_reload(self.bot.config)
        except Exception as e:
            await ctx.send(f'**`ERROR`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(aliases=["reload_all"])
    @commands.is_owner()
    async def bog_reload_all(self, ctx):
        try:
            for extension in self.bot.config.BOT_EXTENSIONS:
                self.bot.reload_extension(extension)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')
    
    @commands.command()
    @commands.is_owner()
    async def invoke(self, ctx, channel: Optional[discord.TextChannel], user: discord.User, *, command: str):
        # Taken from ModMail Source, invoke a command as another user (and optionally in another channel)
        msg = copy.copy(ctx.message)
        channel = channel or ctx.channel # Take user inputted channel first, if not found then default to the current channel
        msg.channel = channel
        msg.author = channel.guild.get_member(user.id) or user
        msg.content = ctx.prefix + command
        new_ctx = await self.bot.get_context(msg, cls=type(ctx))
        await self.bot.invoke(new_ctx)

    @commands.command(aliases=['eval'], enabled=False)
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        # Taken from ModMail Source, evaluates code inputted from within the discord client (it would be a good idea to look this over and try to understand what each part does)
        
        # For some reason it causes the bot to shutdown after reacting to the message
        env = {
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "_": self._last_result,
        }
        env.update(globals())
        body = cleanup_code(body)
        stdout = io.StringIO()
        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
        try:
            exec(to_compile, env)
        
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"```py\n{e.__class__.__name__}: {e}\n```", colour=self.bot.primary_colour,))
        func = env["func"]
        
        try:
            with redirect_stdout(stdout):
                ret = await func()
        
        except Exception:
            value = stdout.getvalue()
            await ctx.send(embed=discord.Embed(description=f"```py\n{value}{traceback.format_exc()}\n```", colour=self.bot.error_colour,))
        
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction("✅")
            
            except discord.Forbidden:
                pass
            
            if ret is None:
                if value:
                    await ctx.send(embed=discord.Embed(descrption=f"```py\n{value}\n```", colour=self.bot.primary_colour))
            
            else:
                self._last_result = ret
                await ctx.send(embed=discord.Embed(description=f"```py\n{value}{ret}\n```", colour=self.bot.primary_colour))

    @commands.command(enabled=False)
    @commands.is_owner()
    async def restart(self, ctx):
        # Doesn't work because of the error that keeps being thrown upon shutdown (about the background task) that I've been ignoring

        await ctx.send("Restarting...")
        await self.bot.logout() # Is reconnection logic needed? Or will my loop in main.py take over at this point? Need to test
        await self.bot.login(self.bot.config.BOT_TOKEN)
        await self.bot.connect()
        
        # This isn't gonna do what I want it to do, won't refresh cogs or config, etc.

    @commands.command(aliases=["kill", "terminate"])
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down...")
        await self.bot.status_channel.send(f"`{self.bot.user}` has been disconnected")
        # Very hacky way of doing it but it'll do for now
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        delta_uptime_seconds = delta_uptime.total_seconds()
        
        #hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        #minutes, seconds = divmod(remainder, 60)
        # days, hours = divmod(hours, 24)
        await self.bot.status_channel.send(f"Total Uptime was: `{botUtils.convert_seconds_friendly(delta_uptime_seconds)}`") # `{days}d, {hours}h, {minutes}m, {seconds}s`")
        print(f"\n[BT] Disconnected Gracefully")
        await self.bot.logout()

    # Add other cool owner commands from ModMail Source

    # If and when DB is added, manual SQL execution command can be put here

def setup(bot):
    bot.add_cog(OwnerCog(bot))