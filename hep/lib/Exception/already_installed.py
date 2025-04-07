class AlreadyInstalledException(Exception):
    def __init__(self, plugin: str) -> None:
        super().__init__(f"Plugin {plugin} already installed")
