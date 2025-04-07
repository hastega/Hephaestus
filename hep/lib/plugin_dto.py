from typing import Any

from hep.util.manifest_dto import ManifestDTO


class PluginDTO:
    def __init__(
        self, name: str, version: str, manifest: ManifestDTO, develop: bool
    ) -> None:
        self.name: str = name
        self.version: str = version
        self.manifest: ManifestDTO = manifest
        self.develop: bool = develop

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> "PluginDTO":
        return cls(
            name=json["name"],
            version=json["version"],
            manifest=ManifestDTO.from_json(json["manifest"]),
            develop=json["develop"] if "develop" in json else False,
        )

    def to_json(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "manifest": self.manifest.to_json(),
            "develop": self.develop,
        }

    def is_upgradable(self) -> bool:
        return not self.develop and self.manifest.version != self.version
