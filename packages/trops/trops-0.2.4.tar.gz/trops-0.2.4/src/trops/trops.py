import os
import subprocess
import time
import argparse
import logging
import distutils.util
from configparser import ConfigParser
from textwrap import dedent
from pathlib import Path
from getpass import getuser
from socket import gethostname

from trops.utils import real_path, generate_sid
from trops.env import add_env_subparsers
from trops.file import add_file_subparsers
from trops.repo import add_repo_subparsers
from trops.capcmd import add_capture_cmd_subparsers
from trops.koumyo import add_koumyo_subparsers
from trops.init import add_init_subparsers
from trops.release import __version__


class Trops:
    """Trops Class"""

    def __init__(self, args, other_args):

        # Make args sharable among functions
        self.args = args
        self.other_args = other_args

        # Set username and hostname
        self.username = getuser()
        self.hostname = gethostname().split('.')[0]

        # Set trops_dir
        if os.getenv('TROPS_DIR'):
            self.trops_dir = real_path(os.getenv('TROPS_DIR'))
        else:
            print("TROPS_DIR has not been set")
            exit(1)

        # Create the log directory
        self.trops_log_dir = self.trops_dir + '/log'
        os.makedirs(self.trops_log_dir, exist_ok=True)

        # Set trops_sid
        if os.getenv('TROPS_SID'):
            self.trops_sid = os.getenv('TROPS_SID')
        else:
            self.trops_sid = False

        if os.getenv('TROPS_TAGS'):
            self.trops_tags = os.getenv('TROPS_TAGS')
        else:
            self.trops_tags = False

        # Set trops_env
        if hasattr(args, 'env') and args.env:
            self.trops_env = args.env
        elif os.getenv('TROPS_ENV'):
            self.trops_env = os.getenv('TROPS_ENV')
        else:
            self.trops_env = False

        self.config = ConfigParser()
        if self.trops_dir:
            self.conf_file = self.trops_dir + '/trops.cfg'
            if os.path.isfile(self.conf_file):
                self.config.read(self.conf_file)

                if self.config.has_section(self.trops_env):
                    try:
                        self.git_dir = real_path(
                            self.config[self.trops_env]['git_dir'])
                    except KeyError:
                        print('git_dir does not exist in your configuration file')
                        exit(1)
                    try:
                        self.work_tree = real_path(
                            self.config[self.trops_env]['work_tree'])
                    except KeyError:
                        print('work_tree does not exist in your configuration file')
                        exit(1)

                    self.git_cmd = ['git', '--git-dir=' + self.git_dir,
                                    '--work-tree=' + self.work_tree]

                    try:
                        self.sudo = distutils.util.strtobool(
                            self.config[self.trops_env]['sudo'])
                        if self.sudo:
                            self.git_cmd = ['sudo'] + self.git_cmd
                    except KeyError:
                        pass

                    if 'logfile' in self.config[self.trops_env]:
                        self.trops_logfile = real_path(
                            self.config[self.trops_env]['logfile'])
                    else:
                        self.trops_logfile = self.trops_log_dir + '/trops.log'

            logging.basicConfig(format=f'%(asctime)s { self.username }@{ self.hostname } %(levelname)s %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S',
                                filename=self.trops_logfile,
                                level=logging.DEBUG)
            self.logger = logging.getLogger()


class TropsMain(Trops):

    def __init__(self, args, other_args):
        super().__init__(args, other_args)

    def git(self):
        """Git wrapper command"""

        cmd = self.git_cmd + self.other_args
        subprocess.call(cmd)

    def check(self):
        """Git status wrapper command"""

        cmd = self.git_cmd + ['status']
        subprocess.call(cmd)

    def ll(self):
        """Shows the list of git-tracked files"""

        dirs = self.args.dirs
        for dir in dirs:
            if os.path.isdir(dir):
                os.chdir(dir)
                cmd = self.git_cmd + ['ls-files']
                output = subprocess.check_output(cmd)
                for f in output.decode("utf-8").splitlines():
                    cmd = ['ls', '-al', f]
                    subprocess.call(cmd)

    def show(self):
        """trops show hash[:path]"""

        cmd = self.git_cmd + ['show', self.args.commit]
        subprocess.call(cmd)

    def _follow(self, file):

        file.seek(0, os.SEEK_END)
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

    def log(self):

        log_file = self.trops_logfile
        numlines = 15
        if self.args.tail and self.args.tail != None:
            numlines = self.args.tail

        if self.args.all:
            with open(log_file) as ff:
                for line in ff.readlines():
                    print(line, end='')
        else:
            with open(log_file) as ff:
                for line in ff.readlines()[-numlines:]:
                    print(line, end='')
        if self.args.follow:
            ff = open(log_file, "r")
            try:
                lines = self._follow(ff)
                for line in lines:
                    print(line, end='')
            except KeyboardInterrupt:
                print('\nClosing trops log...')

    def touch(self):

        for file_path in self.args.paths:

            self._touch_file(file_path)

    def _touch_file(self, file_path):
        """Add a file or directory in the git repo"""

        file_path = real_path(file_path)

        # Check if the path exists
        if not os.path.exists(file_path):
            print(f"{ file_path } doesn't exists")
            exit(1)
        # TODO: Allow touch directory later
        if not os.path.isfile(file_path):
            message = f"""\
                Error: { file_path } is not a file
                Only file is allowed to be touched"""
            print(dedent(message))
            exit(1)

        # Check if the path is in the git repo
        cmd = self.git_cmd + ['ls-files', file_path]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            print(result.stderr.decode('utf-8'))
            exit(result.returncode)
        output = result.stdout.decode('utf-8')
        # Set the message based on the output
        if output:
            git_msg = f"Update { file_path }"
            log_note = "UPDATE"
        else:
            git_msg = f"Add { file_path }"
            log_note = "ADD"
        if self.trops_tags:
            git_msg = f"{ git_msg } ({ self.trops_tags })"
        # Add and commit
        cmd = self.git_cmd + ['add', file_path]
        subprocess.call(cmd)
        cmd = self.git_cmd + ['commit', '-m', git_msg, file_path]
        subprocess.call(cmd)
        cmd = self.git_cmd + ['log', '--oneline', '-1', file_path]
        output = subprocess.check_output(
            cmd).decode("utf-8").split()
        if file_path in output:
            env = self.trops_env
            commit = output[0]
            path = real_path(file_path).lstrip(self.work_tree)
            mode = oct(os.stat(file_path).st_mode)[-4:]
            owner = Path(file_path).owner()
            group = Path(file_path).group()
            message = f"FL trops show -e { env } { commit }:{ path }  #> { log_note } O={ owner },G={ group },M={ mode }"
            if self.trops_sid:
                message = message + f" TROPS_SID={ self.trops_sid }"
            message = message + f" TROPS_ENV={ env }"
            self.logger.info(message)

    def drop(self):

        for file_path in self.args.paths:

            self._drop_file(file_path)

    def _drop_file(self, file_path):
        """Remove a file from the git repo"""

        file_path = real_path(file_path)

        # Check if the path exists
        if not os.path.exists(file_path):
            print(f"{ file_path } doesn't exists")
            exit(1)
        # TODO: Allow touch directory later
        if not os.path.isfile(file_path):
            message = f"""\
                Error: { file_path } is not a file.
                A directory is not allowed to say goodbye"""
            print(dedent(message))
            exit(1)

        # Check if the path is in the git repo
        cmd = self.git_cmd + ['ls-files', file_path]
        output = subprocess.check_output(cmd).decode("utf-8")
        # Set the message based on the output
        if output:
            cmd = self.git_cmd + ['rm', '--cached', file_path]
            subprocess.call(cmd)
            message = f"Goodbye { file_path }"
            cmd = self.git_cmd + ['commit', '-m', message]
            subprocess.call(cmd)
        else:
            message = f"{ file_path } is not in the git repo"
            exit(1)
        cmd = self.git_cmd + ['log', '--oneline', '-1', file_path]
        output = subprocess.check_output(
            cmd).decode("utf-8").split()
        message = f"FL trops show -e { self.trops_env } { output[0] }:{ real_path(file_path).lstrip('/')}  #> BYE BYE"
        if self.trops_sid:
            message = message + f" TROPS_SID={ self.trops_sid }"
        message = message + f" TROPS_ENV={ self.trops_env }"
        self.logger.info(message)


def trops_git(args, other_args):

    tr = TropsMain(args, other_args)
    tr.git()


def trops_check(args, other_args):

    tr = TropsMain(args, other_args)
    tr.check()


def trops_ll(args, other_args):

    tr = TropsMain(args, other_args)
    tr.ll()


def trops_show(args, other_args):

    tr = TropsMain(args, other_args)
    tr.show()


def trops_log(args, other_args):

    tr = TropsMain(args, other_args)
    tr.log()


def trops_touch(args, other_args):

    tr = TropsMain(args, other_args)
    tr.touch()


def trops_drop(args, other_args):

    tr = TropsMain(args, other_args)
    tr.drop()


def add_git_subparsers(subparsers):

    parser_git = subparsers.add_parser('git', help='git wrapper')
    parser_git.add_argument('-s', '--sudo', help="Use sudo",
                            action='store_true')
    parser_git.add_argument('-e', '--env', help="Set env")
    parser_git.set_defaults(handler=trops_git)


def add_show_subparsers(subparsers):

    parser_show = subparsers.add_parser(
        'show', help='trops show commit[:path]')
    parser_show.add_argument('-e', '--env', help="Set env")
    parser_show.add_argument('commit', help='Set commit[:path]')
    parser_show.set_defaults(handler=trops_show)


def add_log_subparsers(subparsers):

    parser_log = subparsers.add_parser('log', help='show log')
    parser_log.add_argument(
        '-t', '--tail', type=int, help='set number of lines to show')
    parser_log.add_argument(
        '-f', '--follow', action='store_true', help='follow log interactively')
    parser_log.add_argument(
        '-a', '--all', action='store_true', help='show all log')
    parser_log.set_defaults(handler=trops_log)


def add_ll_subparsers(subparsers):

    parser_ll = subparsers.add_parser('ll', help="list files")
    parser_ll.add_argument(
        'dirs', help='directory path', nargs='*', default=[os.getcwd()])
    parser_ll.add_argument(
        '-e', '--env', help='Set environment name')
    parser_ll.set_defaults(handler=trops_ll)


def add_touch_subparsers(subparsers):

    parser_touch = subparsers.add_parser(
        'touch', help="add/update file in the git repo")
    parser_touch.add_argument('paths', nargs='+', help='path of file')
    parser_touch.set_defaults(handler=trops_touch)


def add_drop_subparsers(subparsers):

    parser_drop = subparsers.add_parser(
        'drop', help="remove file from the git repo")
    parser_drop.add_argument('paths', nargs='+', help='path of file')
    parser_drop.set_defaults(handler=trops_drop)


def add_gensid_subparsers(subparsers):

    parser_gensid = subparsers.add_parser(
        'gensid', help='generate sid')
    parser_gensid.set_defaults(handler=generate_sid)


def add_check_subparsers(subparsers):

    parser_check = subparsers.add_parser('check', help='Check status')
    parser_check.add_argument('-s', '--sudo', help="Use sudo",
                              action='store_true')
    parser_check.add_argument('-e', '--env', help="Set env")
    parser_check.set_defaults(handler=trops_check)


def main():

    parser = argparse.ArgumentParser(prog='trops',
                                     description='Trops - Tracking Operations')
    subparsers = parser.add_subparsers()
    parser.add_argument('-v', '--version', action='version',
                        version=f'%(prog)s {__version__}')

    for func in [
        'init',
        'env',
        'file',
        'koumyo',
        'repo',
        'git',
        'show',
        'capture_cmd',
        'log',
        'll',
        'touch',
        'drop',
        'gensid',
        'check'
    ]:
        eval(f'add_{ func }_subparsers(subparsers)')

    # Pass args and other args to the hander
    args, other_args = parser.parse_known_args()
    if hasattr(args, 'handler'):
        args.handler(args, other_args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
