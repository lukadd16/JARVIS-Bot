# ------------------------------------------------------------------------
# Mod Cog for JARVIS Bot (future home of purge, kick and ban commands)
# ------------------------------------------------------------------------

import asyncio
import discord
from discord.ext import commands

class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["clear"])
    @commands.bot_has_permissions(manage_messages=True) # In future, will need to figure out if possible to preserve dyno logs by deleting messages slowly
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, cap: int):
        if cap == 0:
            embed = discord.Embed(color=0xd80000) # Change colour to red
            embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
            embed.add_field(name='ERROR', value=f'You cannot delete 0 messages, nice try', inline=False)
            embed.set_footer(text=self.bot.config.BOT_FOOTER)
            zeroerror = await ctx.channel.send(embed=embed)
            await asyncio.sleep(5)
            await ctx.message.delete()
            await zeroerror.delete() # Need to also delete ctx message
            return

        else:
            # Confirm purge (add emoji reaction functionality or a yes/no response)
            embed = discord.Embed(title='WARNING', color=0xd80000)
            embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
            embed.add_field(name='Purge Confirmation', value=f'Please confirm (yes/no) that you want to clear ``{cap}`` message(s)', inline=False)
            embed.set_footer(text=self.bot.config.BOT_FOOTER)
            confirm = await ctx.channel.send(embed=embed)

            def check(m):
                return m.content == "yes" or "no" and m.author == ctx.author

            try:
                msg = await self.bot.wait_for('message', timeout=20.0, check=check)

                if msg.content.lower() == "yes" and msg.author == ctx.author:
                    embed = discord.Embed(title='WARNING', color=0xd80000)
                    embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
                    embed.add_field(name='Purge In Progress', value=f'Clearing ``{cap}`` message(s)...', inline=False)
                    embed.set_footer(text=self.bot.config.BOT_FOOTER)
                    tmp = await ctx.channel.send(embed=embed)

                    await confirm.delete()        
                    await msg.delete()
                    await ctx.message.delete()
                    deleted = await ctx.channel.purge(limit=cap, before=ctx.message)
                    
                else:
                    embed = discord.Embed(title='WARNING', color=0xd80000)
                    embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
                    embed.add_field(name='Purge Cancelled', value=f'This action has been cancelled', inline=False)
                    embed.set_footer(text=self.bot.config.BOT_FOOTER)
                    await confirm.edit(embed=embed)

                    await ctx.message.delete()
                    await msg.delete()
                    await asyncio.sleep(5)
                    await confirm.delete()
                    return

            except asyncio.TimeoutError:
                embed = discord.Embed(title='WARNING', color=0xd80000)
                embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
                embed.add_field(name='Purge Cancelled', value=f'This action timed-out', inline=False)
                embed.set_footer(text=self.bot.config.BOT_FOOTER)
                await confirm.edit(embed=embed)

                await ctx.message.delete()
                await asyncio.sleep(10)
                await confirm.delete()
                return
     
        complete = discord.Embed(title='SUCCESS', color=0x1414ff)
        complete.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        complete.add_field(name='Purge Complete', value=f'Successfully purged ``{len(deleted)}`` message(s)', inline=False)
        complete.set_footer(text=self.bot.config.BOT_FOOTER)
        await tmp.edit(embed=complete)

        await asyncio.sleep(5)
        await tmp.delete()

def setup(bot):
    bot.add_cog(ModCog(bot))