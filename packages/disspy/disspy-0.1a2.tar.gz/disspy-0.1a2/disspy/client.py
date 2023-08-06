from disspy import errs
from .core import DisApi
from .channel import DisChannel
from .embed import DisEmbed
from .guild import DisGuild
from .user import DisUser

from typing import (
    Optional,
    TypeVar,
    Union,
    Type
)

System = {
    bool: bool
}


class DisBotType:
    """
        ----------
        Main information
        ----------
        This class whose vars are str types for DisBot.

        @@@@@@@@@@@@@@@@
        ----------
        Using
        ----------
        import disspy

        bot = disspy.DisBot(token="YOUR_TOKEN", type=disspy.DisBotType.MESSAGE())
                                                ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
    """
    __description__: str = "Class for using types for DisBot"  # Description to class

    __varibles__: dict[str, str] = {  # Description to varibles
        "INTEGRATE": "Will be called when integration is creating (slash command, context menu)",
        "MESSAGE": "Will be called when message created"
    }

    _T: TypeVar = TypeVar("DisBotType")

    _INTEGRATE: str = "integrate"
    _MESSAGE: str = "message"

    @property
    def __class__(self) -> Type[_T]:
        """
        Returns type of this class
        --------
        :return self._T (Type of class):
        """
        return self._T

    @property
    def INTEGRATE(self) -> Type[_INTEGRATE]:
        return self._INTEGRATE

    @property
    def MESSAGE(self) -> Type[_MESSAGE]:
        return self._MESSAGE


class _BaseBot:
    _SLASH: str = "slash"
    _MESSAGE: str = "message"
    _COMMAND: str = "command"

    _isslash = False
    _ismessage = False
    _iscommand = False

    _NUMS = {
        "integrate": 1,
        "message": 2
    }

    def __init__(self, token: str, type: str, prefix: Optional[str] = "!"):
        self.token = token
        self.type = type

        self.commands = {}
        """
            For example:
            self.commands = {
                "help": help()
            }
        """

        try:
            _type_num = self._NUMS[type]

            if _type_num == 1:
                self._isslash = True
            elif _type_num == 2:
                self._ismessage = True
        except KeyError:
            raise errs.BotTypeError("Invalid type! Try again!")

        self.prefix = prefix


class DisBotStatus:
    ONLINE = "online"
    DND = "dnd"
    INVISIBLE = "invisible"
    IDLE = "idle"


class DisBot(_BaseBot):

    _T = TypeVar("DisBot")
    __parent__ = TypeVar("_BaseBot")

    def __init__(self, token: str, type: Union[DisBotType, str], prefix: Optional[str] = "!", status: Optional[str] = None):
        """
        Create bot

        :param token: Discord Developers Portal Bot Token
        :param prefix: Prefix for bot (There is no spaces!)
        """

        super().__init__(token, type, prefix)

        self.status = status

        self._on_messagec = None
        self._on_ready = None

        self.user = None

        self._api = DisApi(token)

        self.isready = False

        if prefix == "" or " " in prefix:
            raise errs.BotPrefixError("Invalid prefix! Try another!")
        else:
            self.prefix = prefix

        self.__slots__ = [self._api, self._on_ready, self._on_messagec, self.token, self.prefix,
                          self.commands, self.user, self.type, self.isready, self.status]

    @property
    def __class__(self) -> Type[_T]:
        """
            Returns type of this class
            --------
            :return self._T (Type of class):
        """
        return self._T

    async def _on_register(self):
        self.user: DisUser = self._api.user

    def on(self, type: str):
        """
        This method was created for changing on_ready and on_message method that using in runner

        :param type: Type of event
        :return: None (wrapper)
        """
        def wrapper(func):
            if type == "messagec":
                self._on_messagec = func
            elif type == "ready":
                self._on_ready = func
            else:
                raise errs.BotEventTypeError("Invalid type of event!")

        return wrapper

    def run(self, status: str = None):
        """
        Running bot

        :param status: Status for bot user
        :return: None
        """
        self.isready = True

        if status is None and self.status is None:
            self.status = "online"
        elif status is not None and self.status is None:
            self.status = status
        elif status is not None and self.status is not None:
            raise errs.BotStatusError("You typed status and in run() and in __init__()")

        self._runner(self.status, 10, 512)

    def _runner(self, status, version: int, intents: int):
        self._api.run(version, intents, status, self._on_ready, self._on_messagec, self._on_register)

        return 0  # No errors

    def disconnect(self):
        self._dissconnenter()

    def close(self):
        self._dissconnenter()

    def _dissconnenter(self):
        for _var in self.__slots__:
            del _var

    async def send(self, channel_id: int, content: Optional[str] = None, embeds: Optional[list[DisEmbed]] = None):
        if self.isready:
            channel = self.get_channel(channel_id)
            await channel.send(content=content, embeds=embeds)
        else:
            raise errs.InternetError("Bot is not ready!")

    async def send(self, channel_id: int, content: Optional[str] = None, embed: Optional[DisEmbed] = None):
        if self.isready:
            channel = self.get_channel(channel_id)
            await channel.send(content=content, embed=embed)
        else:
            raise errs.InternetError("Bot is not ready!")

    def get_channel(self, id: int) -> DisChannel:
        return self._api.get_channel(id)

    def get_guild(self, id: int) -> DisGuild:
        return self._api.get_guild(id)

    def get_user(self, id: int, premium_gets: System[bool] = True) -> DisUser:
        return self._api.get_user(id, premium_gets)
