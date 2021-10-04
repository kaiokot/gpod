import logging
import os
from os import mkdir
from os.path import isdir
import os
import subprocess
from os import mkdir, path
from os.path import isdir
import shutil
import json

# tks to, https://github.com/amouchere/gpod-project


class Preview:
    def __init__(self, settings, git_opts):
        self.git_opts = git_opts
        self.settings = settings

    def execute(self, command):
        logger = logging.getLogger("gpod")
        PIPE = subprocess.PIPE

        try:
            process = subprocess.Popen(
                command, shell=True, stdout=PIPE, stderr=PIPE)
            stdoutput, stderroutput = process.communicate()

            logger.info(stdoutput)
            logger.error(stderroutput)
        except subprocess.CalledProcessError as ex:
            logger.error(ex)

    def check_directory(self):
        logger = logging.getLogger("gpod")
        # Make sure the repo is cloned
        git_dir = self.git_opts["git_dir"]
        git_path = self.git_opts["git_path"]

        if not isdir(git_dir):
            mkdir(git_dir)
            command = "git clone {} {}".format(git_path, git_dir)
            self.execute(command)

    def publish(self):
        logger = logging.getLogger("gpod")
        git_dir = self.git_opts["git_dir"]

        command = "cd {} && git pull".format(git_dir)
        self.execute(command)

        # Commit and push
        command = "cd {} && git add . && git commit -m ':bento: Update preview' && git push -f".format(
            git_dir)
            
        self.execute(command)

    def move_files(self, pic_file_name):
        try:
            logger = logging.getLogger("gpod")

            dest_path = self.git_opts["git_dir"] + self.git_opts["git_sub_dir"]
            dest_pic = dest_path + "/photo.jpeg"
            dest_json = dest_path + "/description.json"
            dest_index_html = dest_path + "/index.html"

            if not isdir(dest_path):
                os.makedirs(dest_path)

            devices = [item.get("id")for item in self.settings["cameras"]]

            with open(self.git_opts["git_dir"] + "/devices.json", 'w') as outfile:
                json.dump(devices, outfile)

            shutil.copyfile(pic_file_name, dest_pic)
            shutil.copyfile(pic_file_name + ".json", dest_json)
            shutil.copyfile("index.html", dest_index_html)

        except Exception as ex:
            logging.error("Error: {}".format(ex))
            raise ex
