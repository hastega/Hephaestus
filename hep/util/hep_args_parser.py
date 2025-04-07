from argparse import ArgumentParser, RawDescriptionHelpFormatter

from hep.lib.string import HEP_DESCRIPTION
from hep.util.const import PROGRAM_NAME


class HepArgsParser:
    def __init__(self) -> None:
        self._hep_parser = ArgumentParser(
            prog=PROGRAM_NAME,
            formatter_class=RawDescriptionHelpFormatter,
            description=self._description(),
        )

    def _description(self):
        return HEP_DESCRIPTION

    @property
    def parser(self) -> ArgumentParser:
        return self._hep_parser
