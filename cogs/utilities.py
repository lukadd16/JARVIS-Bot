# ------------------------------------------------------------------
# Description: Cog that houses utilities commands for JARVIS Bot
# ------------------------------------------------------------------

# Logging ideas:
# - Log bulk deletes regardless of what bot they are from (if they are from jarvis then log event differently because the perpetrator would be knows)
# - Log role mentions (see link bookmarked in toolbar that refers to discord.Message, see if can intertwine this with on_message event)
# - Figure out how to handle which channel to send logs to

# Add member ping (like dyno) to title of this command and avatar command

# Too lazy to do now but will need to compile the names of users roles, convert them to mentionable string and then append these strings to a new list

import discord
import psutil
import sys
import time
import os
import logging

from myutils import botUtils
from datetime import datetime
from discord.ext import commands

logger = logging.getLogger("JB.main") # Next step is to figure out how I can get different named loggers all to use the same file

class UtilitiesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Move all repeated lines of code to utils folder so that all I need to do is call it once, using one line of code
    # Try to also format my code nicer (take MrBot approach)

    # Keep ping command and add extra ping types to it (like MrBot)

    # Make a system command that gives info about the server the bot is running on

    @commands.command(aliases=["botinfo", "info"])
    async def about(self, ctx):
        # Get version info for library and python runtime
        d_version = discord.__version__
        p_version = sys.version[0:5]

        # Get bots' total uptime (as a good skill, should try to put this into its own method)
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        # Calculate websocket latency
        web_latency = self.bot.latency * 1000

        # Total users and guilds the bot can see
        total_users = len(self.bot.users)
        total_guilds = len(self.bot.guilds)
        
        embed = discord.Embed(title='Bot Info', color=self.bot.config.BOT_COLOUR)
        embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.add_field(name='Developer: ', value='`Lukadd.16#8870`', inline=True)
        embed.add_field(name='Bot Version:', value=f'`{self.bot.config.BOT_VERSION}`', inline=True) # See .txt file for full proposals for this command, something like Pre-Release | V0.XX
        embed.add_field(name='Uptime: ', value=f'`{days}d, {hours}h, {minutes}m, {seconds}s`', inline=True)
        embed.add_field(name='User Count: ', value=f'`{total_users}`', inline=True)
        embed.add_field(name='Python Version: ', value=f'`{p_version}`', inline=True)
        embed.add_field(name='Websocket Ping: ', value='`{:.2f}ms`'.format(web_latency), inline=True)
        embed.add_field(name='Guild Count: ', value=f'`{total_guilds}`', inline=True)
        embed.add_field(name='Library Version: ', value=f'`Discord.py {d_version}`', inline=True)
        embed.add_field(name='Server OS: ', value=f'`Placeholder`', inline=True) # Use psutils here?
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.channel.send(embed=embed)

    # WIP, scraping admin idea instead for if the staff member (defined as kick + ban perms pretty much) has send perms to the channel they are specifying, then they are allowed to go through with this command
    @commands.command(aliases=["announcement"], enabled=False)
    @commands.guild_only()
    async def announce(self, ctx, target_channel: discord.TextChannel, *, user_message: str):
        embed = discord.Embed(description=f'{user_message}', colour=self.bot.config.BOT_COLOUR)
        embed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await target_channel.send(embed=embed)

    @commands.command(aliases=["av"])
    async def avatar(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        user_pfp = member.avatar_url_as(format=None, static_format='png', size=256)

        embed = discord.Embed(title=f'Avatar – ``{member.name}#{member.discriminator}``', description=member.mention, colour=self.bot.config.BOT_COLOUR)
        embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_image(url=user_pfp)
        embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=f'{ctx.author.avatar_url}')

        #userpfp = member.avatar_url_as(format=None, static_format='png', size=512)
        await ctx.channel.send(embed=embed)

    @commands.command(aliases=["version", "whatsnew"])
    async def changelog(self, ctx):
        # Remove beta version field and replace with only one "Current Version" or similar that has a variable for version number that changes depending on if this instance is a beta version or not
        # (better idea) In the config file for the beta version only, just set the BOT_VERSION value to the BETAVERSION value and then all that's needed to be done here is just use that one variable

        embed = discord.Embed(color=self.bot.config.BOT_COLOUR)
        embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        #embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Stable Version:", value=self.bot.config.BOT_VERSION, inline=True)
        embed.add_field(name="Beta Version:", value=self.bot.config.BOT_BETAVERSION, inline=True)
        embed.add_field(name="New Features/Fixes with this Version:", value=f"```{self.bot.config.BOT_FEATURES}```", inline=False) # Change to code block
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        # Start timer used for latency calculation
        start = time.perf_counter()
        logger.debug("Ping timer started")

        embed = discord.Embed(color=self.bot.config.BOT_COLOUR)
        embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Ping...", value='Message Round Trip: \nDiscord Websocket: ')
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        message = await ctx.channel.send(embed=embed)

        # Calculate round trip and websocket latencies
        end = time.perf_counter()
        logger.debug("Ping timer ended")
        duration = (end - start) * 1000
        web_latency = self.bot.latency * 1000

        embed = discord.Embed(color=self.bot.config.BOT_COLOUR)
        embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(
            name="Pong!",
            value='Message Round Trip: ``{:.2f}ms``\nDiscord Websocket: ``{:.2f}ms``'.format(duration, web_latency) # Cuts latency values down to two decimal places
        )
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await message.edit(embed=embed)
        logger.debug(f"Ping response sent")

    @commands.command() # Deprecated
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send("I have been online for " f"{days}d, {hours}h, {minutes}m, {seconds}s, Sir")

    @commands.command(aliases=["userinfo", "uinfo"])
    @commands.guild_only()
    async def whois(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        # Get various info on user
        user_createdate = discord.utils.snowflake_time(member.id) # snowflake_time is outputted in the form of datetime.datetime
        user_createdate_friendly = user_createdate.strftime("%a, %b %d, %Y @ %H:%M:%S %p") # Convert account creation time into readable format
        member_joindate_friendly = member.joined_at.strftime("%a, %b %d, %Y @ %H:%M:%S %p") # Convert guild join time into readable format
        bot_identify = botUtils.bot_check(member) # Call function that returns an emoji if the user is a bot
        status_emoji = botUtils.get_member_status(member) # Call function that returns an emoji based on user's current status
        member_role_sum = len(member.roles) - 1 # Subtract by 1 to exclude @everyone role
        print(member.roles[-1]) # Debug

        # Check sum of member.roles list, if there are no roles (excluding @everyone) return None to prevent 400 Bad Request Error. Otherwise perform list manipulation logic.
        if member_role_sum == 0:
            member_role_list = None
        elif member_role_sum >= 1:
            member_role_list = ' '.join([r.mention for r in member.roles[:0:-1]]) # Stores user roles in a semi-mentionable form

        # Now that I understand how to get roles, make a system that loops through user's roles (from highest to lowest)
        # finding the first one that has a colour other than the default invisible one

        embed = discord.Embed(
            title=f'User Info – ``{member.name}#{member.discriminator}``{status_emoji}',
            description=f'{member.mention + bot_identify}',
            colour=self.bot.config.BOT_COLOUR
            #timestamp=datetime.now()
        )
        embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=(member.avatar_url))
        embed.add_field(name='User ID:', value=f'{member.id}', inline=True)
        embed.add_field(name='Nickname:', value=f'{member.nick}', inline=True)
        embed.add_field(name='Account Created:', value=f'{user_createdate_friendly} GMT', inline=False)
        embed.add_field(name='Joined Guild:', value=f'{member_joindate_friendly} GMT ``(Member #: WIP)``', inline=False) # Insert member number here
        embed.add_field(name=f'Roles [{member_role_sum}]:', value=f"{member_role_list}", inline=False)
        embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=(ctx.author.avatar_url))
        await ctx.channel.send(embed=embed)

    # WIP
    @commands.command(aliases=["sinfo"], enabled=False)
    @commands.guild_only()
    async def serverinfo(self, ctx):
        # Using userinfo embed as a placeholder for now

        embed = discord.Embed(title=f'Server Info for: XX', colour=self.bot.config.BOT_COLOUR)
        embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=(member.avatar_url)) # Set thumbnail to be the server's icon (both animated and static)
        embed.add_field(name='User ID:', value=f'{member.id}', inline=True)
        embed.add_field(name='Bot:', value=f'{member.bot}', inline=True)
        #embed.add_field(name='Highest Role:', value=f'{u_roles.roles}', inline=True)
        # Think of another piece of info that can go here and be inline with the highest role
        embed.add_field(name='Account Creation Date:', value=f'{createdate} GMT', inline=False)
        embed.add_field(name='Guild Join Date:', value=f'{member.joined_at} GMT ``(Member #: WIP)``', inline=False) # Insert member number here
        #embed.add_field(name='Last Time Active')
        embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=(ctx.author.avatar_url))
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def suggest(self, ctx, *, user_suggestion: str):
        suggest_channel = self.bot.get_channel(self.bot.config.SUGGEST_CHANNEL_ID)

        if len(user_suggestion) >= 512:
            embed = discord.Embed(
                title='ERROR',
                description='Your suggestion cannot be more than 512 characters in length, please try to shorten it.',
                colour=self.bot.config.BOT_ERR_COLOUR
            )
            embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
            embed.set_footer(text=self.bot.config.BOT_FOOTER)
            await ctx.channel.send(embed=embed)
            return

        else:
            embed = discord.Embed(title='SUCCESS',
            description=f'Your suggestion for the developer has been received!\nThank you for contributing to the bot.',
            colour=self.bot.config.BOT_SUCCESS_COLOUR
            )
            embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
            embed.set_footer(text=f'Sent by {ctx.author.name}#{ctx.author.discriminator}', icon_url=(ctx.author.avatar_url))
            await ctx.message.delete()
            await ctx.channel.send(embed=embed)

        # Info about the user who sent in the suggestion
        embed = discord.Embed(title='NEW SUGGESTION', colour=self.bot.config.BOT_COLOUR)
        embed.set_author(name='J.A.R.V.I.S. Bot', url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.add_field(
            name='Details:',
            value=f'User: `{ctx.author.name}#{ctx.author.discriminator}` (ID: {ctx.author.id})\n'
                  f'Channel: `#{ctx.channel.name}` (ID: {ctx.channel.id})\n'
                  f'Server: `{ctx.guild.name}` (ID: {ctx.guild.id})',
            inline=False
        )
        embed.add_field(name='Suggestion:', value=f'{user_suggestion}', inline=False)
        embed.set_footer(text=f'Sent by {ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await suggest_channel.send(embed=embed)

        # Add checkmark and reject reactions to the message after it has sent (for the public to vote on)

def setup(bot):
    bot.add_cog(UtilitiesCog(bot))
    #print(os.getcwd())