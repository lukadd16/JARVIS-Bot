# -----------------------------------------------------------------------------------------------
# Description: Error Handler forked from internet (creds to MrBot)
# -----------------------------------------------------------------------------------------------

import traceback
import sys
from discord.ext import commands
import discord

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # If the command has a local error handler, return
        if hasattr(ctx.command, "on_error"):
            return

        # Get the original exception or or if nothing is found keep the exception
        error = getattr(error, "original", error)

        # Check for errors
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"You missed the `{error.param}` parameter. Use `{ctx.prefix}help` for more information on how to use this command.")
        
        if isinstance(error, commands.TooManyArguments):
            return await ctx.send(f"You passed too many arguments to the command `{ctx.command}`. Use `{ctx.prefix}help` for more information on how to use this command.")
        
        if isinstance(error, commands.BadArgument):
            return await ctx.send(f"You passed a bad argument to the command `{ctx.command}`.")
        
        if isinstance(error, commands.CommandNotFound):
            return
        
        if isinstance(error, commands.PrivateMessageOnly):
            return await ctx.send(f"The command `{ctx.command}` can only be used in DM's.")
        
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send(f"The command `{ctx.command}` can not be used in DM's.")
            except discord.Forbidden:
                return
        
        if isinstance(error, commands.NotOwner):
            return await ctx.send(f"The command `{ctx.command}` is owner only.")
        
        if isinstance(error, commands.MissingPermissions):
            missing_perms = ""
            for perm in error.missing_perms:
                missing_perms += f"\n> {perm}"
            return await ctx.send(f"You don't have the following permissions required to run the command `{ctx.command}`.\n{missing_perms}")
        
        if isinstance(error, commands.BotMissingPermissions):
            missing_perms = ""
            for perm in error.missing_perms:
                missing_perms += f"\n> {perm}"
            return await ctx.send(f"I am missing the following permissions to run the command `{ctx.command}`.\n{missing_perms}")
        
        if isinstance(error, commands.DisabledCommand):
            return await ctx.send(f"The command `{ctx.command}` is currently disabled.")
        
        # if isinstance(error, commands.CommandOnCooldown):
        #     if error.cooldown.type == commands.BucketType.user:
        #         return await ctx.send(f"The command `{ctx.command}` is on cooldown for you, retry in `{formatting.get_time_friendly(error.retry_after)}`.")
        #     if error.cooldown.type == commands.BucketType.default:
        #         return await ctx.send(f"The command `{ctx.command}` is on cooldown for the whole bot, retry in `{formatting.get_time_friendly(error.retry_after)}`.")
        #     if error.cooldown.type == commands.BucketType.guild:
        #         return await ctx.send(f"The command `{ctx.command}` is on cooldown for this guild, retry in `{formatting.get_time_friendly(error.retry_after)}`.")

        # Print the error and traceback if it doesnt match any of the above.
        print(f"\n[BT] Ignoring exception in command {ctx.command}:")
        traceback.print_exception(type(error), error, error.__traceback__)

    # An example of command specific errors
    # ---
    # @commands.command(name='repeat', aliases=['mimic', 'copy']) # Use the following as templates
    # async def do_repeat(self, ctx, *, inp: str):
    #     await ctx.send(inp)

    # @do_repeat.error
    # async def do_repeat_handler(self, ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         if error.param.name == 'inp':
    #             await ctx.send("You forgot to give me input to repeat!")
      
def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))