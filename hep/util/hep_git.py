from os import listdir, path
from shutil import rmtree
from typing import Callable, Optional

from git import RemoteProgress
from git.repo import Repo

from hep.lib.string import HEP_FOLDER_EXIST, HEP_FOLDERNAME_SHORT


class HepGit:
    @staticmethod
    def clone(repo: str, dest: str, progress: Optional[Callable] = None) -> Repo:
        if len(dest) < 3:
            raise HepGitError(HEP_FOLDERNAME_SHORT.format(len(dest)))

        if path.exists(dest) and path.isdir(dest) and len(listdir(dest)) != 0:
            raise HepGitError(HEP_FOLDER_EXIST.format(dest))

        return Repo.clone_from(repo, dest, progress=progress)

    @staticmethod
    def checkout(repo: Repo, branch: str) -> None:
        repo.git.checkout(branch)

    @staticmethod
    def init(project_path: str, repo: Repo | None = None) -> Repo:
        if repo is not None:
            rmtree(path.join(project_path, ".git"))
        return Repo.init(project_path, b="main")

    @staticmethod
    def get_file(repo: Repo, file: str, branch: str) -> str:
        return repo.git.show(f"origin/{branch}:{file}")

    @staticmethod
    def fetch(repo: Repo, progress: RemoteProgress | None = None) -> None:
        repo.remotes.origin.fetch(progress=progress)

    @staticmethod
    def reset(repo: Repo, branch: str, hard: bool = False) -> None:
        mode: str = "--hard" if hard else "--soft"
        repo.git.reset(mode, f"origin/{branch}")


class HepGitError(Exception):
    """Base class for exceptions in this module."""
