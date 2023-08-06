from __future__ import annotations
from typing import NamedTuple, Dict
import ps4debug
import enum
import random
import struct
import asyncio


class DifficultyType(enum.IntEnum):
    EASY = 0
    NORMAL = 1
    HARD = 2
    EXTREME = 3
    EXTRA_EXTREME = 4


class NoteType(enum.IntEnum):
    Triangle = 0
    Circle = 1
    Cross = 2
    Square = 3
    TriangleHold = 4
    CircleHold = 5
    CrossHold = 6
    SquareHold = 7
    # Invalid = 8
    # Invalid2 = 9
    # Invalid3 = 10
    SlideL = 12
    SlideR = 13
    SlideLPart = 15
    SlideRPart = 16
    # Invalid4 = 17
    Triangle2 = 18
    Circle2 = 19
    Cross2 = 20
    Square2 = 21
    RainbowSliderL = 23
    SliderR2 = 24
    # Invalid from here on out


class ButtonConfigType(enum.IntEnum):
    Triangle = 0
    Square = 1
    Cross = 2
    Circle = 3
    SliderL = 4
    SliderR = 5
    SliderLAlt = 6
    SliderRAlt = 7
    TriangleSquare = 8
    TriangleCross = 9
    TriangleCircle = 10
    SquareCross = 11
    SquareCircle = 12
    CrossCircle = 13
    TriangleSquareCross = 14
    TriangleSquareCircle = 15
    TriangleCrossCircle = 16
    SquareCrossCircle = 17
    TriangleSquareCrossCircle = 18
    NoSetting = 19


class ControlSchemaFlags(enum.IntFlag):
    Circle = 0x0100
    Cross = 0x0200
    Triangle = 0x0400
    Square = 0x0800
    RStickFlick = 0xF0FF

    RStickLeft = 0x0F0000
    Up = 0x100000
    Down = 0x200000
    Left = 0x400000
    Right = 0x800000

    L1 = 0x01000000
    R1 = 0x02000000
    L2 = 0x04000000
    R2 = 0x08000000
    LStickLeft = 0xF0000000


class Note(object):
    default_pool = [
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

        (NoteType.SlideL, 5),
        (NoteType.SlideR, 5),
        (NoteType.SlideLPart, 4),
        (NoteType.SlideRPart, 4),
        (NoteType.RainbowSliderL, 3),
        (NoteType.SliderR2, 3),
    ]

    def __init__(self, button=None, pos=None, start=None, wobble=None, *reserved):
        super(Note, self).__init__()
        self.button = button or NoteType.Triangle
        self.pos = pos or (0, 0)
        self.start = start or (0, 0)
        self.wobble = wobble or 0.5
        self.reserved = reserved or [0, 0, 0]
        assert len(self.reserved) == 3

    @classmethod
    def random(cls, **kwargs):
        max_width = 480
        max_height = 272

        pool = kwargs.get('pool', Note.default_pool)
        start_region = kwargs.get('start_region', (-100, -100, max_width + 100, max_height + 100))
        wobble_enabled = kwargs.get('wobble_enable', True)
        wobble_range = kwargs.get('wobble_range', (-1.0, 1.0))
        wobble_random = random.random() * (wobble_range[1] - wobble_range[0]) + wobble_range[0]

        notes, weights = zip(*pool)
        button = random.choices(notes, weights)[0]
        pos = cls.random_pos(**kwargs)
        start_x = float(random.randint(start_region[0], start_region[2]))
        start_y = float(random.randint(start_region[1], start_region[3]))
        wobble = wobble_random if wobble_enabled else 0.5
        return Note(button, pos, (start_x, start_y), wobble)

    @classmethod
    def random_pos(cls, **kwargs):
        max_width = 480
        max_height = 272
        region = kwargs.get('region', (0, 0, max_width, max_height))

        position_x = float(random.randint(region[0], region[2]))
        position_y = float(random.randint(region[1], region[3]))

        return position_x, position_y

    def __str__(self):
        return self.button.name if isinstance(self.button, NoteType) else str(self.button)

    def __repr__(self):
        return f'{self.button!r} @ {self.pos} from {self.start}'


class NoteDef(object):
    def __init__(self, *notes):
        super(NoteDef, self).__init__()
        self.notes = notes
        assert 0 < len(self.notes) <= 4
        self.__struct = struct.Struct('<I144x28x')
        self.__struct_note = struct.Struct('<I5fiII')
        assert self.__struct.size == 0xB0
        assert self.__struct_note.size == 0x24

    def to_bytes(self):
        count = len(self.notes)
        buffer = bytearray(self.__struct.size)
        self.__struct.pack_into(buffer, 0, count)

        for i, note in enumerate(self.notes):
            self.__struct_note.pack_into(buffer, 4 + i * self.__struct_note.size,
                                         note.button if isinstance(note.button, int) else note.button.value,
                                         *note.pos,
                                         *note.start,
                                         note.wobble,
                                         *note.reserved)

        return buffer

    @staticmethod
    def from_bytes(bytearray_):
        count = int.from_bytes(bytearray_[:4], 'little')

        struct_note = struct.Struct('<I5fiII')
        assert struct_note.size == 0x24
        notes = []

        for i in range(count):
            data = struct_note.unpack_from(bytearray_, 4 + struct_note.size * i)
            button, pos_x, pos_y, start_x, start_y, wobble, *res = data

            button = next((e for e in NoteType if button == e.value), NoteType.Triangle)
            notes.append(Note(button, (pos_x, pos_y), (start_x, start_y), wobble, *res))

        return NoteDef(*notes)

    @classmethod
    def random(cls, **kwargs):
        min_ = min(max(kwargs.pop('min') or 1, 1), 4)
        max_ = max(min(kwargs.pop('max') or 1, 4), 1)
        duplicates = kwargs.pop('duplicates') or True

        buttons = random.choices(range(min_, max_ + 1), [i * 0.25 for i in range(min_, max_ + 1)][::-1])[0]
        notes = []
        while len(notes) < buttons:
            note = Note.random(**kwargs)
            if not duplicates and any(n.button == note.button for n in notes):
                continue
            notes.append(note)

        return NoteDef(*notes)

    def __str__(self):
        return '+'.join([str(note) for note in self.notes])

    def __repr__(self):
        return '+'.join([repr(note) for note in self.notes])


class NoteResultType(enum.IntEnum):
    Cool = 0
    Fine = 1
    Safe = 2
    Bad = 3
    CoolWrong = 4
    FineWrong = 5
    SafeWrong = 6
    BadWrong = 7
    Miss = 8
    CoolDouble = 9
    FineDouble = 10
    SafeDouble = 11
    BadDouble = 12
    CoolTriple = 13
    FineTriple = 14
    SafeTriple = 15
    BadTriple = 16
    CoolQuad = 17
    FineQuad = 18
    SafeQuad = 19
    BadQuad = 20


class ScoreResult(enum.IntEnum):
    COOL = 0
    FINE = 1
    SAFE = 2
    BAD = 3
    MISS = 4


class ScoreDefinition(NamedTuple):
    score: int
    keep_combo: bool
    result: ScoreResult
    reserved: int
    reserved2: int


class NoteModifier(enum.IntEnum):
    Normal = 0
    HIDDEN = 2
    SUDDEN = 3


class FutureTone(object):
    def __init__(self, ps4: ps4debug.PS4Debug, pid, base_address):
        self.ps4debug = ps4
        self.pid = pid
        self.base = base_address

    @classmethod
    async def bind(cls, ps4: ps4debug.PS4Debug) -> FutureTone | None:
        processes = await ps4.get_processes()
        pid = next((p.pid for p in processes if p.name == 'eboot.bin'), None)

        if not pid:
            return None

        process_info = await ps4.get_process_info(pid)
        base_address = await cls.get_base_address(ps4, pid)

        assert process_info.title_id == 'CUSA06211'
        return FutureTone(ps4, pid, base_address)

    @classmethod
    async def get_base_address(cls, ps4: ps4debug.PS4Debug, pid: int):
        maps = await ps4.get_process_maps(pid)
        base_address = next(map_.start for map_ in maps if map_.name == 'executable')
        return base_address

    async def get_score_definitions(self) -> Dict[NoteResultType, ScoreDefinition]:
        definitions = {}
        structure = struct.Struct('<5I')
        types_ = list(NoteResultType)

        for i, type_ in enumerate(types_):
            data = await self.ps4debug.read_struct(self.pid, self.base + 0x8ACE30 + i * structure.size, structure)
            definitions[type_] = ScoreDefinition(*data)

        return definitions

    async def get_score_definition(self, type_: NoteResultType) -> ScoreDefinition:
        definitions = await self.get_score_definitions()
        return definitions[type_]

    async def set_score_definitions(self, *score_definitions: ScoreDefinition):
        structure = struct.Struct('<5I')
        types_ = list(NoteResultType)

        assert len(score_definitions) == len(types_)

        for i, type_ in enumerate(types_):
            data = tuple(score_definitions[i])
            await self.ps4debug.write_struct(self.pid, self.base + 0x8ACE30 + i * structure.size, structure, *data)

    async def set_score_definition(self, type_: NoteResultType, value: ScoreDefinition):
        structure = struct.Struct('<5I')
        address = self.base + 0x8ACE30 + type_.value * structure.size
        await self.ps4debug.write_struct(self.pid, address, structure, *tuple(value))

    async def get_vp(self) -> int:
        return await self.ps4debug.read_uint32(self.pid, self.base + 0xB34000 + 0xE7CDC)

    async def set_vp(self, value: int):
        await self.ps4debug.write_uint32(self.pid, self.base + 0xB34000 + 0xE7CDC, value)

    async def get_melody_icon_settings(self) -> int:
        return await self.ps4debug.read_uint32(self.pid, self.base + 0xB34000 + 0xE8460 + 0x2C)

    async def set_melody_icon_settings(self, value: int):
        assert 0 <= value < 5
        await self.ps4debug.write_uint32(self.pid, self.base + 0xB34000 + 0xE8460 + 0x2C, value)

    async def get_music_volume(self) -> float:
        address = self.base + 0xB34000 + 0xE8460 + 0x5C
        data = await self.ps4debug.read_int32(self.pid, address)
        return data * 0.06

    async def get_soundfx_volume(self) -> float:
        address = self.base + 0xB34000 + 0xE8460 + 0x60
        data = await self.ps4debug.read_int32(self.pid, address)
        return data * 0.06

    async def get_buttonfx_volume(self) -> float:
        address = self.base + 0xB34000 + 0xE8460 + 0x64
        data = await self.ps4debug.read_int32(self.pid, address)
        return data * 0.06

    async def get_calibration_shared(self) -> int:
        address = self.base + 0xB34000 + 0x11AFD0
        data = await self.ps4debug.read_int32(self.pid, address)
        return data

    async def set_calibration_shared(self, value: int):
        address = self.base + 0xB34000 + 0x11AFD0
        address2 = self.base + 0xB34000 + 0xE8460 + 0x24
        await self.ps4debug.write_int32(self.pid, address, value)
        await self.ps4debug.write_int32(self.pid, address2, value)

    async def get_calibration_song(self) -> int:
        address = self.base + 0xB34000 + 0x11AFD4
        data = await self.ps4debug.read_int32(self.pid, address)
        return data

    async def set_calibration_song(self, value: int):
        address = self.base + 0xB34000 + 0x11AFD4
        address2 = self.base + 0xB34000 + 0xE8460 + 0x28
        await self.ps4debug.write_int32(self.pid, address, value)
        await self.ps4debug.write_int32(self.pid, address2, value)

    async def get_chart(self) -> list[NoteDef] | None:
        start = await self.ps4debug.read_uint64(self.pid, self.base + 0xC687708 + 0x2C600)

        if start == 0:
            return

        end = await self.ps4debug.read_uint64(self.pid, self.base + 0xC687708 + 0x2C608)
        count = (end - start) // 0xB0

        chart = []
        for i in range(count):
            address = start + i * 0xB0
            data = await self.ps4debug.read_memory(self.pid, address, 0xB0)
            note_def = NoteDef.from_bytes(data)
            chart.append(note_def)

        return chart

    async def get_chart_size(self) -> int | None:
        start = await self.ps4debug.read_uint64(self.pid, self.base + 0xC687708 + 0x2C600)

        if start == 0:
            return

        end = await self.ps4debug.read_uint64(self.pid, self.base + 0xC687708 + 0x2C608)
        count = (end - start) // 0xB0
        return count

    async def get_chart_note(self, i: int) -> NoteDef | None:
        start = await self.ps4debug.read_uint64(self.pid, self.base + 0xC687708 + 0x2C600)

        if start == 0:
            return

        end = await self.ps4debug.read_uint64(self.pid, self.base + 0xC687708 + 0x2C608)
        count = (end - start) // 0xB0

        assert 0 <= i <= count
        address = start + i * 0xB0

        data = await self.ps4debug.read_memory(self.pid, address, 0xB0)
        note_def = NoteDef.from_bytes(data)
        return note_def

    async def set_chart_note(self, i: int, note_def: NoteDef):
        start = await self.ps4debug.read_uint64(self.pid, self.base + 0xC687708 + 0x2C600)

        if start == 0:
            return

        end = await self.ps4debug.read_uint64(self.pid, self.base + 0xC687708 + 0x2C608)
        count = (end - start) // 0xB0

        assert 0 <= i <= count
        address = start + i * 0xB0
        data = note_def.to_bytes()

        await self.ps4debug.write_memory(self.pid, address, data)

    async def get_note_index(self) -> int:
        address = self.base + 0xC687640 + 0x2C6E0
        data = await self.ps4debug.read_uint32(self.pid, address)
        return data

    async def set_note_index(self, value: int):
        address = self.base + 0xC687640 + 0x2C6E0
        await self.ps4debug.write_uint32(self.pid, address, value)

    async def get_song_name(self) -> str:
        flag = await self.ps4debug.read_byte(self.pid, self.base + 0xC687640 + 0x2CE10)
        is_pointer = (flag & 0xF0) > 0

        address = self.base + 0xC687640 + 0x2CDF8

        if is_pointer:
            address = await self.ps4debug.read_uint64(self.pid, address)

        return await self.ps4debug.read_text(self.pid, address, encoding='utf8')

    async def set_song_name(self, value: str):
        flag = await self.ps4debug.read_byte(self.pid, self.base + 0xC687640 + 0x2CE10)
        is_pointer = (flag & 0xF0) > 0
        max_length = 30 if is_pointer else 15

        # TODO inject pointer instead
        assert len(value) <= max_length

        address = self.base + 0xC687640 + 0x2CDF8

        if is_pointer:
            address = await self.ps4debug.read_uint64(self.pid, address)

        await self.ps4debug.write_text(self.pid, address, value, encoding='utf8')

    async def is_hidden(self) -> bool:
        address = self.base + 0xC687640 + 0x2D0A0
        data = await self.ps4debug.read_uint32(self.pid, address)
        return data == 2

    async def is_sudden(self) -> bool:
        address = self.base + 0xC687640 + 0x2D0A0
        data = await self.ps4debug.read_uint32(self.pid, address)
        return data == 3

    async def set_note_modifier(self, value: NoteModifier):
        address = self.base + 0xC687640 + 0x2D0A0
        await self.ps4debug.write_uint32(self.pid, address, value.value)

    async def disable_lyrics(self, clear: bool = True):
        # Disable writing to lyric text
        await self.ps4debug.write_memory(self.pid, self.base + 0x70824E, b'\x90' * 5)
        await self.ps4debug.write_memory(self.pid, self.base + 0x7081CB, b'\x90' * 8)
        await self.ps4debug.write_memory(self.pid, self.base + 0x6F63D5, b'\x90' * 9)
        await self.ps4debug.write_memory(self.pid, self.base + 0x6FF009, b'\x90' * 9)
        await self.ps4debug.write_memory(self.pid, self.base + 0x70C599, b'\x90' * 9)
        await self.ps4debug.write_memory(self.pid, self.base + 0x70C718, b'\x90' * 5)

        # Disable hiding lyrics
        await self.ps4debug.write_memory(self.pid, self.base + 0x7081BB, b'\x90' * 8)
        await self.ps4debug.write_memory(self.pid, self.base + 0x708227, b'\x90' * 6)
        await self.ps4debug.write_memory(self.pid, self.base + 0x70C587, b'\x90' * 9)
        await self.ps4debug.write_memory(self.pid, self.base + 0x70C70C, b'\x90' * 6)
        await self.ps4debug.write_memory(self.pid, self.base + 0x6F63C3, b'\x90' * 9)
        await self.ps4debug.write_memory(self.pid, self.base + 0x6FEFF7, b'\x90' * 9)

        if clear:
            await self.set_lyrics('')
        await self.set_lyrics_visible(True)

    async def enable_lyrics(self, clear: bool = True):
        # Enable writing to lyric text
        await self.ps4debug.write_memory(self.pid, self.base + 0x70824E, b'\xE8\xED\x09\x95\xFF')
        await self.ps4debug.write_memory(self.pid, self.base + 0x7081CB, b'\xC5\xFC\x11\x83\xA8\xD0\x02\x00')
        await self.ps4debug.write_memory(self.pid, self.base + 0x6F63D5, b'\xC4\xC1\x7C\x11\x86\xA8\xD0\x02\x00')
        await self.ps4debug.write_memory(self.pid, self.base + 0x6FF009, b'\xC4\xC1\x7C\x11\x86\xA8\xD0\x02\x00')
        await self.ps4debug.write_memory(self.pid, self.base + 0x70C599, b'\xC4\xC1\x7C\x11\x86\xA8\xD0\x02\x00')
        await self.ps4debug.write_memory(self.pid, self.base + 0x70C718, b'\xC4\xC1\x7C\x11\x07')

        # Enable hiding lyrics
        await self.ps4debug.write_memory(self.pid, self.base + 0x7081BB, b'\xC5\xFC\x11\x83\xD5\xD0\x02\x00')
        await self.ps4debug.write_memory(self.pid, self.base + 0x708227, b'\x88\x83\xF4\xD0\x02\x00')
        await self.ps4debug.write_memory(self.pid, self.base + 0x70C587, b'\xC4\xC1\x7C\x11\x86\xD5\xD0\x02\x00')
        await self.ps4debug.write_memory(self.pid, self.base + 0x70C70C, b'\xC4\xC1\x7C\x11\x47\x2D')
        await self.ps4debug.write_memory(self.pid, self.base + 0x6F63C3, b'\xC4\xC1\x7C\x11\x86\xD5\xD0\x02\x00')
        await self.ps4debug.write_memory(self.pid, self.base + 0x6FEFF7, b'\xC4\xC1\x7C\x11\x86\xD5\xD0\x02\x00')

        if clear:
            await self.set_lyrics('')

    async def get_lyrics(self) -> str:
        address = self.base + 0xC687640 + 0x2D0A8
        return await self.ps4debug.read_text(self.pid, address, encoding='utf8')

    async def set_lyrics(self, value: str):
        assert len(value) <= 75

        address = self.base + 0xC687640 + 0x2D0A8
        await self.ps4debug.write_text(self.pid, address, value, encoding='utf8')

    async def get_lyrics_visible(self) -> bool:
        address = self.base + 0xC687640 + 0x2D0F4
        return await self.ps4debug.read_bool(self.pid, address)

    async def set_lyrics_visible(self, value: bool):
        address = self.base + 0xC687640 + 0x2D0F4
        await self.ps4debug.write_bool(self.pid, address, value)

    async def get_life(self) -> int:
        address = self.base + 0xC687640 + 0x2D1B4
        data = await self.ps4debug.read_uint32(self.pid, address)
        return data

    async def set_life(self, value: int):
        address = self.base + 0xC687640 + 0x2D1B4
        await self.ps4debug.write_uint32(self.pid, address, value)

    async def get_score(self) -> int:
        address = self.base + 0xC687640 + 0x2D1B8
        data = await self.ps4debug.read_uint32(self.pid, address)
        return data

    async def set_score(self, value: int):
        address = self.base + 0xC687640 + 0x2D1B8
        await self.ps4debug.write_uint32(self.pid, address, value)

    async def get_score_valid(self) -> bool:
        address = self.base + 0xC687640 + 0x2D1C0
        data = await self.ps4debug.read_bool(self.pid, address)
        return data

    async def set_score_valid(self, value: bool):
        address = self.base + 0xC687640 + 0x2D1C0
        await self.ps4debug.write_bool(self.pid, address, value)

    async def get_combo(self) -> int:
        address = self.base + 0xC687640 + 0x2D1C8
        data = await self.ps4debug.read_uint32(self.pid, address)
        return data

    async def set_combo(self, value: int):
        address = self.base + 0xC687640 + 0x2D1C8
        await self.ps4debug.write_uint32(self.pid, address, value)

    async def get_cools(self) -> int:
        address = self.base + 0xC687640 + 0x2D1E0 + 0 * 4
        address2 = self.base + 0xC687640 + 0x2D1F4 + 0 * 4

        data = await self.ps4debug.read_uint32(self.pid, address)
        data2 = await self.ps4debug.read_uint32(self.pid, address2)

        assert data == data2

        return data

    async def set_cools(self, value: int):
        address = self.base + 0xC687640 + 0x2D1E0 + 0 * 4
        address2 = self.base + 0xC687640 + 0x2D1F4 + 0 * 4

        await self.ps4debug.write_uint32(self.pid, address, value)
        await self.ps4debug.write_uint32(self.pid, address2, value)

    async def get_fines(self) -> int:
        address = self.base + 0xC687640 + 0x2D1E0 + 1 * 4
        address2 = self.base + 0xC687640 + 0x2D1F4 + 1 * 4

        data = await self.ps4debug.read_uint32(self.pid, address)
        data2 = await self.ps4debug.read_uint32(self.pid, address2)

        assert data == data2

        return data

    async def set_fines(self, value: int):
        address = self.base + 0xC687640 + 0x2D1E0 + 1 * 4
        address2 = self.base + 0xC687640 + 0x2D1F4 + 1 * 4

        await self.ps4debug.write_uint32(self.pid, address, value)
        await self.ps4debug.write_uint32(self.pid, address2, value)

    async def get_safes(self) -> int:
        address = self.base + 0xC687640 + 0x2D1E0 + 2 * 4
        address2 = self.base + 0xC687640 + 0x2D1F4 + 2 * 4

        data = await self.ps4debug.read_uint32(self.pid, address)
        data2 = await self.ps4debug.read_uint32(self.pid, address2)

        assert data == data2

        return data

    async def set_safes(self, value: int):
        address = self.base + 0xC687640 + 0x2D1E0 + 2 * 4
        address2 = self.base + 0xC687640 + 0x2D1F4 + 2 * 4

        await self.ps4debug.write_uint32(self.pid, address, value)
        await self.ps4debug.write_uint32(self.pid, address2, value)

    async def get_bads(self) -> int:
        address = self.base + 0xC687640 + 0x2D1E0 + 3 * 4
        address2 = self.base + 0xC687640 + 0x2D1F4 + 3 * 4

        data = await self.ps4debug.read_uint32(self.pid, address)
        data2 = await self.ps4debug.read_uint32(self.pid, address2)

        assert data == data2

        return data

    async def set_bads(self, value: int):
        address = self.base + 0xC687640 + 0x2D1E0 + 3 * 4
        address2 = self.base + 0xC687640 + 0x2D1F4 + 3 * 4

        await self.ps4debug.write_uint32(self.pid, address, value)
        await self.ps4debug.write_uint32(self.pid, address2, value)

    async def get_misses(self) -> int:
        address = self.base + 0xC687640 + 0x2D1E0 + 4 * 4
        address2 = self.base + 0xC687640 + 0x2D1F4 + 4 * 4

        data = await self.ps4debug.read_uint32(self.pid, address)
        data2 = await self.ps4debug.read_uint32(self.pid, address2)

        assert data == data2

        return data

    async def set_misses(self, value: int):
        address = self.base + 0xC687640 + 0x2D1E0 + 4 * 4
        address2 = self.base + 0xC687640 + 0x2D1F4 + 4 * 4

        await self.ps4debug.write_uint32(self.pid, address, value)
        await self.ps4debug.write_uint32(self.pid, address2, value)

    async def get_processed_notes(self) -> int:
        address = self.base + 0xC687640 + 0x2D20C
        data = await self.ps4debug.read_uint32(self.pid, address)
        return data

    async def set_processed_notes(self, value: int):
        address = self.base + 0xC687640 + 0x2D20C
        await self.ps4debug.write_uint32(self.pid, address, value)

    async def disable_note_spawning(self):
        await self.ps4debug.write_memory(self.pid, self.base + 0x728448, b'\x90' * 5)

    async def enable_note_spawning(self):
        await self.ps4debug.write_memory(self.pid, self.base + 0x728448, b'\xE8\xE3\xC9\x00\x00')

    async def set_music_volume(self, volume: float) -> int:
        target = int.to_bytes(self.base + 0x67EB70, 8, 'little')
        prog = b'\x66\x48\x0F\x6E\xC7\x49\xBF' + target + b'\x41\xFF\xD7\xC3'

        assert 0 <= volume <= 1

        async with self.ps4debug.memory(self.pid, 4096) as memory:
            await memory.write(prog)
            res = await memory.call(volume, parameter_format='<f')

        return res[0]

    async def set_soundfx_volume(self, volume: float) -> int:
        target = int.to_bytes(self.base + 0x67EA50, 8, 'little')
        prog = b'\x66\x48\x0F\x6E\xC7\xBF\01\00\00\00\x49\xBF' + target + b'\x41\xFF\xD7\xC3'

        assert 0 <= volume <= 1

        async with self.ps4debug.memory(self.pid, 4096) as memory:
            await memory.write(prog)
            res = await memory.call(volume, parameter_format='<f')

        return res[0]

    async def set_buttonfx_volume(self, volume: float) -> int:
        target = int.to_bytes(self.base + 0x67EA50, 8, 'little')
        prog = b'\x66\x48\x0F\x6E\xC7\xBF\03\00\00\00\x49\xBF' + target + b'\x41\xFF\xD7\xC3'

        assert 0 <= volume <= 1

        async with self.ps4debug.memory(self.pid, 4096) as memory:
            await memory.write(prog)
            res = await memory.call(volume, parameter_format='<f')

        return res[0]

    async def play_music(self, file_path: str) -> int:
        target = int.to_bytes(self.base + 0x67ECD0, 8, 'little')
        prog = b'\xB3\x02\xB1\x02\x48\x8D\x35\x11\x00\x00\x00\x49\xBF' + target + \
               b'\x41\xFF\xD7\x48\x8B\xC7\xC3'

        async with self.ps4debug.memory(self.pid, 4096) as memory:
            await memory.write(prog)
            await self.ps4debug.write_text(self.pid, memory.address + len(prog), file_path)

            res = await memory.call()
        return res[0]

    async def spawn_note(self, *notes: NoteDef) -> int | None:
        chart_base = await self.ps4debug.read_uint64(self.pid, self.base + 0xC687708 + 0x2C600)

        # No chart loaded, spawning a note would crash the game
        if chart_base == 0:
            return

        game_target = int.to_bytes(self.base + 0x08B34000 + 0x3B81E78, 4, 'little')
        target = int.to_bytes(self.base + 0x734E30, 8, 'little')

        note_spawner = (b'\x48\x8B\xF7\x48\x8B\xDF\x48\x31\xFF\xBF' + game_target +
                        b'\x31\xDB\x49\xBF' + target + b'\x41\xFF\xD7\x49\x8B\xC3\xC3')

        async with self.ps4debug.memory(self.pid, 4096) as memory:
            await memory.write(note_spawner)

            note_base = memory.address + len(note_spawner)
            notes_max = (4096 - len(note_spawner)) // 0xB0

            # Ensure the note data fits in memory
            assert len(notes) <= notes_max

            # Send notes to game
            for i, note in enumerate(notes):
                note_bytes = note.to_bytes()
                await self.ps4debug.write_memory(self.pid, note_base + i * len(note_bytes), note_bytes)

            # Spawn the note
            rax = await memory.call(note_base)
        return rax[0]

    async def get_max_life(self) -> int:
        max_health = await self.ps4debug.read_uint32(self.pid, self.base + 0x70D4AA)
        return max_health - 1

    async def set_max_life(self, value: int):
        arg1 = (value + 1).to_bytes(4, 'little')
        arg2 = value.to_bytes(4, 'little')
        code = b'\x3D' + arg1 + b'\x7C\x13\xB8' + arg2 + b'\x41\x89\x84\x24\xB4\xD1\x02\x00\x90\x90\x90\x90'
        await self.ps4debug.write_memory(self.pid, self.base + 0x70D4A9, code)

    async def get_starting_life(self) -> int:
        addr = self.base + 0x70C5E8
        return await self.ps4debug.read_uint32(self.pid, addr)

    async def set_starting_life(self, value: int):
        await self.ps4debug.write_uint32(self.pid, self.base + 0x70C5E8, value)
        await self.ps4debug.write_uint32(self.pid, self.base + 0x6F820E, value)

    async def get_life_table(self, difficulty: DifficultyType) -> dict[NoteResultType, int]:
        notes = list(NoteResultType)

        address = self.base + 0x8AD040 + difficulty.value * len(notes) * 4
        life_table = await self.ps4debug.read_struct(self.pid, address, f'<{len(notes)}i')

        return {note: delta for note, delta in zip(notes, life_table)}

    async def get_life_tables(self) -> dict[DifficultyType, dict[NoteResultType, int]]:
        return {d: await self.get_life_table(d) for d in DifficultyType}

    async def set_life_table_entry(self, difficulty: DifficultyType, note: NoteResultType, value: int):
        notes = list(NoteResultType)
        address = self.base + 0x8AD040 + difficulty.value * len(notes) * 4
        address += note.value * 4
        await self.ps4debug.write_int32(self.pid, address, value)

    async def disable_score_invalidation(self):
        offsets = [
            0x128491,  # Shared - Decrement
            0x1287C5,  # Shared - Increment
            0x1284F5,  # Song - Decrement
            0x128822,  # Song - Increment
        ]

        await asyncio.gather(*[
            self.ps4debug.write_memory(self.pid, self.base + o, b'\x90' * 7) for o in offsets
        ])

    async def enable_score_invalidation(self):
        offsets = [
            0x128491,  # Shared - Decrement
            0x1287C5,  # Shared - Increment
            0x1284F5,  # Song - Decrement
            0x128822,  # Song - Increment
        ]

        await asyncio.gather(*[
            self.ps4debug.write_memory(self.pid, self.base + o, b'\xC6\x80\xC0\xD1\x02\x00\x00') for o in offsets
        ])

        await self.set_score_valid(True)

    async def disable_hold_invalidation(self):
        addr = self.base + 0x72F7D5
        await self.ps4debug.write_memory(self.pid, addr, b'\x90\x90\x90\xE9')

    async def enable_hold_invalidation(self):
        addr = self.base + 0x72F7D5
        await self.ps4debug.write_memory(self.pid, addr, b'\x84\xC0\x0F\x84')

    async def get_max_volume(self):
        multiplier = await self.ps4debug.read_float(self.pid, self.base + 0x7FA940)
        return multiplier * 10

    async def set_max_volume(self, volume: float):
        assert 0 <= volume <= 1
        await self.ps4debug.write_float(self.pid, self.base + 0x7FA940, volume / 10)
