from __future__ import annotations
from twitchio import ChannelInfo, PartialUser
from twitchio.ext import commands, pubsub, routines
import functools
import random
import asyncio
import typer
from .config import *
from .core import FutureTone, NoteDef, Note, NoteType, NoteModifier
from ps4debug import PS4Debug


# Create a config section [spawnpools] for this where name=button:weight, button2:weight2, .... are the key-value pairs.
spawn_pools = {
    SpawnPoolValues.full: Note.default_pool,
    SpawnPoolValues.no_sliders: [
        (NoteType.Triangle, 7),
        (NoteType.Triangle2, 6),
        (NoteType.TriangleHold, 6),

        (NoteType.Circle, 7),
        (NoteType.Circle2, 6),
        (NoteType.CircleHold, 6),

        (NoteType.Square, 7),
        (NoteType.Square2, 6),
        (NoteType.SquareHold, 6),

        (NoteType.Cross, 7),
        (NoteType.Cross2, 6),
        (NoteType.CrossHold, 6),
    ],
    SpawnPoolValues.no_holds: [
        (NoteType.Triangle, 7),
        (NoteType.Triangle2, 6),

        (NoteType.Circle, 7),
        (NoteType.Circle2, 6),

        (NoteType.Square, 7),
        (NoteType.Square2, 6),

        (NoteType.Cross, 7),
        (NoteType.Cross2, 6),

        (NoteType.SlideL, 5),
        (NoteType.SlideR, 5),
        (NoteType.SlideLPart, 4),
        (NoteType.SlideRPart, 4),
        (NoteType.RainbowSliderL, 3),
        (NoteType.SliderR2, 3),
    ],
    SpawnPoolValues.only_regular: [
        (NoteType.Triangle, 7),
        (NoteType.Triangle2, 6),
        (NoteType.Circle, 7),
        (NoteType.Circle2, 6),
        (NoteType.Square, 7),
        (NoteType.Square2, 6),
        (NoteType.Cross, 7),
        (NoteType.Cross2, 6),
    ]
}


def requires_mod(exempt: list[str]):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            bot, ctx = args
            if ctx.author.is_mod or ctx.author.name in exempt:
                return await func(*args, **kwargs)
            typer.secho(f'{ctx.author.name} tried to invoke {ctx.command.name}', fg='red')

        return wrapper

    return decorator


@routines.routine(seconds=1.0)
async def spawner(bot: FutureToneIntegrationBot):
    if len(bot.spawn_queue) == 0:
        return

    next_note, user = bot.spawn_queue.pop(0)

    subs = await bot.channel_info.user.fetch_subscriptions(bot.config.global_.access_token)
    is_subscriber = user.id in {e.user.id for e in subs}

    if is_subscriber:
        old_melody_icons = await bot.ft.get_melody_icon_settings()
        if old_melody_icons != 4:
            await bot.ft.set_melody_icon_settings(4)
            rax = await bot.ft.spawn_note(next_note)
            await bot.ft.set_melody_icon_settings(old_melody_icons)
        else:
            rax = await bot.ft.spawn_note(next_note)
    else:
        rax = await bot.ft.spawn_note(next_note)

    if rax is not None and rax > 0:
        if bot.config.global_.verbose:
            typer.echo(f'Spawned note {typer.style(next_note, fg="green")} '
                       f'(rax = {typer.style(hex(rax), fg="yellow")})')
    else:
        if bot.config.global_.verbose:
            typer.echo(f'Could not spawn {typer.style(next_note, fg="red")}. Re-queueing...')
        bot.spawn_queue.append((next_note, user))


class FutureToneIntegrationBot(commands.Bot):
    ft: FutureTone
    channel_info: ChannelInfo
    spawn_queue: list[tuple[NoteDef, PartialUser]]
    spawner: asyncio.Task
    redemptions: dict[str, tuple[CommandSettings, ...]]

    def __init__(self, config: Settings):
        super(FutureToneIntegrationBot, self).__init__(
            token=config.global_.bot_token,
            initial_channels=[config.global_.channel],
            prefix=config.global_.prefix
        )

        self.config = config
        self.pubsub = pubsub.PubSubPool(self)
        self.spawner = spawner.start(self)
        self.spawn_queue = []

        self.note_modifier_lock = asyncio.Lock()
        self.score_invalidation_lock = asyncio.Lock()
        self.slow_note_lock = asyncio.Lock()

    async def bind(self):
        ps4 = PS4Debug(self.config.global_.ip)

        if self.config.global_.verbose:
            typer.echo(f'Connected to {typer.style(ps4.pool.host, fg="green")}')

        processes = await ps4.get_processes()
        if self.config.global_.verbose:
            typer.echo(f'Retrieved {typer.style(len(processes), fg="green")} processes')

        pid = next((p.pid for p in processes if p.name == 'eboot.bin'), None)
        if not pid:
            raise Exception('No eboot.bin loaded')
        if self.config.global_.verbose:
            typer.echo(f'eboot.bin found (id: {typer.style(pid, fg="green")})')

        process_info = await ps4.get_process_info(pid)
        title_id = self.config.global_.title_id
        if process_info.title_id != title_id:
            raise Exception(f'Wrong game running. Expected: {title_id}, got: {process_info.title_id}')
        if self.config.global_.verbose:
            typer.echo(f'Game found [{typer.style(title_id, fg="green")}]')

        base_address = await FutureTone.get_base_address(ps4, pid)
        if self.config.global_.verbose:
            typer.echo(f'Retrieved base address: {typer.style(hex(base_address), fg="green")}')

        rpc_stub = await ps4.find_rpc(pid, start=0x4000, end=0x40000, step=0x4000) or \
            await ps4.install_rpc(pid)
        if self.config.global_.verbose:
            typer.echo(f'Successfully injected RPC-stub at {typer.style(hex(rpc_stub), fg="green")}')

        self.ft = FutureTone(ps4, pid, base_address)

    async def event_ready(self):
        if self.config.global_.verbose:
            typer.echo(f'Logged in as | {typer.style(self.nick, fg="green")}')
            typer.echo(f'User id is | {typer.style(self.user_id, fg="green")}')

        await self.subscribe_topics(
            pubsub.channel_points,
            pubsub.bits,
        )
        self.channel_info = await self.fetch_channel(self.config.global_.channel)

        if self.config.global_.verbose:
            typer.echo('Trying to connect to the PlayStation 4...')
        await self.bind()

        if self.config.global_.verbose:
            typer.echo('Applying configuration to the game...')
        await self.apply_config(self.config)

        typer.secho('Ready!', fg='green')
        typer.echo('If this is your first time using this, please refer to "https://rentry.co/mikuslow_strimer"')
        await self.get_channel(self.config.global_.channel).send('Ready!')

    async def subscribe_topics(self, *topics):
        channel = await self.fetch_channel(self.config.global_.channel)
        token = self.config.global_.access_token
        id_ = channel.user.id
        await self.pubsub.subscribe_topics([topic(token)[id_] for topic in topics])

    async def apply_config(self, config: Settings):
        await self.ft.set_max_life(config.game.max_life)
        await self.ft.set_starting_life(config.game.start_life)

        if config.game.disable_lyrics:
            await self.ft.disable_lyrics(clear=True)
        else:
            await self.ft.enable_lyrics(clear=False)

        await self.ft.set_max_volume(config.game.max_volume)

        if config.game.unpatch_holds:
            await self.ft.disable_hold_invalidation()
        else:
            await self.ft.enable_hold_invalidation()

        if config.game.unpatch_calibration:
            await self.ft.disable_score_invalidation()
            await self.ft.set_score_valid(True)
        else:
            await self.ft.enable_score_invalidation()

        # Redemption LUT
        self.redemptions = {
            config.spawn_random.title: (config.spawn_random, self.redeem_spawn_random),
            config.spawn.title: (config.spawn, self.redeem_spawn),
            config.kill.title: (config.kill, self.redeem_kill),
            config.harm.title: (config.harm, self.redeem_harm),
            config.heal.title: (config.heal, self.redeem_heal),
            config.invincibility.title: (config.invincibility, self.redeem_invincibility),
            config.change_calibration.title: (config.change_calibration, self.redeem_change_calibration),
            config.sudden_modifier.title: (config.sudden_modifier, self.redeem_sudden_modifier),
            config.hidden_modifier.title: (config.hidden_modifier, self.redeem_hidden_modifier),
            config.highlight.title: (config.highlight, self.redeem_highlight),
            config.invalidate_score.title: (config.invalidate_score, self.redeem_invalidate_score),
            config.enable_slow.title: (config.enable_slow, self.redeem_enable_slow),
        }

    async def event_pubsub_channel_points(self, event: pubsub.PubSubChannelPointsMessage):
        if event.status != 'UNFULFILLED' or event.reward.paused:
            return

        for title in self.redemptions:
            config, callback = self.redemptions[title]
            if not config.enabled or callback is None:
                continue

            if event.reward.title == title:
                if self.config.global_.verbose:
                    typer.echo(f'{typer.style(event.user.name, fg="green")} redeemed '
                               f'"{typer.style(event.reward.title, fg="green")}"')
                await callback(event, config)
                if config.notify:
                    await self.ft.ps4debug.notify(f'{event.user.name} redeemed {event.reward.title}')

    async def event_pubsub_bits(self, event: pubsub.PubSubBitsMessage):
        vp = await self.ft.get_vp()
        self.ft.set_vp(vp + event.bits_used)

    async def create_rewards(self):
        raise NotImplementedError()

    async def redeem_spawn_random(self, event: pubsub.PubSubChannelPointsMessage, config: SpawnRandomSettings):
        note = NoteDef.random(min=config.min_, max=config.max_,
                              pool=spawn_pools[config.pool], duplicates=config.allow_duplicates)

        if self.config.global_.verbose:
            typer.echo(f'  Generated note: {typer.style(note, fg="green")}')

        self.spawn_queue.append((note, event.user))

    async def redeem_spawn(self, event: pubsub.PubSubChannelPointsMessage, config: SpawnSettings):
        note_def = None
        notes = []

        parts = event.input.split(' ')
        if len(parts) > 4 and self.config.global_.verbose:
            typer.secho(f'{event.user.name} tried to spawn more than 4 notes. Using only the first 4.', fg='yellow')
            parts = parts[0:4]

        note_dict = config.dict(exclude={'enabled', 'title', 'description', 'notify', 'exclude', 'allow_random'})

        for in_ in parts:
            in_ = in_.lower()

            for type_ in note_dict:
                print(type_)
                type_ = next(x for x in NoteType if x.name == type_)

                if type_.name.lower() in config.exclude:
                    if self.config.global_.verbose:
                        typer.echo(f'  Note type {typer.style(type_.name, fg="yellow")} is excluded. Skipping..')
                    continue

                if in_ == '...' and config.allow_random:
                    notes.append(Note.random())
                    break

                if in_ in note_dict[type_.name]:
                    notes.append(Note(type_, Note.random_pos()))
                    break

        if len(notes) > 0:
            note_def = NoteDef(*notes)

        if note_def is not None:
            self.spawn_queue.append((note_def, event.user))
            if self.config.global_.verbose:
                typer.echo(f'  Created note: {typer.style(note_def, fg="green")}')

    async def redeem_kill(self, event: pubsub.PubSubChannelPointsMessage, _):
        await self.ft.set_life(0)
        if self.config.global_.verbose:
            typer.echo(f'  {typer.style(event.user.name, fg="red")} killed you :\'(')

    async def redeem_harm(self, event: pubsub.PubSubChannelPointsMessage, config: HarmSettings):
        life = await self.ft.get_life()
        min_life = 0 if config.can_kill else 1
        life = max(life - config.damage, min_life)
        await self.ft.set_life(life)
        if self.config.global_.verbose:
            typer.echo(f'  {typer.style(event.user.name, fg="red")} harmed you :(')

    async def redeem_heal(self, event: pubsub.PubSubChannelPointsMessage, config: HealSettings):
        if config.full:
            await self.ft.set_life(await self.ft.get_max_life())
        else:
            life = await self.ft.get_life()
            max_life = await self.ft.get_max_life()
            life = min(life + config.life, max_life)
            await self.ft.set_life(life)

        if self.config.global_.verbose:
            typer.echo(f'  {typer.style(event.user.name, fg="bright_green")} healed you :)')

    async def redeem_invincibility(self, event: pubsub.PubSubChannelPointsMessage, config: DurationSettings):
        # TODO sophisticate
        off = b'\x90\x90\x90\x90\x90\x90\x90\x90\x90\xEB'
        on = b'\x41\x83\xBC\x24\xB4\xD1\x02\x00\x00\x7F'
        await self.ft.ps4debug.write_memory(self.ft.pid, self.ft.base + 0x70B447, off)

        if self.config.global_.verbose:
            typer.echo(f'  {typer.style(event.user.name, fg="green")} gave you '
                       f'invincibility for {config.duration} seconds.')

        await asyncio.sleep(config.duration)
        await self.ft.ps4debug.write_memory(self.ft.pid, self.ft.base + 0x70B447, on)

    async def redeem_change_calibration(self, event: pubsub.PubSubChannelPointsMessage,
                                        config: ChangeCalibrationSettings):
        calibration = await self.ft.get_calibration_shared()
        delta = random.randint(1, 2 * config.range_) - config.range_
        await self.ft.set_calibration_shared(calibration + delta)

        if self.config.global_.verbose:
            typer.echo(f'  {typer.style(event.user.name, fg="yellow")} messed your calibration up by {delta} '
                       f'for {config.duration} seconds.')

        await asyncio.sleep(config.duration)
        calibration = await self.ft.get_calibration_shared()
        await self.ft.set_calibration_shared(calibration - delta)

    async def redeem_sudden_modifier(self, event: pubsub.PubSubChannelPointsMessage, config: DurationSettings):
        await self.note_modifier_lock.acquire()
        await self.ft.set_note_modifier(NoteModifier.SUDDEN)

        if self.config.global_.verbose:
            typer.echo(f'  {typer.style(event.user.name, fg="red")} activated {NoteModifier.SUDDEN.name} '
                       f'for {config.duration} seconds.')

        if config.duration > 0:
            await asyncio.sleep(config.duration)
            await self.ft.set_note_modifier(NoteModifier.Normal)
        self.note_modifier_lock.release()

    async def redeem_hidden_modifier(self, event: pubsub.PubSubChannelPointsMessage, config: DurationSettings):
        await self.note_modifier_lock.acquire()
        await self.ft.set_note_modifier(NoteModifier.HIDDEN)

        if self.config.global_.verbose:
            typer.echo(f'  {typer.style(event.user.name, fg="red")} activated {NoteModifier.HIDDEN.name} '
                       f'for {config.duration} seconds.')

        if config.duration > 0:
            await asyncio.sleep(config.duration)
            await self.ft.set_note_modifier(NoteModifier.Normal)
        self.note_modifier_lock.release()

    async def redeem_highlight(self, event: pubsub.PubSubChannelPointsMessage, _):
        if self.config.global_.verbose:
            typer.echo(f'  {typer.style(event.user.name, fg="green")} redeemed highlighting in the lyrics:')
            typer.secho(f' {event.input}', fg='green')

        message = event.input
        if len(message) > 75:
            message = message[:72] + '...'

        await self.ft.set_lyrics(message)
        await self.ft.set_lyrics_visible(True)

    async def redeem_invalidate_score(self, event: pubsub.PubSubChannelPointsMessage, config: DurationSettings):
        await self.score_invalidation_lock.acquire()
        await self.ft.set_score_valid(False)

        if self.config.global_.verbose:
            typer.echo(f'  {typer.style(event.user.name, fg="red")} invalidated the score '
                       f'for {config.duration} seconds.')

        await asyncio.sleep(config.duration)
        await self.ft.set_score_valid(True)
        self.score_invalidation_lock.release()

    async def redeem_enable_slow(self, event: pubsub.PubSubChannelPointsMessage, config: DurationSettings):
        await self.slow_note_lock.acquire()
        old_icons = await self.ft.get_melody_icon_settings()
        await self.ft.set_melody_icon_settings(4)

        if self.config.global_.verbose:
            typer.echo(f'  {typer.style(event.user.name, fg="blue")} enabled stoichSlow notes '
                       f'for {config.duration} seconds.')

        await asyncio.sleep(config.duration)
        await self.ft.set_melody_icon_settings(old_icons)
        self.slow_note_lock.release()

    @commands.command(aliases=['h'])
    async def help(self, ctx: commands.Context):
        """Displays information and help about commands."""
        # if ctx.author.name == self.channel_name:
        #    await ctx.send(f'You don\'t need help. Kappa')
        #    return

        if len(ctx.view.words) > 0:
            name = ctx.view.words[1]
            matching = next((c for k, c in self.commands.items() if name == k or
                             (c.aliases is not None and name in c.aliases)), None)

            if matching is None:
                await ctx.reply(f'No command "{name}"')
                return

            docstring = matching._callback.__doc__
            await ctx.reply(f'!{name} - {docstring or "No help text specified. Sorry."}')
            return

        await ctx.send('I am machine. I have no feelings. However, I do things in Future Tone. '
                       'Use !help <command> for more information. '
                       'You may also check out "https://rentry.co/mikuslow_chat"')

    @commands.command(aliases=['stop', 'leave', 'exit', 'q'])
    @requires_mod(exempt=['0jay0'])
    async def quit(self, ctx: commands.Context):
        """Cleanly shuts the bot down. Mods only."""
        if self.config.global_.verbose:
            typer.echo(f'Bot disconnected by {typer.style(ctx.author.name, fg="green")}')

        self.spawner.cancel()
        await ctx.reply('Bye!')
        await self.close()

    @commands.command(name='showcommands', aliases=['commands'])
    async def show_commands(self, ctx: commands.Context):
        """Shows a list of all commands."""
        if len(ctx.view.words) > 0 and ctx.view.words[1].lower() == 'all':
            await ctx.reply(', '.join([
                ', '.join([f'!{k}'] + ([] if c.aliases is None else [f'!{a}' for a in c.aliases]))
                for k, c in self.commands.items()
            ]))
        else:
            await ctx.reply(', '.join([f'!{k}' for k in self.commands]))

    @commands.command(name='loadconfig', aliases=['loadconf', 'reloadconf', 'reloadconfig'])
    @requires_mod(exempt=['0jay0'])
    async def reload_config(self, ctx: commands.Context):
        """Reloads a configuration file. 'config.ini' is used when no file is provided."""
        file_path = 'config.ini'

        if len(ctx.view.words) > 0:
            file_path = ctx.view.words[1]

        try:
            settings = get_config(file_path)
            await self.apply_config(settings)
            self.config = settings
            await ctx.reply('Configuration loaded!')
            typer.echo(f'Configuration "{typer.style(file_path, fg="green")}" loaded by '
                       f'{typer.style(ctx.author.display_name, fg="green")}')
        except FileNotFoundError as ex:
            await ctx.reply('File does not exist.')
            typer.echo(ex, err=True)
        except ValidationError as ex:
            await ctx.reply('There are some errors in the configuration file.')
            typer.echo(ex, err=True)

    @commands.command()
    async def laundry(self, ctx: commands.Context):
        """Time to do laundry."""
        await ctx.send('LaundryBasket')

    @commands.command(aliases=['bobbas'])
    async def boobas(self, ctx: commands.Context):
        await ctx.send('(.)(.)')

    @commands.command()
    @requires_mod(exempt=['0jay0'])
    async def volume(self, ctx: commands.Context):
        """Sets the game audio settings. Use !volume (music|button|sound) (number) to set a specific setting."""
        args = list(ctx.view.words.values())

        if len(args) < 1:
            await ctx.reply('Please provide a setting or a number from 0 to 100.')

        track = None

        if len(args) > 1:
            track = args[-2]

        volume = args[-1]
        try:
            volume = int(volume) / 100
        except ValueError as ex:
            if self.config.global_.verbose:
                typer.echo(ex, err=True)
            await ctx.reply('Please provide a setting or a number from 0 to 100.')

        if 0 <= volume <= 1:
            if track is None or track.lower() in {'music', 'm'}:
                await self.ft.set_music_volume(volume)
            if track is None or track.lower() in {'button', 'b'}:
                await self.ft.set_buttonfx_volume(volume)
            if track is None or track.lower() in {'sound', 's'}:
                await self.ft.set_soundfx_volume(volume)
        else:
            await ctx.reply('Please provide a number from 0 to 100.')

    @commands.command()
    @requires_mod(exempt=['0jay0'])
    async def calibration(self, ctx: commands.Context):
        """Set your timing calibration. Usage: !calibration (song|shared) (number)."""
        args = list(ctx.view.words.values())

        if len(args) < 2:
            await ctx.reply('Provide either "song" or "shared" and a number. Like so "!calibration shared -4"')
            return

        try:
            value = int(args[1])
        except ValueError:
            await ctx.reply('Provide number. Like so "!calibration shared -4"')
            return

        if args[0].lower() == 'shared':
            await self.ft.set_calibration_shared(value)
        elif args[0].lower() == 'song':
            await self.ft.set_calibration_song(value)

    @commands.command(name='songname', aliases=['currentsong'])
    async def song_name(self, ctx: commands.Context):
        """Displays currently playing song."""
        name = await self.ft.get_song_name()
        await ctx.reply(f'Currently playing "{name}".')

    @commands.command(aliases=['kill', 'killme', 'kms'])
    @requires_mod(exempt=['0jay0'])
    async def die(self, ctx: commands.Context):
        """Kills the player."""
        await self.ft.set_life(0)
        await ctx.send(f'{self.config.global_.channel} couldn\'t take it anymore PoroSad')

    @commands.command()
    @requires_mod(exempt=['0jay0'])
    async def harm(self, ctx: commands.Context):
        """Takes 10 life away from the player. Will never kill the player."""
        life = await self.ft.get_life()
        await self.ft.set_life(min(life - 10, 1))

    @commands.command()
    @requires_mod(exempt=['0jay0'])
    async def heal(self, ctx: commands.Context):
        """Fills up the lifebar."""
        await self.ft.set_life(255)

    @commands.command(name='disablenotes')
    @requires_mod(exempt=['0jay0'])
    async def disable_notes(self, ctx: commands.Context):
        """Disables the spawning of the chart's notes."""
        await self.ft.disable_note_spawning()

    @commands.command(name='enablenotes')
    @requires_mod(exempt=['0jay0'])
    async def enable_notes(self, ctx: commands.Context):
        """Enables the spawning of the chart's notes."""
        await self.ft.enable_note_spawning()

    @commands.command(name='playmusic')
    @requires_mod(exempt=['0jay0'])
    async def play_music(self, ctx: commands.Context):
        """Plays an audio file. Make sure the filepath is in the game. Example: !playmusic rom/sound/song/pv_270.ogg"""
        args = list(ctx.view.words.values())
        if not len(args):
            await ctx.reply('Please provide a file path.')

        await self.ft.play_music(args[0])

    @commands.command(name='spawnrandom')
    @requires_mod(exempt=['0jay0'])
    async def spawn_random(self, ctx: commands.Context):
        """Spawns a random note."""
        await self.ft.spawn_note(NoteDef.random())

    @commands.command(name='crashthegame')
    @requires_mod(exempt=['0jay0'])
    async def dont_do_this(self, ctx: commands.Context):
        """Really, don't."""
        note_types = list(NoteType)
        note_types = {t.value: random.choice(note_types) for t in note_types}

        print(note_types)

        size = await self.ft.get_chart_size()
        while not size:
            await asyncio.sleep(0.5)
            size = await self.ft.get_chart_size()

        typer.echo('Starting...')
        for i in range(size):
            note_def = await self.ft.get_chart_note(i)
            for note in note_def.notes:
                note.button = note_types[note.button.value]
            await self.ft.set_chart_note(i, note_def)
            typer.echo(f'{i}/{size}')
        typer.echo('Done...')
