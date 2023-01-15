#!/usr/bin/env python3
import asyncio
from pathlib import Path
from random import randint

import discord
from discord.ext import commands

from utils import (
    return_playback_images_to_embed,
    return_embed_help_images
)


class MusicBot(commands.Cog):
    "MusicBot Cog for my personal music bot"

    def __init__(self, bot):
        self.bot = bot
        self.vc = None       # discord.VoiceClient()
        self.music_index = 0
        self.musics_list = []

        self.default_embed_color = 0x10ffa8
        self.embedding_playback = discord.Embed(color=self.default_embed_color)
        self.reproduction_images_to_embed = return_playback_images_to_embed()
        self.embed_help_images = return_embed_help_images()

        self.playlists = {
            "funk-shitpost": "./musics/funk-shitpost",
            "lofi": "./musics/lofi"
        }

    @commands.command()
    async def play(self, ctx, playlist=None):
        if ctx.author.voice:
            if not self.vc or not self.vc.is_connected():
                if playlist not in self.playlists:
                    await ctx.send(
                        f"[-] {ctx.author.mention}, você inseriu uma playlist inexistente, digite `$list-playlists` para "
                        "visualizar as playlists atuais"
                        )

                self.musics_list = self.get_musics_from_directory(self.playlists[playlist])
                self.vc = await ctx.author.voice.channel.connect()
                self.music_index = 0
                await ctx.send(f"[-] Começando a reprodução da playlist `{playlist}`")

                while True:
                    self.embedding_playback.title = self.get_music_name(self.musics_list[self.music_index].name)
                    self.embedding_playback.description = f"`Reproduzindo a {self.music_index+1}° faixa de {len(self.musics_list)} de faixa(s)`"
                    self.embedding_playback.set_author(
                        name=f"Playlist - {playlist.capitalize()}",
                        icon_url="http://www.clipartbest.com/cliparts/nTB/RaB/nTBRaB6kc.gif"    
                    )
                    self.embedding_playback.set_image(url=self.reproduction_images_to_embed[randint(0, len(self.reproduction_images_to_embed)-1)])

                    self.vc.play(discord.FFmpegPCMAudio(
                        executable="/usr/bin/ffmpeg",
                        source=self.musics_list[self.music_index]
                    ))
                    self.vc.source = discord.PCMVolumeTransformer(self.vc.source, 0.7)

                    # await ctx.send(f"[-] Reproduzindo: `{self.musics_list[self.music_index]}`")
                    await ctx.send(embed=self.embedding_playback)

                    while self.vc.is_playing() or self.vc.is_paused():
                        await asyncio.sleep(1)

                    if self.music_index+1 < len(self.musics_list):
                        self.music_index += 1
                    else:
                        break

                await self.vc.disconnect()
                await ctx.send(f"[-] Reprodução da playlist `{playlist}` finalizada! Desconectando...")

            else:
                await ctx.send(f"[-] {ctx.author.mention}, o bot já está em reprodução!")

        else:
            await ctx.send(f"[-] {ctx.author.mention}, você não está em um canal de voz!")

    @commands.command()
    async def stop(self, ctx):
        if ctx.author.voice:
            if self.vc:
                await self.vc.disconnect()
                await ctx.send(f"[-] Desconectando do canal de voz...")
            else:
                await ctx.send(f"[-] {ctx.author.mention}, o bot não está em reprodução")
        else:
            await ctx.send(f"[-] {ctx.author.mention}, você não está num canal de voz!")


    @commands.command()
    async def pause(self, ctx):
        if ctx.author.voice:
            if self.vc != None:
                if self.vc.is_playing():
                    self.vc.pause()
                else:
                    await ctx.send(f"[-] {ctx.author.mention}, a reprodução já está pausada!")
            else:
                await ctx.send(f"[-] {ctx.author.mention}, o bot não está em reprodução. Digite `$help`")
        else:
            await ctx.send(f"[-] {ctx.author.mention}, você não está num canal de voz!")

    @commands.command()
    async def resume(self, ctx):
        if ctx.author.voice:
            if self.vc != None:
                if self.vc.is_paused():
                    self.vc.resume()
                else:
                    await ctx.send(f"[-] {ctx.author.mention}, a reprodução já está ocorrendo!")
            else:
                await ctx.send(f"[-] {ctx.author.mention}, o bot não está em reprodução. Digite `$help`")
        else:
            await ctx.send(f"[-] {ctx.author.mention}, você não está num canal de voz!")

    @commands.command()
    async def skip(self, ctx):
        if ctx.author.voice:
            if self.vc != None:
                if self.vc.is_connected():
                    if self.music_index+1 < len(self.musics_list):
                        self.music_index += 1
                    else:
                        await ctx.send(f"[-] A playlist chegou ao fim, a reprodução atual é a última!")
                        return

                    self.embedding_playback.title = self.get_music_name(self.musics_list[self.music_index].name)
                    self.embedding_playback.description = f"`Reproduzindo a {self.music_index+1}° faixa de {len(self.musics_list)} de faixa(s)`"
                    self.embedding_playback.set_image(url=self.reproduction_images_to_embed[randint(0, len(self.reproduction_images_to_embed)-1)])

                    self.vc.stop()
                    self.vc.play(discord.FFmpegPCMAudio(
                        executable="/usr/bin/ffmpeg",
                        source=self.musics_list[self.music_index]
                    ))

                    await ctx.send(embed=self.embedding_playback)

                    while self.vc.is_playing or self.vc.is_paused():
                        await asyncio.sleep(1)
            else:
                await ctx.send(f"[-] {ctx.author.mention}, o bot não está em reprodução. Digite `$help`")
        else:
            await ctx.send(f"[-] {ctx.author.mention}, você não está num canal de voz!")

    @commands.command()
    async def helpme(self, ctx):
        embed = discord.Embed(
            title="Menu de Ajuda",
            description="Lista de comandos para o bot:",
            color=self.default_embed_color
        )

        embed.set_image(url=self.embed_help_images["helpme"])
        embed.add_field(
            name="Comandos\n", 
            value=self.get_commands_list(), 
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def list_playlists(self, ctx):
        embed = discord.Embed(
            title="Lista de Playlists",
            color=self.default_embed_color
        )

        embed.set_image(url=self.embed_help_images["list_playlists"])
        embed.add_field(
            name="Playlists",
            value=self.get_playlists(),
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def list_songs(self, ctx, playlist=None):
        if playlist is not None:
            if playlist in self.playlists:
                embed = discord.Embed(
                    title="Lista de músicas",
                    description=f"Total de músicas: `{len(self.get_musics_from_directory('./musics/' + playlist))}` faixas",
                    color=self.default_embed_color
                )

                embed.set_image(url=self.embed_help_images["list_songs"])
                embed.add_field(
                    name="Faixas:", 
                    value=self.get_all_musics_name("./musics/" + playlist),
                    inline=False
                )

                await ctx.send(embed=embed)


            else:
                await ctx.send(f"[-] Playlist inválida! Utilize `$list_playlists` para listar todas as playlists existentes")
        else:
            await ctx.send(f"[-] Nenhuma playlist especificada!")
            
    
    def get_all_musics_name(self, directory):
        musics_list = self.get_musics_from_directory(directory)
        return_string = ""

        for index, element in enumerate(musics_list, start=1):
            return_string += f"\n`[{index}]` => **`{self.get_music_name(element.name)}`**"

        return return_string

    def get_music_name(self, name):
        dot_index = name.find(".")
        music_name = name[:dot_index]
        return music_name

    def get_playlists(self):
        return_string = "\n\n"
        for count, playlist in enumerate(self.playlists, start=1):
            return_string += f"\nPlaylist {count}: `{playlist}`"
        
        return return_string

    def get_commands_list(self):
        return """\n
        `$play [playlist-name]` - Reproduz uma playlist específica
        `$stop` - Encerra a reprodução e desconecta do canal de voz
        `$pause` - Pausa a reprodução atual
        `$resume` - Retorna a reprodução atual
        `$skip` - Avança a reprodução atual para a próxima na playlist
        `$list_playlists` - Lista todas as playlists existentes
        `$list_songs [playlist-name]` - Lista todas as músicas de uma playlist específica
        """

    def get_musics_from_directory(self, directory):
        path = Path(directory).glob("**/*")
        music_list = [x for x in path if x.is_file()]
        return music_list

if __name__ == "__main__":
    ...
