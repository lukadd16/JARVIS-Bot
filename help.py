# -----------------------------------------------------------------------
# Description: Cog that contains the help command for JARVIS Bot
# -----------------------------------------------------------------------

import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):  
        embed=discord.Embed(title="HELP for JARVIS Bot", description=f"Prefix: {self.bot.config.BOT_PREFIX}\n\nClick the header of any JARVIS command to invite the bot into your own server", color=0xd89e47)
        embed.set_author(name="J.A.R.V.I.S. Bot", url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        #embed.add_field(name="help", value="The command you are currently using", inline=False)
        embed.add_field(name="My Commands:", value="**Fun** (Currently Disabled: is due for an overhaul)", inline=False)
        embed.add_field(name="roll", value=f"Rolls dice in NdN format\n - Usage: ``{self.bot.config.BOT_PREFIX}roll [# of dice]d[# of sides]``", inline=False)
        embed.add_field(name="choose", value="For settling hard decisions", inline=False)
        #embed.add_field(name="ironman", value="[Not released yet], Will retrieve stats about a specific Iron Man Armour", inline=False)
        embed.add_field(name="\u200b", value="**Utility**", inline=False)
        embed.add_field(name="botinfo", value="Retrieves relevant information about me\n - Aliases: `about`, `binfo`", inline=False)
        embed.add_field(name="userinfo", value=f"Retrieves information about a person in this server, arg is optional\n - Usage: ``{self.bot.config.BOT_PREFIX}userinfo [@UserName]``\n - Aliases: `whois`, `uinfo`", inline=False)
        embed.add_field(name="ping", value="Test my connection to Discord", inline=False)
        embed.add_field(name="uptime", value="Outputs how long I have been online", inline=False)
        embed.add_field(name="version", value="Prints my protocol version and what is new with this version", inline=False)
        embed.add_field(name="\u200b", value="**Moderation**", inline=False)
        embed.add_field(name="purge", value=f"Clears a specified number of messages from the channel the command is being invoked in\n - Requires ``Manage Messages`` Permission\n - Usage: ``{self.bot.config.BOT_PREFIX}purge [# of Messages]``\n - Alias: `clear`", inline=False)
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(HelpCog(bot))