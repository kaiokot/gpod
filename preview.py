import os
from os import mkdir
from os.path import isdir
import os
import subprocess
from os import mkdir, path
from os.path import isdir


class Preview:
    def __init__(self, git_opts):
        self.git_opts = git_opts

    def execute(self, command):
        PIPE = subprocess.PIPE

        try:
            process = subprocess.Popen(
                command, shell=True, stdout=PIPE, stderr=PIPE)
            stdoutput, stderroutput = process.communicate()

            # print(stdoutput)
            # print(stderroutput)
        except subprocess.CalledProcessError as err:
            print(err)

    def check_directory(self):
        # Make sure the repo is cloned
        git_dir = self.git_opts["git_dir"]
        git_path = self.git_opts["git_path"]

        if not isdir(git_dir):
            mkdir(git_dir)
            command = "git clone {} {}".format(git_path, git_dir)
            self.execute(command)

    def publish(self):
        git_dir = self.git_opts["git_dir"]

        command = "cd {} && git pull".format(git_dir)
        self.execute(command)

        # Commit and push
        command = "cd {} && git add . && git commit -m ':bento: Update preview' && git push -f".format(
            git_dir)
        self.execute(command)


# tks to, https://github.com/amouchere/growlab-project
