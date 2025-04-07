from tqdm import tqdm

from hep.lib.plugins_manager import PluginsStatus
from hep.util.progress_interface import ProgressInterface


class Progress(ProgressInterface):
    def __init__(self) -> None:
        super().__init__()

        self.pbar: tqdm | None = None
        self.description: dict = {
            PluginsStatus.FETCH: "Fetching",
            PluginsStatus.INSTALL: "Installing",
            PluginsStatus.UPGRADE: "Upgrading",
        }

    def setup(self, name: str, status: PluginsStatus) -> None:
        self.pbar = tqdm(unit="B", unit_scale=True, unit_divisor=1024)
        self.pbar.set_description(f"{self.description[status]} {name}")

    def update(self, op_code, cur_count, max_count=None, message=""):
        if self.pbar is not None:
            self.pbar.total = max_count * 1024 if max_count is not None else cur_count
            self.pbar.n = cur_count * 1024
            self.pbar.refresh()

    def __del__(self):
        self.close()

    def close(self) -> None:
        if self.pbar is not None:
            self.pbar.close()
