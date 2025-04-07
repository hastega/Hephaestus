from typing import Any

from hep.lib.plugin_dto import PluginDTO


class PluginsDTO:
    def __init__(
        self,
        plugins: list[PluginDTO],
    ) -> None:
        self.plugins: list[PluginDTO] = plugins

    @classmethod
    def from_list(cls, json: list[dict[str, Any]]) -> "PluginsDTO":
        plugins: list[PluginDTO] = []

        for plugin in json:
            plugins.append(PluginDTO.from_json(plugin))

        return cls(plugins=plugins)

    def to_json(self) -> list[dict[str, Any]]:
        return [elem.to_json() for elem in self.plugins]

    def __str__(self) -> str:
        plugins: list[str] = []

        for plugin in self.plugins:
            if plugin.is_upgradable():
                plugins.append(
                    f"{plugin.name}: {plugin.version} -> {plugin.manifest.version}"
                )
            else:
                plugins.append(f"{plugin.name}: {plugin.version}")

        return "\n".join(plugins)

    def add(self, plugin: PluginDTO) -> bool:
        if self.find(plugin):
            return False

        self.plugins.append(plugin)
        return True

    def remove(self, plugin: PluginDTO) -> bool:
        plugin_selected: PluginDTO | None = self.find(plugin)
        return self._remove(plugin_selected)

    def remove_by_name(self, plugin: str) -> bool:
        plugin_selected: PluginDTO | None = self.find_by_name(plugin)
        return self._remove(plugin_selected)

    def _remove(self, plugin: PluginDTO | None) -> bool:
        if not plugin:
            return False

        self.plugins.remove(plugin)
        return True

    def find(self, plugin: PluginDTO) -> PluginDTO | None:
        return self.find_by_name(plugin.name)

    def find_by_name(self, plugin: str) -> PluginDTO | None:
        filter_plugin = filter(lambda elem: elem.name == plugin, self.plugins)
        return next(filter_plugin, None)

    def names(self) -> list[str]:
        return [elem.name for elem in self.plugins]

    def is_empty(self) -> bool:
        return len(self.plugins) == 0

    def update(self, plugin: PluginDTO) -> bool:
        plugin_selected: PluginDTO | None = self.find(plugin)
        if not plugin_selected:
            return False

        self.plugins.remove(plugin_selected)
        self.plugins.append(plugin)
        return True

    def merge(self, plugins: "PluginsDTO") -> None:
        for plugin in plugins.plugins:
            self.update(plugin)
