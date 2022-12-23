#!/usr/bin/env python3

import discord
import os
import youtube_dl
from discord.ext import commands
from dotenv import load_dotenv
from time import sleep
from music_utils import get_musics
import asyncio

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)
music_index = 0

@bot.event
async def on_ready():
    print(f"[+] {bot.user} is working!")

@bot.command(pass_context=True)
async def play(ctx):
    try:
        voice_channel = ctx.author.voice
        channel = None
        if voice_channel != None:
            await ctx.send(f"[+] Entrando no canal de voz e começando a reprodução da playlist!")
            global vc
            vc = await voice_channel.channel.connect()
            global musics
            musics = get_musics("./musics")
            global music_index

            #print(musics)

            for index, music in enumerate(musics):
                if not vc.is_connected():
                    return

                await ctx.send(f"Reproduzindo: {musics[music_index]}")
                vc.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source=musics[music_index]))
                vc.source = discord.PCMVolumeTransformer(vc.source, 0.7)

                print(f"Index play: {music_index}")

                while vc.is_playing() or vc.is_paused():
                    await asyncio.sleep(1)

                music_index += 1
                print(f"Index play inc: {music_index}")

            await ctx.send("[+] Playlist finalizada!")
            await vc.disconnect()

        else:
            await ctx.send(f"[+] {ctx.author.name}, você não está em um canal de voz!")


    except Exception as err:
        print(err)

@bot.command(pass_context=True)
async def pause(ctx):
    voice_channel = ctx.author.voice
    if voice_channel != None:
        try:
            if vc.is_playing():
                vc.pause()
            else:
                await ctx.send("[+] A reprodução já está pausada!")
        
        except Exception as err:
            print(err)
            await ctx.send(f"[+] {ctx.author.name}, o bot não está em reprodução!")

    else:
        await ctx.send(f"[+] {ctx.author.name}, você não está em um canal de voz!")

@bot.command(pass_context=True)
async def resume(ctx):
    voice_channel = ctx.author.voice
    if voice_channel != None:
        try:
            if vc.is_paused():
                vc.resume()

            else:
                await ctx.send("[+] A reprodução já está ocorrendo!")

        except Exception as err:
            print(err)
            await ctx.send(f"[+] {ctx.author.name}, o bot não está em reprodução!")

    else:
        await ctx.send(f"[+] {ctx.author.name}, você não está em um canal de voz!")


@bot.command(pass_context=True)
async def stop(ctx):
    voice_channel = ctx.author.voice
    if voice_channel != None:
        try:
            if vc.is_connected():
                await vc.disconnect()
            else:
                await ctx.send("[+] O bot não está conectado!")

        except Exception as err:
            print(err)
            await ctx.send("[+] O bot não está em reprodução!")

    else:
        await ctx.send(f"[+] {ctx.author.name}, você não está em um canal de voz!")

@bot.command(pass_context=True)
async def skip(ctx):
    voice_channel = ctx.author.voice
    if voice_channel != None:
        try:
            if vc.is_connected():
                global music_index
                music_index += 1
                print(f"Index skip: {music_index}")
                await ctx.send(f"Reproduzindo: {musics[music_index]} (SKIP)")
                vc.stop()
                vc.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source=musics[music_index]))

                while vc.is_playing() or vc.is_paused():
                    await asyncio.sleep(1)

        except Exception as err:
            print(err)

    else:
        await ctx.send(f"[+] {ctx.author.name}, você não está em um canal de voz!")


load_dotenv()
bot.run(os.getenv("TOKEN"))
