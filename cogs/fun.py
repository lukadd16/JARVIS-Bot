# --------------------------------------------------------------------
# Description: Cog that houses fun & games commands for JARVIS Bot
# --------------------------------------------------------------------

# THIS COG IS CURRENTLY DISABLED (not loaded during initial bootup)
# Try to find cool, fun commands from internet, come up with own ideas or even combine own ideas with online code

import random
import asyncio
import discord
from discord.ext import commands

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Better dice roll example from online docs
    @commands.command()
    async def roll(self, ctx, dice: str): # Add proper local error handler for missing dice arg or incorrectly inputted dice arg
        try:
            rolls, limit = map(int, dice.split('d'))

        except Exception:
            await ctx.send('Format has to be in NdN!')
            return
        
        if rolls > 100 or limit > 100:
            await ctx.send("What you are asking is beyond my current computational abilities (i.e. going any higher will most likely cause me to crash)")

        else:
            result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
            await ctx.send(result)

    # Chooses randomly between multiple things
    @commands.command()
    async def choose(self, ctx, *choices: str):
        message = await ctx.send("I prefer...")

        botchoice = random.choice(choices)

        await message.edit(content=f"I prefer {botchoice}")

    # Repeats user message multiple times
    # DISABLED COMMAND, BUT WILL KEEP IN FILE FOR FUTURE REFERENCE

    # @commands.command()
    # async def repeater(self, ctx, times: int, *, content):
    #     if times > 50:
    #         await ctx.send("What you are asking will disturb others, I cannot let you do that")

    #     else:
    #         for i in range(times):
    #             await ctx.send(content)

    @commands.command() # Create a command that can search up info about any Iron Man Armour (from MCU)
    async def ironman(self, ctx):
        pass

    @commands.command()
    async def ball(self, ctx):
     await ctx.send(random.choice(["You are doomed...", "You will succeed", "test", "XD", "why"]))

def setup(bot):
    bot.add_cog(FunCog(bot))
