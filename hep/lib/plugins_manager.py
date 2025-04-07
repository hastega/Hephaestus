import inspect
import os
from argparse import ArgumentParser
from enum import Enum
from importlib import import_module
from json import loads
from os import remove, symlink
from pathlib import Path
from shutil import move, rmtree
from sys import path
from tempfile import mkdtemp

from git.repo import Repo

from hep.lib.Exception.already_installed import AlreadyInstalledException
from hep.lib.Exception.no_plugin import ItsNotAPluginException
from hep.lib.Exception.not_installed import NotInstalledException
from hep.lib.plugin import Plugin
from hep.lib.plugin_dto import PluginDTO
from hep.lib.plugins_dto import PluginsDTO
from hep.lib.type import ErrorFallback
from hep.util.const import (
    DEFAULT_PLUGIN,
    MANIFEST_FILE,
    PLUGINS_DIR,
    PLUGINS_FILE,
    PROGRAM_FOLDER_LINUX,
    PROGRAM_FOLDER_WIN,
)
from hep.util.hep_file import HepFile
from hep.util.hep_git import HepGit
from hep.util.manifest_dto import ManifestDTO
from hep.util.plugin import HepPlugin
from hep.util.progress_interface import ProgressInterface
from hep.util.shell import confirmation


class PluginsStatus(Enum):
    INSTALL = "install"
    UPGRADE = "upgrade"
    FETCH = "fetch"


class PluginsManager:
    def __init__(self, hep_parser: ArgumentParser) -> None:
        self.plugins: PluginsDTO
        self._hep_parser = hep_parser

        self.load_plugins()

    @staticmethod
    def _get_program_folder() -> Path:
        if os.name == "posix":
            return Path.home().joinpath(PROGRAM_FOLDER_LINUX)

        return Path(os.path.expandvars(PROGRAM_FOLDER_WIN))

    @staticmethod
    def get_plugins_file_path() -> str:
        return str(
            PluginsManager._get_program_folder().joinpath(PLUGINS_FILE).absolute()
        )

    @staticmethod
    def get_plugins_folder() -> str:
        return str(
            PluginsManager._get_program_folder().joinpath(PLUGINS_DIR).absolute()
        )

    def load_plugins(self) -> None:
        file: str = PluginsManager.get_plugins_file_path()

        try:
            json = HepFile.from_json(file)
        except Exception:
            json = []
            HepFile.to_json(file, json)

        self.plugins = PluginsDTO.from_list(json)

    def save_plugins(self, plugins_dto: PluginsDTO | None = None) -> None:
        file: str = PluginsManager.get_plugins_file_path()

        if plugins_dto:
            self.plugins.merge(plugins_dto)

        HepFile.to_json(file, self.plugins.to_json())

    def get_plugin_name(self) -> str:
        self._hep_parser.add_argument(
            "plugin",
            type=str,
            choices=self.plugins.names(),
            help="Plugin to use",
        )

        args, _ = self._hep_parser.parse_known_args()
        return args.plugin

    def import_plugin(self, plugin: str) -> Plugin | None:
        path.append(str(PluginsManager._get_program_folder()))
        module = import_module(f"{PLUGINS_DIR}.{plugin}")

        imported_classes: list[type] = [
            obj for _, obj in inspect.getmembers(module, inspect.isclass)
        ]

        for imported_class in imported_classes:
            if issubclass(imported_class, HepPlugin):
                return Plugin(imported_class, self._hep_parser)  # type: ignore

        return None

    @staticmethod
    def get_manifest(
        repo: str, plugin_dto: PluginDTO, progress: ProgressInterface | None
    ) -> ManifestDTO:
        repository = Repo(repo)

        if progress:
            progress.setup(repo, PluginsStatus.FETCH)

        HepGit.fetch(repository, progress)

        if progress:
            progress.close()

        json = HepGit.get_file(repository, MANIFEST_FILE, plugin_dto.manifest.branch)

        return ManifestDTO.from_json(loads(json))

    def install(
        self,
        on_error: ErrorFallback,
        progress: ProgressInterface,
    ) -> None:
        def install_link(destination: str, repository: str) -> None:
            folder = Path(repository).resolve().absolute()

            if not folder.is_dir():
                raise ItsNotAPluginException(repository)

            manifest_file = folder.absolute().joinpath(MANIFEST_FILE)

            try:
                json = HepFile.from_json(str(manifest_file))
                manifest = ManifestDTO.from_json(json)
            except Exception:
                raise ItsNotAPluginException(destination)

            if not self.plugins.add(
                PluginDTO(manifest.name, manifest.version, manifest, develop=True)
            ):
                raise AlreadyInstalledException(manifest.name)

            destination = str(Path(destination).joinpath(manifest.name))
            symlink(folder, destination)

        def install_clone(destination: str, repository: str, tag: str | None) -> None:
            tmp = mkdtemp()

            progress.setup(repository, PluginsStatus.INSTALL)
            HepGit.clone(repository, tmp, progress=progress)  # type: ignore
            progress.close()

            manifest_file = Path(tmp).joinpath(MANIFEST_FILE)

            if tag:
                HepGit.checkout(Repo(tmp), tag)

            try:
                json = HepFile.from_json(str(manifest_file))
                manifest = ManifestDTO.from_json(json)
            except Exception:
                raise ItsNotAPluginException(repository)

            if not self.plugins.add(
                PluginDTO(
                    manifest.name, manifest.version, manifest, develop=tag is not None
                )
            ):
                rmtree(tmp)
                raise AlreadyInstalledException(manifest.name)

            if not tag:
                HepGit.checkout(Repo(tmp), manifest.branch)

            destination = str(Path(destination).joinpath(manifest.name))
            move(tmp, destination)

        destination: str = PluginsManager.get_plugins_folder()

        self._hep_parser.add_argument(
            "repository",
            type=str,
            help="Repository to install",
        )

        self._hep_parser.add_argument(
            "--link-to-folder",
            help="Make a symlink to the folder instead of clone it",
            action="store_true",
        )

        self._hep_parser.add_argument(
            "-t",
            "--tag",
            type=str,
            help="Specify the tag of the repository",
        )

        args, _ = self._hep_parser.parse_known_args()
        repository: str = args.repository
        is_a_link_to_a_folder: bool = args.link_to_folder
        tag: str = args.tag

        if not Path(destination).exists():
            Path(destination).mkdir(parents=True)

        # Ask for confirmation
        repository_name = (
            f"{Path(repository).name}@{tag}" if tag else Path(repository).name
        )
        message = f"The following NEW package will be installed:\n{repository_name}"
        if not confirmation(message, yes_is_default=not is_a_link_to_a_folder):
            return None

        try:
            if is_a_link_to_a_folder:
                message = (
                    "[WARNING] installing a folder is designated for develop use only."
                )
                if not confirmation(message, yes_is_default=False):
                    return None
                install_link(destination, repository)
            else:
                install_clone(destination, repository, tag)
        except ItsNotAPluginException as e:
            return on_error(e)
        except AlreadyInstalledException as e:
            return on_error(e)

        self.save_plugins()
        return None

    def uninstall(self, on_error: ErrorFallback) -> None:
        destination: str = PluginsManager.get_plugins_folder()

        self._hep_parser.add_argument(
            "plugin",
            type=str,
            help="Plugin to remove",
        )

        args, _ = self._hep_parser.parse_known_args()
        plugin: str = args.plugin

        # Ask for confirmation
        message = f"The following package will be removed:\n{plugin}"
        if not confirmation(message):
            return None

        if not self.plugins.remove_by_name(plugin):
            return on_error(NotInstalledException(plugin))

        destination = str(Path(destination).joinpath(plugin))
        try:
            rmtree(destination)
        except Exception:
            remove(destination)

        self.save_plugins()
        return None

    def update(
        self,
        on_error: ErrorFallback,
        progress: ProgressInterface,
    ) -> PluginsDTO | None:
        self._hep_parser.add_argument(
            "plugin",
            type=str,
            nargs="?",
            help="Plugin to update",
            default=None,
        )

        args, _ = self._hep_parser.parse_known_args()
        plugin: str | None = args.plugin

        plugins: list[str] = self.plugins.names() if plugin is None else [plugin]

        updates: PluginsDTO = PluginsDTO([])

        for plugin in plugins:
            plugin_dto: PluginDTO | None = self.plugins.find_by_name(plugin)

            if plugin_dto is None:
                return on_error(NotInstalledException(plugin))

            if plugin_dto.develop:
                continue

            self._update_plugin(plugin, plugin_dto, progress)

            if plugin_dto.is_upgradable():
                updates.add(plugin_dto)

        self.save_plugins()
        return updates

    def _update_plugin(
        self,
        plugin: str,
        plugin_dto: PluginDTO,
        progress: ProgressInterface,
    ) -> PluginDTO | None:
        destination: str = PluginsManager.get_plugins_folder()

        destination = str(Path(destination).joinpath(plugin))
        manifest: ManifestDTO = self.get_manifest(destination, plugin_dto, progress)

        plugin_dto.manifest = manifest

    def upgrade(
        self,
        on_error: ErrorFallback,
        progress: ProgressInterface,
    ) -> PluginsDTO | None:
        self._hep_parser.add_argument(
            "plugin",
            type=str,
            nargs="?",
            help="Plugin to upgrade",
            default=None,
        )

        args, _ = self._hep_parser.parse_known_args()
        plugin_name: str | None = args.plugin
        plugins: PluginsDTO = PluginsDTO([])

        if plugin_name:
            plugin_dto: PluginDTO | None = self.plugins.find_by_name(plugin_name)

            if not plugin_dto:
                return on_error(NotInstalledException(plugin_name))

            plugins.add(plugin_dto)
        else:
            plugins = PluginsDTO.from_list(self.plugins.to_json())

        for plugin in plugins.plugins:
            if not self.is_upgradable(plugin):
                plugins.remove(plugin)

        if plugins.is_empty():
            raise Exception("No upgradable plugins")

        # Ask for confirmation
        message = (
            f"The following packages will be upgraded:\n{', '.join(plugins.names())}"
        )
        if not confirmation(message):
            return None

        for plugin in plugins.plugins:
            plugin = self._upgrade_plugin(plugin)

        self.save_plugins(plugins)
        return plugins

    def is_upgradable(
        self,
        plugin_dto: PluginDTO,
    ) -> bool:
        return plugin_dto.manifest.version != plugin_dto.version

    def _upgrade_plugin(self, plugin_dto: PluginDTO) -> PluginDTO | None:
        destination: str = PluginsManager.get_plugins_folder()
        destination = str(Path(destination).joinpath(plugin_dto.name))

        repository = Repo(destination)

        HepGit.reset(repository, plugin_dto.manifest.branch, True)

        plugin_dto.manifest = self.get_manifest(destination, plugin_dto, None)
        plugin_dto.version = plugin_dto.manifest.version

        return plugin_dto

    def new_plugin(
        self,
        on_error: ErrorFallback,
        progress: ProgressInterface,
    ) -> str | None:
        self._hep_parser.add_argument(
            "plugin",
            type=str,
            help="Plugin name",
            default=None,
        )

        args, _ = self._hep_parser.parse_known_args()
        plugin_name: str | None = args.plugin
        destination: str = "./"

        if plugin_name is None:
            return on_error(Exception())

        # Ask for confirmation
        message = (
            "A new plugin called "
            f"{plugin_name}"
            " will be created in "
            f"{'this folder' if destination == './' else destination}"
        )
        if not confirmation(message):
            return None

        tmp = mkdtemp()

        progress.setup(DEFAULT_PLUGIN, PluginsStatus.INSTALL)
        HepGit.clone(DEFAULT_PLUGIN, tmp, progress=progress)  # type: ignore
        progress.close()

        destination += plugin_name
        move(tmp, destination)
        rmtree(destination + "/.git")

        return plugin_name
