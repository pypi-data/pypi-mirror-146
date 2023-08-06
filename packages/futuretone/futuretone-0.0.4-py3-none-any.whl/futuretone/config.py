from pydantic import BaseSettings, BaseModel, Field, Extra, ValidationError, validator
from pathlib import Path
import configparser
import enum


class SpawnPoolValues(str, enum.Enum):
    full = 'all'
    no_sliders = 'no_sliders'
    no_holds = 'no_holds'
    only_regular = 'only_regular'


class CommandSettings(BaseModel):
    enabled: bool
    title: str
    description: str = ''
    notify: bool = False


class DurationSettings(CommandSettings):
    duration: int = 5


class SpawnRandomSettings(CommandSettings):
    min_: int = Field(..., alias='min', env='min')
    max_: int = Field(..., alias='max', env='max')
    pool: SpawnPoolValues
    allow_duplicates: bool = Field(True, alias='allowduplicates', env='allowduplicates')

    @validator('min_', 'max_')
    def check_minmax(cls, v):
        if v < 1 or v > 4:
            raise ValueError('Invalid value for note range. Use 1 to 4.')
        return v


class SpawnSettings(CommandSettings):
    TriangleHold: set[str] = Field(..., alias='trianglehold', env='trianglehold')
    Triangle: set[str] = Field(..., alias='triangle', env='triangle')
    SquareHold: set[str] = Field(..., alias='squarehold', env='squarehold')
    Square: set[str] = Field(..., alias='square', env='square')
    CrossHold: set[str] = Field(..., alias='crosshold', env='crosshold')
    Cross: set[str] = Field(..., alias='cross', env='cross')
    CircleHold: set[str] = Field(..., alias='circlehold', env='circlehold')
    Circle: set[str] = Field(..., alias='circle', env='circle')
    SlideR: set[str] = Field(..., alias='slider', env='slider')
    SlideL: set[str] = Field(..., alias='slidel', env='slidel')
    exclude: set[int] = Field(set())
    allow_random: bool = Field(True, alias='allowrandom', env='allowrandom')

    @validator('exclude',
               'TriangleHold',
               'Triangle',
               'SquareHold',
               'Square',
               'CrossHold',
               'Cross',
               'CircleHold',
               'Circle',
               'SlideR',
               'SlideL', pre=True)
    def map_to_set(cls, v):
        if isinstance(v, str):
            return {x.strip().lower() for x in v.split(',')} if len(v) else set()
        return v


class HarmSettings(CommandSettings):
    damage: int = 10
    can_kill: bool = Field(False, alias='cankill', env='cankill')

    @validator('damage')
    def check_positive(cls, v):
        if v < 1:
            raise ValueError('Cannot damage 0 or less health. Use a positive number.')
        return v


class HealSettings(CommandSettings):
    life: int = 30
    full: bool = False

    @validator('life')
    def check_positive(cls, v):
        if v < 1:
            raise ValueError('Cannot give 0 or less health. Use a positive number.')
        return v


class ChangeCalibrationSettings(DurationSettings):
    range_: int = Field(..., alias='range', env='range')


class GameSettings(BaseModel):
    max_life: int = Field(255, alias='maxlife', env='maxlife')
    start_life: int = Field(127, alias='startlife', env='startlife')
    disable_lyrics: bool = Field(True, alias='disablelyrics', env='disablelyrics')
    max_volume: float = Field(0.6, alias='maxvolume', env='maxvolume')
    unpatch_holds: bool = Field(True, alias='unpatchholds', env='unpatchholds')
    unpatch_calibration: bool = Field(True, alias='unpatchcalibration', env='unpatchcalibration')

    # TODO turn into pydantic models and writer a validator splitting the semicolon of the strings
    cool: str = Field(..., alias='cool', env='cool')
    fine: str = Field(..., alias='fine', env='fine')
    safe: str = Field(..., alias='safe', env='safe')
    bad: str = Field(..., alias='bad', env='bad')
    cool_wrong: str = Field(..., alias='coolwrong', env='coolwrong')
    fine_wrong: str = Field(..., alias='finewrong', env='finewrong')
    safe_wrong: str = Field(..., alias='safewrong', env='safewrong')
    bad_wrong: str = Field(..., alias='badwrong', env='badwrong')
    miss: str = Field(..., alias='miss', env='miss')
    cool_double: str = Field(..., alias='cooldouble', env='cooldouble')
    fine_double: str = Field(..., alias='finedouble', env='finedouble')
    safe_double: str = Field(..., alias='safedouble', env='safedouble')
    bad_double: str = Field(..., alias='baddouble', env='baddouble')
    cool_triple: str = Field(..., alias='cooltriple', env='cooltriple')
    fine_triple: str = Field(..., alias='finetriple', env='finetriple')
    safe_triple: str = Field(..., alias='safetriple', env='safetriple')
    bad_triple: str = Field(..., alias='badtriple', env='badtriple')
    cool_quad: str = Field(..., alias='coolquad', env='coolquad')
    fine_quad: str = Field(..., alias='finequad', env='finequad')
    safe_quad: str = Field(..., alias='safequad', env='safequad')
    bad_quad: str = Field(..., alias='badquad', env='badquad')

    @validator('max_life', 'start_life')
    def check_health(cls, v):
        if v > 0:
            return v
        raise ValueError('Life values have to be greater than 0.')


class GlobalSettings(BaseModel):
    verbose: bool | int | None = 0
    ip: str | None
    bot_token: str = Field(..., alias='token', env='token')
    access_token: str = Field(..., alias='usertoken', env='usertoken')
    title_id: str = Field(..., alias='titleid', env='titleid')
    channel: str
    prefix: str = '!'

    @validator('ip')
    def check_ip_empty(cls, v):
        if isinstance(v, str):
            return v.strip() if len(v.strip()) else None
        return v  # Only None here

    @validator('bot_token', 'access_token')
    def check_token_length(cls, v):
        if len(v) != 30:
            raise ValueError('Tokens have to be 30 characters long')
        return v

    @validator('title_id')
    def assert_titleid(cls, v):
        if v != 'CUSA06211':
            raise ValueError('Only "CUSA06211" allowed')
        return v


class Settings(BaseSettings):
    class Config:
        extra = Extra.allow

    global_: GlobalSettings = Field(..., alias='global', env='global')
    game: GameSettings
    spawn_random: SpawnRandomSettings
    spawn: SpawnSettings
    kill: CommandSettings
    harm: HarmSettings
    heal: HealSettings
    invincibility: DurationSettings
    change_calibration: ChangeCalibrationSettings
    sudden_modifier: DurationSettings
    hidden_modifier: DurationSettings
    invalidate_score: DurationSettings
    highlight: CommandSettings
    enable_slow: DurationSettings


def get_config(file_path: str | Path = 'config.ini') -> Settings:
    parser = configparser.ConfigParser()
    read = parser.read(file_path)

    if not len(read):
        raise FileNotFoundError(f'{file_path} not found.')

    sections = parser.sections()

    data = {s: {k: v for k, v in parser[s].items()} for s in sections}
    settings = Settings(**data)

    return settings


def set_config(settings: Settings, file_path: str | Path = 'config.ini'):
    parser = configparser.ConfigParser()
    data = settings.dict(by_alias=True, exclude_none=True)

    for section, sub_setting in data.items():
        parser.add_section(section)

        for key, value in sub_setting.items():
            if isinstance(value, list):
                value = ','.join(map(str, value))
            parser.set(section, key, str(value))

    with open(file_path, 'w') as f:
        parser.write(f)
