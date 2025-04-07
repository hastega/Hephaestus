from argparse import ArgumentParser
from types import CoroutineType
from typing import Coroutine

from hep.util.plugin import HepPlugin
from hep.util.str import Str


class Plugin:
    def __init__(self, plugin: HepPlugin, hep_parser: ArgumentParser) -> None:
        self._plugin = plugin
        self._methods_name: list[str] = []

        self._hep_parser = hep_parser

    def get_method(self) -> str:
        self._methods_name = [
            method for method in dir(self._plugin) if not method.startswith("_")
        ]

        self._hep_parser.add_argument(
            "method",
            type=str,
            choices=Str.replace_str_in_list(self.methods, "_", "-"),
            help="Method name",
        )
        args, _ = self._hep_parser.parse_known_args()
        return args.method.replace("-", "_")

    def _get_method_list_name(self) -> list[str]:
        return self._methods_name

    async def exec(self, method: str) -> Coroutine:
        plugin = self._plugin()
        value = getattr(plugin, method)(self._hep_parser)

        if isinstance(value, CoroutineType):
            return await value
        return value

    methods = property(fget=_get_method_list_name)


class PluginDTO:
    def __init__(
        self, name: str | None, version: str | None, source: str | None
    ) -> None:
        self.name: str | None = name
        self.version: str | None = version
        self.source: str | None = source

    @staticmethod
    def from_json(json: dict[str, str | None]):
        return PluginDTO(
            name=json["name"] if "name" in json else None,
            version=json["version"] if "version" in json else None,
            source=json["source"] if "source" in json else None,
        )

    @staticmethod
    def from_json_list(json: list[dict[str, str | None]]):
        return [PluginDTO.from_json(elem) for elem in json]

    def to_json(self) -> dict[str, str | None]:
        return {
            "name": self.name,
            "version": self.version,
            "source": self.source,
        }
