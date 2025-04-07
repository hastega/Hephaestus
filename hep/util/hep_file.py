from os import makedirs, path, walk
from typing import Any


class HepFile:
    @staticmethod
    def find_replace_all(directory: str, find: str, replace: str) -> None:
        for file_path, _, files in walk(path.abspath(directory)):
            for file_name in files:
                HepFile.find_replace(file_path, file_name, find, replace)

    @staticmethod
    def find_replace(
        file_name: str, find, replace, file_path: str | None = None
    ) -> None:
        abs_file_path = path.join(file_path, file_name) if file_path else file_name

        try:
            with open(abs_file_path, "r") as f:
                s = f.read()
                s = s.replace(find, replace)
            with open(abs_file_path, "w") as f:
                f.write(s)
        except UnicodeDecodeError:
            pass

    @staticmethod
    def from_json(file_name: str, file_path: str | None = None) -> Any:
        from json import load

        abs_file_path = path.join(file_path, file_name) if file_path else file_name

        with open(abs_file_path, "r") as f:
            return load(f)

    @staticmethod
    def to_json(file_name: str, json: Any, file_path: str | None = None) -> None:
        from json import dump

        abs_file_path = path.join(file_path, file_name) if file_path else file_name

        if not path.exists(path.dirname(abs_file_path)):
            makedirs(path.dirname(abs_file_path))

        with open(abs_file_path, "w") as f:
            dump(json, f)
