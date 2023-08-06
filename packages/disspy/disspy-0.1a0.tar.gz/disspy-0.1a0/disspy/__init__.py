from .client import DisBot, DisBotStatus
from .errs import UserNitroTypeError, InternetError, BotTypeError, BotPrefixError, MissingPerms
from .guild import DisGuild
from .channel import DisChannel
from .embed import DisEmbed, DisField, DisColor
from .message import DisMessage
from .user import DisUser
from ._core import DisApi, DisFlags

import typing

"""
    Main information about dispy
    
    :var: __version__ -> Version of dipsy
    :var: __github__ -> Link to github repo
    :var: __packagename__ -> Name of package 
"""

__version__ = "0.1dev"
__minpythonver__ = "3.6"
__github__ = "https://github.com/itttgg/dispy"
__stablever__ = "https://github.com/itttgg/dispy/tree/0.1-dev-preview-3.4"
__description__ = "Dispy - package for creating bots."
__packagename__ = "dispy"


class _DocObject:
    __description__: str = ""  # Description to class
    __doc__: str = ""  # Mini doc with using
    __varibles__: dict[str, str] = {}  # Description to varibles

    _T: typing.TypeVar = None

    def __str__(self) -> str:  # Using in str()
        r = ""

        for i in self.__varibles__.keys():
            if r == "":
                r += i
            else:
                r += f", {i}"

        return r


# Types for simpler creating bots
class DisBotEventType(_DocObject):  # Event type for DisBot
    __description__: str = "This class created for simplification adding events to DisBot. This is class, not an object"  # Description to class

    __varibles__: dict[str, str] = {  # Description to varibles
        "ON_MESSAGE": ":type: property, :returns: str - Will be called when new message was created in DisBot.guild.channel",
        "ON_READY": ":type: property, :returns: str - Will be called when bot becomes ready"
    }

    # Mini doc with using
    __doc__: str = "Using:" \
                   "@bot.on(dispy.DisBotEventType.ONMESSAGEC())" \
                   "async def on_messagec(message):" \
                   "    await message.channel.send('Test!')"

    _T: typing.TypeVar = typing.TypeVar("DisBotEventType")

    @property
    def __class__(self) -> typing.Type[_T]:
        return self._T

    @property
    def ON_MESSAGEC(self) -> str:
        return "messagec"

    @property
    def ON_READY(self) -> str:
        return "ready"
