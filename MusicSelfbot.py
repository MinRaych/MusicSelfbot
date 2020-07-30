import os
import discord
import youtube_dl
# - Download ffmpeg https://ffmpeg.org/download.html #
# - Download discord.py https://pypi.org/project/discord.py/ #
# - Download youtube_dl https://pypi.org/project/youtube_dl/ #

token = "" # <-- Token

client = discord.Client()
prefix = ">"

@client.event
async def on_message(message):
    global player
    if message.content.startswith(prefix + "play"):
        try:
            oof = message.content.split(" ")
            url = oof[1]
            server = message.guild.voice_client
            if server is not None:
                await server.disconnect()
            try:
                os.remove("player.mp3")
            except FileNotFoundError:
                print("idk")

            if url[0:32] == "https://www.youtube.com/watch?v=":
                channel = await message.author.voice.channel.connect()
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '720',
                    }],
                    'outtmpl': 'player.mp3'
                }

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                source = discord.FFmpegPCMAudio("player.mp3")
                player = channel.play(source)
        except:
            await message.channel.send("Musique introuvable")
    elif message.content.lower().startswith(prefix + "join"):
        return
    elif message.content.lower().startswith(prefix + "leave"):
        await player.disconnect()

if __name__ == '__main__':
    client.run(token, bot=False)
