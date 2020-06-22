# ----------------------------------------------------------------------------
# Description: Cog that contains the re-designed help command for JARVIS Bot
# ----------------------------------------------------------------------------

import discord
from discord.ext import commands

class NewHelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Change bullet points to code blocks with > arrows?

    # Also, remove multiban and multikick from the command, only have stuff that will be usable (with fun commands as an exception)

    # Add a seperate owners only help menu

    # Still need to add help for ban, unban, softban, purge

    # Add prefix+commandname as a title, change author to botname Help Menu (much easier, all sub commands will have this as author and can be changed easily via config.py)

    @commands.group()
    async def nhelp(self, ctx):
        if ctx.invoked_subcommand is None:
            embed=discord.Embed(
                description=f"Run `{self.bot.config.BOT_PREFIX}help <commandname>` to view detailed help on a specific command\n"
                            "`[] Required Args`\n"
                            "`<> Optional Args`\n\n"
                            "Click the header of any of my commands to invite me to your own server", # Will become useless with the proposed change above
                colour=self.bot.config.BOT_COLOUR
            )
            embed.set_author(name="J.A.R.V.I.S. Bot Help", url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
            embed.add_field(name="Fun Commands [All Disabled]", value="`choose`, `roll`", inline=False)
            embed.add_field(name="Utility Commands [6]", value="`about`, `avatar`, `changelog`, `ping`, `suggest`, `whois`", inline=False)
            embed.add_field(name="Moderation Commands [5]", value="`ban`, `kick`, `purge`, `softban`, `unban`", inline=False) # None of these have sub-help commands atm
            embed.set_footer(text=self.bot.config.BOT_FOOTER)
            await ctx.send(embed=embed)

    @nhelp.command(enabled=False)
    async def choose(self, ctx):
        pass

    @nhelp.command(enabled=False)
    async def roll(self, ctx):
        pass

    @nhelp.command(aliases=["botinfo", "info"])
    async def about(self, ctx):
        embed=discord.Embed(
            description=f"Retrieves relevant information about me (uptime, library, etc.)\n\n"
                        "**Type:** Utility\n"
                        f"**Usage:** `{self.bot.config.BOT_PREFIX}about`\n"
                        "**Aliases:** `botinfo`, `info`",
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(name=f"{self.bot.user.name} About Command", url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @nhelp.command(aliases=["av"])
    async def avatar(self, ctx):
        embed=discord.Embed(
            description=f"Outputs an enlarged version of a specified user's profile picture\n\n"
                        "**Type:** Utility\n"
                        f"**Usage:** `{self.bot.config.BOT_PREFIX}avatar <user>`\n"
                        f"**Aliases:** `av`\n{self.bot.config.BOT_HELP_USER_ARG}",
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(name=f"{self.bot.user.name} Avatar Command", url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @nhelp.command(aliases=["version", "whatsnew"])
    async def changelog(self, ctx):
        embed=discord.Embed(
            description=f"Learn what's new with this version of the bot\n\n"
                        "**Type:** Utility\n"
                        f"**Usage:** `{self.bot.config.BOT_PREFIX}changelog`\n"
                        "**Aliases:** `version`, `whatsnew`",
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(name=f"{self.bot.user.name} Changelog Command", url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @nhelp.command()
    async def ping(self, ctx):
        embed=discord.Embed(
            description=f"Tests my connection to Discord\n\n"
                        "**Type:** Utility\n"
                        f"**Usage:** `{self.bot.config.BOT_PREFIX}ping`",
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(name=f"{self.bot.user.name} Ping Command", url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @nhelp.command(aliases=["sinfo"], enabled=False)
    async def serverinfo(self, ctx):
        embed=discord.Embed(
            description=f"Retrieves information about this server\n\n"
                        "**Type:** Utility\n"
                        f"**Usage:** `{self.bot.config.BOT_PREFIX}serverinfo`\n"
                        "**Aliases:** `sinfo`",
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(name=f"{self.bot.user.name} ServerInfo Command", url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @nhelp.command()
    async def suggest(self, ctx):
        embed=discord.Embed(
            description=f"Allows you to report a bug or suggest ideas for new commands/improvements to existing ones. Your response is sent directly to the developer.\n\n"
                        "**Type:** Utility\n"
                        f"**Usage:** `{self.bot.config.BOT_PREFIX}suggest <yoursuggestion>`",
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(name=f"{self.bot.user.name} Suggest Command", url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @nhelp.command(aliases=["userinfo", "uinfo"])
    async def whois(self, ctx):
        embed=discord.Embed(
            description=f"Retrieves relevant information about a specified user in this server\n\n"
                        "**Type:** Utility\n"
                        f"**Usage:** `{self.bot.config.BOT_PREFIX}whois <user>`\n"
                        f"{self.bot.config.BOT_HELP_USER_ARG}",
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(name=f"{self.bot.user.name} Whois Command", url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @nhelp.command(enabled=False)
    async def ban(self, ctx):
        embed=discord.Embed(
            description=f"Bans a specified user from your server.\n\n"
                        "**Type:** Moderation\n"
                        f"**Usage:** `{self.bot.config.BOT_PREFIX}ban <userID or mention> <reason> <days>`\n"
                        f"{self.bot.config.BOT_HELP_REASON_ARG}{self.bot.config.BOT_HELP_BAN_ARG}", # New line?
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(name=f"{self.bot.user.name} Ban Command", url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    @nhelp.command()
    async def kick(self, ctx):
        embed=discord.Embed(
            description=f"Kicks a specified user from your server.\n\n"
                        "**Type:** Moderation\n"
                        f"**Usage:** `{self.bot.config.BOT_PREFIX}kick <userID or mention> <reason>`\n"
                        f"{self.bot.config.BOT_HELP_REASON_ARG}",
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(name=f"{self.bot.user.name} Kick Command", url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

    # Continue to add moderation help subcommands, include a "usage" thing for perm requirements

    @nhelp.command(enabled=False)
    async def multiban(self, ctx):
        embed=discord.Embed(
            description=f"Ban many users from your server with a single command.\n\n"
                        "**Type:** Moderation\n"
                        f"**Usage:** `{self.bot.config.BOT_PREFIX}multiban <userIDs or mentions> <reason> <days>`\n"
                        f"{self.bot.config.BOT_HELP_REASON_ARG}\n"
                        f"{self.bot.config.BOT_HELP_BAN_ARG}",
            colour=self.bot.config.BOT_COLOUR
        )
        embed.set_author(name=f"{self.bot.user.name} Multi-Ban Command", url=self.bot.config.BOT_URL, icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=self.bot.config.BOT_FOOTER)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(NewHelpCog(bot))