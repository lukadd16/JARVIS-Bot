# --------------------------------------------------------------
# Description: Cog that holds all of the bot's key variables
# --------------------------------------------------------------

# Bot Token
BOT_TOKEN = ""

# Bot Prefix
BOT_PREFIX = "jar "

# Discord Bot List Token (for future)
DBL_TOKEN = ""

# Initial Extensions
BOT_EXTENSIONS = [
    "cogs.help",
    "cogs.newhelp",
    "cogs.owner",
    "cogs.utilities",
    "cogs.background",
    "cogs.error_handler",
    "cogs.moderation",
    "cogs.fun"
    #"cogs.jishaku"
]
# Bot Emoji Config
BOT_EMOJI_ARROW = "<:member_joinJB:674374208251232325>"
BOT_EMOJI_BTAG = "<:bot_tagJB:674379570769821713>"
BOT_EMOJI_ONLINE = "<:status_onlineJB:674384199809105933>"
BOT_EMOJI_IDLE = "<:status_idleJB:674384199448395788>"
BOT_EMOJI_DND = "<:status_dndJB:674384199272103946>"
BOT_EMOJI_OFFLINE = "<:status_offlineJB:674384202539728926>"
BOT_EMOJI_STREAM = "<:status_streamingJB:674384199729414164>"

# Bot String Values
BOT_VERSION = "V0.6.2.0" # Change this each time I make significant changes to bot
BOT_BETAVERSION = "V0.6.3.0"
BOT_FEATURES = f"> New Version Naming Scheme (bot is considered Pre-Release now)\n> Revamped Help Command! (with sub-commands too)\n> New Suggest Command! (send the dev your ideas for the bot)\n> New Avatar Command\n> Revamped Whois Command\n> Revamped About Command\n> Many behind-the-scenes changes" # Add new version changes/fixes here (displayed in version command)
BOT_URL = "https://discordapp.com/api/oauth2/authorize?client_id=559890663924170762&permissions=268561542&scope=bot" # Invite link for bot, has audit, role and message perms
BOT_AUTHOR = "Click to invite me!" # Figure out how I can make this part blue
BOT_OLDFOOTER = "This bot was created by @Lukadd.16#8870, please DM him if you have any bugs or issues to report."
BOT_FOOTER = f"Found a bug/have an idea? Send it to the dev with {BOT_PREFIX}suggest"
BOT_HELP_USER_ARG = "```Argument is optional but if specified must be a: @mention, userID, or username#discriminator```"
BOT_HELP_REASON_ARG = "```Optional reason argument is a message that will be appended in the server audit log for other moderators to see, if none is provided, a default one will be used.```"
BOT_HELP_BAN_ARG = "```Optional days argument is how many days prior (to a max of 7) that the bot will delete messages sent by the specified user.```"

# Bot Embed Colours
BOT_COLOUR = 0xd89e47
BOT_ERR_COLOUR = 0xd80000
BOT_SUCCESS_COLOUR = 0x00e600
# BOT_SUCCESS_COLOUR = 0x1414ff

# PSQL (for future)
DB_CONN_INFO = {
    "user": "",
    "password": "",
    "host": "",
    "database": ""
}

LOG_LEVEL = "debug"

# Logging Channel (joined new server, critical errors, etc.)
LOG_CHANNEL_ID = 659072068725506058

# Status Channel (successful login, successful shutdown, etc.)
STATUS_CHANNEL_ID = 617794889291268105

# Suggestion Channel
SUGGEST_CHANNEL_ID = 655464964869586945
