# ------------------------------------------------------------------------
# Mod Cog for JARVIS Bot (future home of purge, kick and ban commands)
# ------------------------------------------------------------------------

import config
import asyncio
import discord
from discord.ext import commands

class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True) # Need to test using cmd with canary to see outcome
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, cap: int):
        if cap == 0:
            embed = discord.Embed(color=0xd80000) # Change colour to red
            embed.set_author(name='J.A.R.V.I.S. Bot', url=config.BOT_URL, icon_url=self.bot.user.avatar_url)
            embed.add_field(name='ERROR', value=f'You cannot delete 0 messages, nice try', inline=False)
            embed.set_footer(text=config.BOT_FOOTER)
            await ctx.channel.send(embed=embed)
            return

        else:
            # Confirm purge (add emoji reaction functionality or a yes/no response)
            embed = discord.Embed(title='WARNING', color=0xd80000)
            embed.set_author(name='J.A.R.V.I.S. Bot', url=config.BOT_URL, icon_url=self.bot.user.avatar_url)
            embed.add_field(name='Purge Confirmation', value=f'Please confirm (yes/no) that you want to clear ``{cap}`` message(s)', inline=False)
            embed.set_footer(text=config.BOT_FOOTER)
            confirm = await ctx.channel.send(embed=embed)

            #await ctx.send(f"DEBUG: {cap}")

        embed = discord.Embed(title='WARNING', color=0xd80000)
        embed.set_author(name='J.A.R.V.I.S. Bot', url=config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.add_field(name='Purge In Progress', value=f'Clearing ``{cap}`` message(s)...', inline=False)
        embed.set_footer(text=config.BOT_FOOTER)
        tmp = await ctx.channel.send(embed=embed)

        await confirm.delete()        
        deleted = await ctx.channel.purge(limit=cap, before=ctx.message)

        complete = discord.Embed(title='SUCCESS', color=0x1414ff)
        complete.set_author(name='J.A.R.V.I.S. Bot', url=config.BOT_URL, icon_url=self.bot.user.avatar_url)
        complete.add_field(name='Purge Complete', value=f'Successfully purged ``{len(deleted)}`` message(s)', inline=False)
        complete.set_footer(text=config.BOT_FOOTER)
        await tmp.edit(embed=complete)

        await asyncio.sleep(6)
        await ctx.message.delete()
        await tmp.delete()

    @commands.command()
    async def thumb(self, ctx):
        txtCHK = await ctx.send('Send me that confirmation mate')

        def check(m):
            return m.content == "yes" or "no"

        try:
            msg = await self.bot.wait_for('message', timeout=10.0, check=check)
        
            print(msg.content)

            if msg.content.lower() == "yes":
                await ctx.send("Purging...")

            else:
                await ctx.send("Action Cancelled")

        except asyncio.TimeoutError:
            to = await ctx.send("timed out")
        
        await asyncio.sleep(6)
        await msg.delete()
        await txtCHK.delete()

    @commands.command()
    async def thumbb(self, ctx):        
        emojiCHK = await ctx.send('Send me that emoji mate') # Need to experiment more
        emoji = "👍"
        await emojiCHK.add_reaction(emoji)

        def check(m):
            return str(m.reaction.emoji) == "👍"# or "❌"

        try:
            reaction = await self.bot.wait_for('add_reaction', timeout=10.0, check=check)
        
            #print(str(reaction.emoji))

            if reaction.emoji == "👍":
                await ctx.send("Purging...")

            else:
                await ctx.send("Action Cancelled")

        except asyncio.TimeoutError:
            to = await ctx.send("timed out")
        
        await asyncio.sleep(6)
        await emojiCHK.delete()
        await to.delete()


        # Need to figure out how to react to this previous message

        # Need to figure out how to check member's that have reacted

        # Need if statement, if clicked check mark... else send timeout message

        

    # Need to take int input
    # Add a confirmation screen with capital/bolded letters, red embed colour, etc.
    # --> user will react to either :white_check_mark: or :x: (need to be able to check that the original author reacted and not a rando)
    # --> add a 60 second time out (send cancelled message once this limit is reached)
    # --> if cancelled, send message saying purge cancelledl; delete this message after 4 seconds
    # Need to delete inputed number of messages
    # --> With a 1 second delay (will need to test with dyno and adjust accordingly)
    # --> After complete, send a success message (successfully deleted 33 messages!)
    # --> Delete this message after 4 seconds

#def setup(bot):
#    bot.add_cog(ModCog(bot))