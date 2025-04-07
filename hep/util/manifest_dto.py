from typing import Any


class ManifestDTO:
    def __init__(
        self,
        name: str,
        description: str,
        version: str,
        authors: list[str],
        repository: str,
        branch: str,
    ) -> None:
        self.name: str = name
        self.description: str = description
        self.version: str = version
        self.authors: list[str] = authors
        self.repository: str = repository
        self.branch: str = branch

    @classmethod
    def from_path(cls, path: str) -> "ManifestDTO":
        from json import load
        from os.path import join
        from pathlib import Path

        parent = Path(path).parent.resolve()
        json = load(open(join(parent, "manifest.json")))
        return ManifestDTO.from_json(json)

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> "ManifestDTO":
        return cls(
            name=json["name"],
            description=json["description"],
            version=json["version"],
            authors=json["authors"],
            repository=json["repository"],
            branch=json["branch"],
        )

    def to_json(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "authors": self.authors,
            "repository": self.repository,
            "branch": self.branch,
        }
