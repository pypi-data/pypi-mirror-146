import shlex
import subprocess
import re
import click
import os
import sys


class GitPrune(object):
    def __init__(self, **kwargs):
        self.working_directory = kwargs["dir_"] if ("dir_" in kwargs) else os.getcwd()
        self.is_git = (
            True
            if ".git" in os.listdir(self.working_directory)
            else sys.exit("Directory does not contain .git directory.")
        )
        self.git = (
            f"/usr/bin/git --git-dir={self.working_directory}/.git/ --work-tree={self.working_directory}"
            if self.working_directory != os.getcwd()
            else "git"
        )

        self.shell_cmd(f"{self.git} fetch -p")
        self.remote_branches = self.get_remote_branches()
        self.local_branches = self.get_local_branches()
        self.not_remote = list(set(self.local_branches) - set(self.remote_branches))

    def shell_cmd(self, cmd: str) -> str:
        """Execute a shell command

        Args:
            cmd (str): Shell command with arguments to execute

        Returns:
            str: Shell command output
        """
        try:
            cmd = shlex.split(cmd)
            results = subprocess.check_output(
                cmd, stderr=subprocess.STDOUT, shell=False
            )
            results = results.strip()
            return results.decode("UTF-8")
        except subprocess.CalledProcessError as e:
            errorText = e.output.strip()
            return errorText.decode("UTF-8")

    def get_remote_branches(self) -> list:
        """Get branches currently on remote

        Returns:
            list: List of remote branches
        """
        remote_branches = self.shell_cmd(f"{self.git} for-each-ref")
        remote_branches = re.findall(r"refs/remotes/[a-zA-Z]*/(.*)", remote_branches)
        for line in remote_branches:
            if "HEAD" in line:
                remote_branches.remove(line)
            else:
                pass
        return remote_branches

    def get_local_branches(self) -> list:
        """Get branches currently on the local machine

        Returns:
            str: List of local branches
        """
        local_branches = self.shell_cmd(f"{self.git} for-each-ref")
        local_branches = re.findall(r"refs/heads/(.*)", local_branches)
        return local_branches

    def delete_branches(self):
        """Delete the branches not on remote"""
        self.shell_cmd(f"git checkout {self.get_remote_branches()[0]}")
        for branch in self.not_remote:
            self.shell_cmd(f'{self.git} branch -D "{branch}"')

    def prune_local_branches(self):
        """
        Confirm which branches will be removed. Remove them.
        """
        if self.not_remote:
            delete_branches = input(
                f"Branch(es) {self.not_remote} do not exist in the origin repository. Would you like to delete them? y/n: "
            )
            if delete_branches == "y":
                self.delete_branches()
            else:
                print(f"Branch(es) {self.not_remote} will not be deleted.")
        else:
            print("Local git branches match remote. No pruning needed.")
            sys.exit(0)


@click.command()
@click.option(
    "-d",
    "--directory",
    "dir_",
    default="pwd",
    help="Specify your target directory. Default is current working directory.",
)
def cli(dir_):
    if dir_ == "pwd":
        dir_ = os.getcwd()
    git_prune = GitPrune(dir_=dir_)
    git_prune.prune_local_branches()


if __name__ == "__main__":
    cli()
