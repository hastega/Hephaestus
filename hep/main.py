import asyncio
from importlib.metadata import version

from hep.lib.plugins_manager import PluginsManager
from hep.util.hep_args_parser import HepArgsParser
from hep.util.progress import Progress

COMMAND_RUN = "run"
COMMAND_INSTALL = "install"
COMMAND_UNINSTALL = "uninstall"
COMMAND_LIST = "list"
COMMAND_UPDATE = "update"
COMMAND_UPGRADE = "upgrade"
COMMAND_NEW_PLUGIN = "new-plugin"
VERSION = "version"

commands = [
    COMMAND_RUN,
    COMMAND_INSTALL,
    COMMAND_UNINSTALL,
    COMMAND_LIST,
    COMMAND_UPDATE,
    COMMAND_UPGRADE,
    COMMAND_NEW_PLUGIN,
    VERSION,
]


def main():
    hep_parser = HepArgsParser()

    hep_parser.parser.add_argument(
        "command",
        type=str,
        choices=commands,
        help="Command",
    )
    args, _ = hep_parser.parser.parse_known_args()
    command = args.command

    if command == COMMAND_RUN:
        run(hep_parser)
    elif command == COMMAND_INSTALL:
        install(hep_parser)
    elif command == COMMAND_UNINSTALL:
        uninstall(hep_parser)
    elif command == COMMAND_LIST:
        list(hep_parser)
    elif command == COMMAND_UPDATE:
        update(hep_parser)
    elif command == COMMAND_UPGRADE:
        upgrade(hep_parser)
    elif command == COMMAND_NEW_PLUGIN:
        new_plugin(hep_parser)
    elif command == VERSION:
        app_version()


def run(hep_parser: HepArgsParser):
    plugin_manager = PluginsManager(hep_parser.parser)
    plugin_name = plugin_manager.get_plugin_name()
    plugin = plugin_manager.import_plugin(plugin_name)

    if not plugin:
        exit(1)

    method = plugin.get_method()
    _ = asyncio.run(plugin.exec(method))


def install(hep_parser: HepArgsParser):
    plugin_manager = PluginsManager(hep_parser.parser)

    try:
        plugin_manager.install(
            on_error=lambda error: print(error),
            progress=Progress(),
        )
    except Exception as e:
        print(e)


def uninstall(hep_parser: HepArgsParser):
    plugin_manager = PluginsManager(hep_parser.parser)

    try:
        plugin_manager.uninstall(
            on_error=lambda error: print(error),
        )
    except Exception as e:
        print(e)


def list(hep_parser: HepArgsParser):
    plugin_manager = PluginsManager(hep_parser.parser)
    if plugin_manager.plugins.is_empty():
        print("No plugins installed")
        return
    print(plugin_manager.plugins)


def update(hep_parser: HepArgsParser):
    plugin_manager = PluginsManager(hep_parser.parser)

    try:
        updates = plugin_manager.update(
            on_error=lambda error: print(error),
            progress=Progress(),
        )
        if updates.is_empty():
            return
        print(updates)
    except Exception as e:
        print(e)


def upgrade(hep_parser: HepArgsParser):
    plugin_manager = PluginsManager(hep_parser.parser)

    try:
        updates = plugin_manager.upgrade(
            on_error=lambda error: print(error),
            progress=Progress(),
        )
        print(updates)
    except Exception as e:
        print(e)


def new_plugin(hep_parser: HepArgsParser):
    plugin_manager = PluginsManager(hep_parser.parser)

    try:
        plugin_manager.new_plugin(
            on_error=lambda error: print(error),
            progress=Progress(),
        )
    except Exception as e:
        print(e)


def app_version():
    print(version("hep"))
