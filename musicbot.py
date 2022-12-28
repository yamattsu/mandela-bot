#!/usr/bin/env python3
import asyncio
from pathlib import Path
from random import randint

import discord
from discord.ext import commands


class MusicBot(commands.Cog):
    "MusicBot Cog for my personal music bot"

    def __init__(self, bot):
        self.bot = bot
        self.vc = None       # discord.VoiceClient()
        self.music_index = 0
        self.musics_list = []
        self.default_embed_color = 0x10ffa8
        self.playing_embed = discord.Embed(color=self.default_embed_color)

        self.playlists = {
            "funk-shitpost": "./musics/funk-shitpost",
            "lofi": "./musics/lofi"
        }

        self.playing_embed_images = [
            "https://i.pinimg.com/originals/8d/b6/33/8db63391392f24b5946107b0af92caec.jpg",
            "https://wallpapercave.com/wp/wp4779055.png",
            "https://wallpaperaccess.com/full/3434188.jpg",
            "https://wallpapercave.com/wp/wp8151805.jpg",
            "https://wallpapercave.com/wp/wp5756318.jpg",
            "https://wallpaperforu.com/wp-content/uploads/2021/03/Wallpaper-Lofi-Anime-Anime-Girls-Room-Laptop-Brunette-Look48-1536x865.jpg",
            "https://wallpaperaccess.com/full/1511068.png",
            "https://i.pinimg.com/originals/13/ab/1c/13ab1c2a907541d07426df22083f01d1.jpg",
            "https://i.pinimg.com/originals/ad/2c/67/ad2c6767f4fc8c7f3a013d6a11f2ed66.jpg",
            "https://wallpapercave.com/wp/wp5161081.jpg",
            "https://wallpaperboat.com/wp-content/uploads/2021/12/20/79953/lofi-girl-15.jpg",
            "https://wallpaperaccess.com/full/2223498.jpg",
            "https://wallpapercave.com/wp/wp5161083.jpg",
            "https://wallpaperaccess.com/full/754903.jpg",
            "https://wallpapercave.com/wp/wp7817997.jpg"
        ]

        self.help_embed_images = {
            "helpme": "https://lh5.googleusercontent.com/proxy/vhI84k6wjQOZXgG-wbCMbNfTOaKmDshzKGffSr-ApVkqJ_UAMmhR0yzJhTH3SLLz5Jz9M-v_9TDJopwiE2HTHI8V6GB7fI742pp5JdXe5YlMJ9EKwN-sa8SonKlUG6Hn=w1200-h630-p-k-no-nu",
            "list_playlists": "https://wallpaperaccess.com/full/849778.jpg",
            "list_songs": "https://wallpapercave.com/wp/wp4602843.png"
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
                    self.playing_embed.title = self.get_music_name(self.musics_list[self.music_index].name)
                    self.playing_embed.description = f"`Reproduzindo a {self.music_index+1}° faixa de {len(self.musics_list)} de faixa(s)`"
                    self.playing_embed.set_author(
                        name=f"Playlist - {playlist.capitalize()}",
                        icon_url="http://www.clipartbest.com/cliparts/nTB/RaB/nTBRaB6kc.gif"    
                    )
                    self.playing_embed.set_image(url=self.playing_embed_images[randint(0, len(self.playing_embed_images)-1)])

                    self.vc.play(discord.FFmpegPCMAudio(
                        executable="/usr/bin/ffmpeg",
                        source=self.musics_list[self.music_index]
                    ))
                    self.vc.source = discord.PCMVolumeTransformer(self.vc.source, 0.7)

                    # await ctx.send(f"[-] Reproduzindo: `{self.musics_list[self.music_index]}`")
                    await ctx.send(embed=self.playing_embed)

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

                    self.playing_embed.title = self.get_music_name(self.musics_list[self.music_index].name)
                    self.playing_embed.description = f"`Reproduzindo a {self.music_index+1}° faixa de {len(self.musics_list)} de faixa(s)`"
                    self.playing_embed.set_image(url=self.playing_embed_images[randint(0, len(self.playing_embed_images)-1)])

                    self.vc.stop()
                    self.vc.play(discord.FFmpegPCMAudio(
                        executable="/usr/bin/ffmpeg",
                        source=self.musics_list[self.music_index]
                    ))

                    await ctx.send(embed=self.playing_embed)

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

        embed.set_image(url=self.help_embed_images["helpme"])
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

        embed.set_image(url=self.help_embed_images["list_playlists"])
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

                embed.set_image(url=self.help_embed_images["list_songs"])
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
