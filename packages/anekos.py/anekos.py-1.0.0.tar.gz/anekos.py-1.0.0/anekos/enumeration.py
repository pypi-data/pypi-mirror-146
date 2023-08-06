from enum import Enum, auto
from typing import List


class AutoName(Enum):
    def _generate_next_value_(name, *args):
        # https://docs.python.org/3/library/enum.html#using-automatic-values
        return name.lower()

    @classmethod
    def to_list(cls) -> List[str]:
        """Get all values, put them into a list and return.

        Returns
        -------
        List[str]
        """
        return [attr.value for attr in cls]


class NSFWImageTags(AutoName):
    FEMDOM = auto()
    CLASSIC = auto()
    EROFEET = auto()
    EROKITSUNE = "erok"
    LESBIAN = "les"
    #hololewd
    #lewdk
    KETA = auto()
    FEETGIF = "feetg"
    NSFW_NEKO_GIF = auto()
    EROYURI = auto()
    KUNI = auto()
    TITS = auto()
    PUSSY = "pussy_jpg"
    CUM = "cum_jpg"
    PUSSYGIF = "pussy"
    #lewdkemo
    #lewd
    CUM_GIF = "cum"
    SPANK = auto()
#    SMALLBOOBS = auto()
    RANDOM_HENTAI_GIF = "Random_hentai_gif"
    AVATAR = auto()
    BOOBS = auto()
    FEET = auto()
    GIRL_SOLO_GIF = "solog"
    BLOWJOB_GIF = "bj"
    YURI = auto()
    TRAP = auto()
    ANAL = auto()
    BLOWJOB = auto()
    HOLOERO = auto()
    GASM = auto()
    HENTAI = auto()
    FUTANARI = auto()
    ERO = auto()
    GIRL_SOLO = "solo"
    PUSSY_WANK_GIF = "pwankg"
    ERONEKO = "eron"
    EROKEMONOMINI = "erokemo"


class RealSFWImageTags(AutoName):
    MEOW = auto()
    EIGHTBALL = "8ball"
    LIZARD = auto()
    GOOSE = auto()
    WOOF = auto()


class SFWImageTags(AutoName):
    TICKLE = auto()
    NEKOGIF = "ngif"
    POKE = auto()
    KISS = auto()
    SLAP = auto()
    CUDDLE = auto()
    AVATAR = auto()
    FOX_GIRL = auto()
    HUG = auto()
    GECG = auto()
    PAT = auto()
    SMUG = auto()
    KEMONOMIMI = auto()
    HOLO = auto()
    WALLPAPER = auto()
    BAKA = auto()
    FEED = auto()
    NEKO = auto()
    WAIFU = auto()
