# ------------------------------------------------------------------
# Description: Cog that houses utilities commands for JARVIS Bot
# ------------------------------------------------------------------

import time
import sys
import discord
from discord.ext import commands
from datetime import datetime

class UtilitiesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        # Start timer used for latency calculation
        start = time.perf_counter()

        embed = discord.Embed(color=0xd89e47)
        embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Ping...", value='Message Round Trip: \nDiscord Websocket: ')
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        message = await ctx.channel.send(embed=embed)

        # Calculate round trip and websocket latency
        end = time.perf_counter()
        duration = (end - start) * 1000
        weblatency = self.bot.latency * 1000

        embed = discord.Embed(color=0xd89e47)
        embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Pong!", value='Message Round Trip: ``{:.2f}ms``\nDiscord Websocket: ``{:.2f}ms``'.format(duration, weblatency))
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await message.edit(embed=embed)

    @commands.command()
    async def version(self, ctx):
        embed = discord.Embed(color=0xd89e47)
        embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Current Stable Version", value=self.bot.config.BOT_VERSION, inline=False)
        embed.add_field(name="Current BETA Version", value=self.bot.config.BOT_BETAVERSION, inline=False)
        embed.add_field(name="New Features/Fixes with this Version", value=self.bot.config.BOT_FEATURES, inline=False)
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send("I have been online for " f"{days}d, {hours}h, {minutes}m, {seconds}s, Sir")

    @commands.command(aliases=["about", "binfo"])
    async def botinfo(self, ctx):
        # Get version info for library and python runtime
        d_version = discord.__version__
        p_version = sys.version[0:6]

        # Get bots' total uptime
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        embed = discord.Embed(title='Information about J.A.R.V.I.S. Bot:', color=0xd89e47)
        embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name='Owner: ', value='@Lukadd.16#8870', inline=True)
        embed.add_field(name='Library Version: ', value="Discord.py " +  d_version, inline=True)
        embed.add_field(name='Python Version: ', value=p_version, inline=True)
        embed.add_field(name='Uptime: ', value=f'{days}d, {hours}h, {minutes}m, {seconds}s', inline=True)
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.channel.send(embed=embed)

    @commands.command(aliases=["uinfo", "whois"])
    async def userinfo(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        createdate = discord.utils.snowflake_time(member.id)

        embed = discord.Embed(title=f'User Info for: ``{member.name}#{member.discriminator}``', colour=0xd89e47)
        embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=(member.avatar_url))
        embed.add_field(name='User ID:', value=f'{member.id}', inline=True)
        embed.add_field(name='Bot:', value=f'{member.bot}', inline=True)
        #embed.add_field(name='Highest Role:', value=f'{u_roles.roles}', inline=True)
        # Think of another piece of info that can go here and be inline with the highest role
        embed.add_field(name='Account Creation Date:', value=f'{createdate} GMT', inline=False)
        embed.add_field(name='Guild Join Date:', value=f'{member.joined_at} GMT ``(Member #: WIP)``', inline=False) # Insert member number here
        #embed.add_field(name='Last Time Active')
        embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=(ctx.author.avatar_url))
        await ctx.channel.send(embed=embed)            

def setup(bot):
    bot.add_cog(UtilitiesCog(bot))
