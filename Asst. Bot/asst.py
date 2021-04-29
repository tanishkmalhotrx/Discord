import discord
from discord.ext import commands, tasks
from itertools import cycle
import youtube_dl
import os
#from keep_alive import keep_alive

client = commands.Bot(command_prefix = 'm.')
client.remove_command("help")
players = {}
status = cycle(["||m.Help||", "*MerrdeU's Asst. Bot*"])

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    change_status.start()
    print("Bot is ready!")
#-------------------------------------------------------------------------------------------
@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name="Bot")
    await client.add_roles(member, role)
#-------------------------------------------------------------------------------------------
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Sorry, you don't have the permissions!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter all the required areguments!")
    else:
        raise error
        await ctx.send("No such command available!")
#-------------------------------------------------------------------------------------------
@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
@client.command() # m.online command
async def online(ctx):
    await ctx.send("Hey I am Online! What can I do for ya?")
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
@client.command()# m.version command
async def version(ctx):
    awaitctx.send("This version is M1.0!")
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
@client.group(invole_without_command=True)
async def Help(ctx):
    em = discord.Embed(title="Help", description="Use m.Help <command> for extended info on a command.", color=ctx.author.color)
    em.add_field(name="Moderation", value="Mute, Unmute, Ban, Unban, Kick")
    em.add_field(name="Music", value="Join, Leave, Play, Pause, Resume, Skip")
    em.add_field(name="More Commands", value="Version")
    await ctx.send(embed=em)
@Help.command()
async def mute(ctx):
    em = discord.Embed(title="Mute", description="Mutes a member from the guild by giving him/her the 'MUTED🤐' role", color=ctx.author.color)
    await ctx.send(embed=em)
@Help.command()
async def unmute(ctx):
    em = discord.Embed(title="Unmute", description="Unmutes a member from the guild by taking away the 'MUTED🤐' role", color=ctx.author.color)
    await ctx.send(embed=em)
@Help.command()
async def ban(ctx):
    em = discord.Embed(title="Ban", description="Bans a member from the guild. He/She won't be ablt to join the server", color=ctx.author.color)
    await ctx.send(embed=em)
@Help.command()
async def unban(ctx):
    em = discord.Embed(title="Unban", description="Unbans a member from the guild. He/She van now join the server", color=ctx.author.color)
    await ctx.send(embed=em)
@Help.command()
async def kick(ctx):
    em = discord.Embed(title="kick", description="kicks a member from the guild.", color=ctx.author.color)
    await ctx.send(embed=em)
@Help.command()
async def version(ctx):
    em = discord.Embed(title="Version", description="Tells the latest verion, the Bot is running on.", color=ctx.author.color)
    await ctx.send(embed=em)
@Help.command()
async def play(ctx):
    em = discord.Embed(title="Play", description="Join the 'General' voice channel and put in the command <m.play> + 'youtube link'. The bot will download the song and start playing it!", color=ctx.author.color)
    await ctx.send(embed=em)
@Help.command()
async def leave(ctx):
    em = discord.Embed(title="Leave", description="Done listening to songs? Use this command to disconnect the bot from a voice channel", color=ctx.author.color)
    await ctx.send(embed=em)
@Help.command()
async def pause(ctx):
    em = discord.Embed(title="Pause", description="This command will pause the song which is being played in the voice channel!", color=ctx.author.color)
    await ctx.send(embed=em)
@Help.command()
async def resume(ctx):
    em = discord.Embed(title="Resume", description="This command will resume the song which was being played in the voice channel!", color=ctx.author.color)
    await ctx.send(embed=em)
@Help.command()
async def stop(ctx):
    em = discord.Embed(title="Stop", description="This command will stop the song which is being played in the voice channel!", color=ctx.author.color)
    await ctx.send(embed=em)
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
@client.command(aliases=['cm']) # m.clear/m.cm - command to clear msgs from that channel
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit = amount)
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
@client.command(aliases=['m']) # m.mute/m.m command to mute someone - m.m @abc
@commands.has_permissions(kick_members=True)
async def mute(ctx, member : discord.Member):
    muted_role = ctx.guild.get_role(832915093708734494)
    await member.add_roles(muted_role)
    await ctx.send(member.mention +" has been muted!")
#-------------------------------------------------------------------------------------------
@client.command(aliases=['um']) # m.unmute/m.um command to unmute someone - m.um @abc
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member : discord.Member):
    muted_role = ctx.guild.get_role(832915093708734494)
    await member.remove_roles(muted_role)
    await ctx.send(member.mention +" has been unmuted!")
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
@client.command(aliases=['k']) # m.kick/m.k - command to kick someone and DM them - m.k @abc
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member,*,reason="No reason provided!"):
    try:
        await member.send("You have been kicked from 'server name', Because: " + reason)
    except:
        await ctx.send("The member has their DMs colsed!")
    await member.kick(reason=reason)
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
@client.command(aliases=['b']) # m.ban/m.b - command to ban someone and Dm them - m.b @abc
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member,*,reason="No reason provided!"):
    try:
        await ctx.send(member.name + "has been banned from 'server name', Because: "+ reason)
    except:
        await ctx.send("The member has their DMs colsed!")
    await member.ban(reason=reason)
#-------------------------------------------------------------------------------------------
@client.command(aliases=['ub']) # m.unban/m.ub - command to unban someone - m.ub abc#1234
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split("#")

    for banned_entry in banned_users:
        user = banned_entry.user

        if (user.name, user.discriminator) == (member_name, member_disc):

            await ctx.guild.unban(user)
            await ctx.send(member_name +"has been unbanned!")
            return

    await ctx.send(member+"was not found:(")
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
@client.command(aliases=["pl"])
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
#-------------------------------------------------------------------------------------------
@client.command(aliases=["lv"])
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")
#-------------------------------------------------------------------------------------------
@client.command(aliases=["ps"])
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")
#-------------------------------------------------------------------------------------------
@client.command(aliases=["rs"])
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")
#-------------------------------------------------------------------------------------------
@client.command(aliases=["st"])
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#keep_alive()
client.run('Enter your bot token')
