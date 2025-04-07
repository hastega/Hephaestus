class NotInstalledException(Exception):
    def __init__(self, plugin: str) -> None:
        super().__init__(f"Plugin {plugin} is not installed")
