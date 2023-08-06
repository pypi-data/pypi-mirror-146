import asyncio
import discord
from discord import Embed, Color
import async_timeout
import wavelink
from discord import ClientException
from discord.ext import commands
from wavelink import (
    LavalinkException,
    LoadTrackError,
    SoundCloudTrack,
    YouTubeMusicTrack,
    YouTubePlaylist,
    YouTubeTrack,
)
from wavelink.ext import spotify
from wavelink.ext.spotify import SpotifyTrack

from ._classes import Provider
from .checks import voice_channel_player, voice_connected
from .errors import MustBeSameChannel
from .paginator import Paginator
from .player import DisPlayer


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.bot.loop.create_task(self.start_nodes())

    def get_nodes(self):
        return sorted(wavelink.NodePool._nodes.values(), key=lambda n: len(n.players))

    async def play_track(self, ctx: commands.Context, query: str, provider=None):
        player: DisPlayer = ctx.voice_client

        if ctx.author.voice.channel.id != player.channel.id:
            raise MustBeSameChannel(
                "You must be in the same voice channel as the player."
            )

        track_providers = {
            "yt": YouTubeTrack,
            "ytpl": YouTubePlaylist,
            "ytmusic": YouTubeMusicTrack,
            "soundcloud": SoundCloudTrack,
            "spotify": SpotifyTrack,
        }


        query = query.strip("<>")
        msg = await ctx.send(f"Searching for `{query}` <:R_:961248893176283146>")

        track_provider = provider if provider else player.track_provider

        if track_provider == "yt" and "playlist" in query:
            provider = "ytpl"

        provider: Provider = (
            track_providers.get(provider)
            if provider
            else track_providers.get(player.track_provider)
        )

        nodes = self.get_nodes()
        tracks = list()

        for node in nodes:
            try:
                with async_timeout.timeout(20):
                    tracks = await provider.search(query, node=node)
                    break
            except asyncio.TimeoutError:
                self.bot.dispatch("dismusic_node_fail", node)
                wavelink.NodePool._nodes.pop(node.identifier)
                continue
            except (LavalinkException, LoadTrackError):
                continue

        if not tracks:
            return await msg.edit("<:loi2:961250273412677652> No Song Or Track Found With Your Link Give")

        if isinstance(tracks, YouTubePlaylist):
            tracks = tracks.tracks
            for track in tracks:
                await player.queue.put(track)
                omg = discord.Embed(color=discord.Color.yellow())
                omg.add_field(name=f'Music Commands !', value=f'Add Song To Queue : `{len(tracks)}`')
                omg.set_image(url=f'https://gifimage.net/wp-content/uploads/2017/10/music-equalizer-gif-7.gif')
            await msg.edit(embed=omg)
        else:
            track = tracks[0]

        embed = discord.Embed(color=discord.Color.green())
        embed.add_field(name=f'Music Commands !', value=f'Add Song To Queue : `{track.title}`')
        embed.set_image(url=f'https://gifimage.net/wp-content/uploads/2017/10/music-equalizer-gif-7.gif')

        await msg.edit(embed=embed)
        await player.queue.put(track)

        if not player.is_playing():
            await player.do_next()

    async def start_nodes(self):
        await self.bot.wait_until_ready()
        spotify_credential = getattr(
            self.bot, "spotify_credentials", {"client_id": "", "client_secret": ""}
        )

        for config in self.bot.lavalink_nodes:
            try:
                node: wavelink.Node = await wavelink.NodePool.create_node(
                    bot=self.bot,
                    **config,
                    spotify_client=spotify.SpotifyClient(**spotify_credential),
                )
                print(f"[Lkinght Music] INFO - Created node: {node.identifier}")
            except Exception:
                print(
                    f"[Lkinght Music] ERROR - Failed to create node {config['host']}:{config['port']}"
                )

    @commands.command(aliases=["con"])
    @voice_connected()
    async def connect(self, ctx: commands.Context):
        if ctx.voice_client:
            return

        embed = discord.Embed(color=discord.Color.green())
        embed.add_field(name=f'Music Commands !', value=f'Connecting To `{ctx.author.voice.channel}`')
        embed.set_image(url=f'https://cdn.discordapp.com/avatars/742672021422342165/d26bfcf7495aada8ed9294d49933eb6a.png')

        msg = await ctx.send(embed=embed)

        try:
            player: DisPlayer = await ctx.author.voice.channel.connect(cls=DisPlayer)
            self.bot.dispatch("dismusic_player_connect", player)
        except (asyncio.TimeoutError, ClientException):
            return await msg.edit(content="Failed to connect to voice channel.")

        player.bound_channel = ctx.channel
        player.bot = self.bot
        abc = discord.Embed(color=discord.Color.green())
        abc.add_field(name=f'Music Commands !', value=f'Connected To `{ctx.author.voice.channel}`')
        abc.set_image(url=f'https://cdn.discordapp.com/avatars/742672021422342165/d26bfcf7495aada8ed9294d49933eb6a.png')
        await msg.edit(embed=abc)

    @commands.group(aliases=["p"], invoke_without_command=True)
    @voice_connected()
    async def play(self, ctx: commands.Context, *, query: str):
        await ctx.invoke(self.connect)
        await self.play_track(ctx, query)

    @play.command(aliases=["yt"])
    @voice_connected()
    async def youtube(self, ctx: commands.Context, *, query: str):
        await ctx.invoke(self.connect)
        await self.play_track(ctx, query, "yt")

    @play.command(aliases=["ytmusic"])
    @voice_connected()
    async def youtubemusic(self, ctx: commands.Context, *, query: str):
        await ctx.invoke(self.connect)
        await self.play_track(ctx, query, "ytmusic")

    @play.command(aliases=["sc"])
    @voice_connected()
    async def soundcloud(self, ctx: commands.Context, *, query: str):
        await ctx.invoke(self.connect)
        await self.play_track(ctx, query, "soundcloud")

    @play.command(aliases=["sp"])
    @voice_connected()
    async def spotify(self, ctx: commands.Context, *, query: str):
        await ctx.invoke(self.connect)
        await self.play_track(ctx, query, "spotify")

    @commands.command(aliases=["vol"])
    @voice_channel_player()
    async def volume(self, ctx: commands.Context, vol: int, forced=False):
        player: DisPlayer = ctx.voice_client
        if vol < 0:
            return await ctx.send("⛔ | Volume Can't Be Less Than 0 ")

        if vol > 100 and not forced:
            return await ctx.send("⛔ | Volume Can't Greater Than 100")

        await player.set_volume(vol)
        await ctx.send(f"✅ | Volume Set To {vol} :loud_sound:")
        


    @commands.command(aliases=["disconnect", "dc"])
    @voice_channel_player()
    async def stop(self, ctx: commands.Context):
        player: DisPlayer = ctx.voice_client

        await player.destroy()

        tcm = discord.Embed(color=discord.Color.red())
        tcm.add_field(name=f'Music Commands !', value=f'Stop Play Music At `{ctx.author.voice.channel}`')
        tcm.set_image(url=f'https://th.bing.com/th/id/R.205a21c7900450742895142f5c1dbd72?rik=04APERZMDhombw&pid=ImgRaw&r=0')
        await ctx.send(embed=tcm)
        self.bot.dispatch("dismusic_player_stop", player)

    @commands.command()
    @voice_channel_player()
    async def pause(self, ctx: commands.Context):
        player: DisPlayer = ctx.voice_client

        if player.is_playing():
            if player.is_paused():
                return await ctx.send("❌ | Player is already paused.")

            await player.set_pause(pause=True)
            self.bot.dispatch("dismusic_player_pause", player)
            uml = discord.Embed(color=discord.Color.red())
            uml.add_field(name=f'Music Commands !', value=f'Pause Music At `{ctx.author.voice.channel}`')
            uml.set_image(url=f'https://th.bing.com/th/id/R.42bd92c08b3bab7a6841d60f921c9e0e?rik=98utNBGLb2F6cQ&pid=ImgRaw&r=0')
            return await ctx.send(embed=uml)

        await ctx.send("Player is not playing anything.")

    @commands.command()
    @voice_channel_player()
    async def resume(self, ctx: commands.Context):
        player: DisPlayer = ctx.voice_client

        if player.is_playing():
            if not player.is_paused():
                return await ctx.send("Player is already playing.")

            await player.set_pause(pause=False)
            self.bot.dispatch("dismusic_player_resume", player)
            return await ctx.send("Resumed :musical_note: ")

        await ctx.send("Player is not playing anything.")

    @commands.command()
    @voice_channel_player()
    async def skip(self, ctx: commands.Context):
        player: DisPlayer = ctx.voice_client

        if player.loop == "CURRENT":
            player.loop = "NONE"

        await player.stop()

        self.bot.dispatch("dismusic_track_skip", player)
        await ctx.send("Skipped :track_next:")

    @commands.command()
    @voice_channel_player()
    async def loop(self, ctx: commands.Context, loop_type: str = None):
        player: DisPlayer = ctx.voice_client

        result = await player.set_loop(loop_type)
        await ctx.send(f"Loop has been set to {result} :repeat: ")

    @commands.command(aliases=["q"])
    @voice_channel_player()
    async def queue(self, ctx: commands.Context):
        player: DisPlayer = ctx.voice_client

        if len(player.queue._queue) < 1:
            omgo = discord.Embed(color=discord.Color.red())
            omgo.add_field(name=f'Music Commands !', value=f'Nothing In Queue `{ctx.author}`')
            omgo.set_image(url=f'https://th.bing.com/th/id/R.42bd92c08b3bab7a6841d60f921c9e0e?rik=98utNBGLb2F6cQ&pid=ImgRaw&r=0')
            return await ctx.send(embed=omgo)

        paginator = Paginator(ctx, player)
        await paginator.start()

    @commands.command(aliases=["np"])
    @voice_channel_player()
    async def nowplaying(self, ctx: commands.Context):
        player: DisPlayer = ctx.voice_client
        await player.invoke_player(ctx)
