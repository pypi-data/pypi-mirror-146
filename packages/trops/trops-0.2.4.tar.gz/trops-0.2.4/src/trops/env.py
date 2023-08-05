import os
import subprocess
from shutil import rmtree
from configparser import ConfigParser
from socket import gethostname

from trops.utils import real_path, yes_or_no


class TropsEnv:

    def __init__(self, args, other_args):

        if other_args:
            msg = f"""\
                Unsupported argments: { ', '.join(other_args)}
                > trops env <subcommand> --help"""
            print(dedent(msg))
            exit(1)

        self.trops_args = args

        if hasattr(args, 'dir'):
            self.trops_dir = real_path(args.dir) + '/trops'
        elif 'TROPS_DIR' in os.environ:
            self.trops_dir = real_path('$TROPS_DIR')
        else:
            print('TROPS_DIR does not exists')
            exit(1)

        if hasattr(args, 'work_tree'):
            self.trops_work_tree = args.work_tree

        if hasattr(args, 'git_remote'):
            self.trops_git_remote = args.git_remote
        else:
            self.trops_git_remote = None

        if hasattr(args, 'env') and args.env:
            self.trops_env = args.env
        elif os.getenv('TROPS_ENV'):
            self.trops_env = os.getenv('TROPS_ENV')
        else:
            self.trops_env = gethostname().split('.')[0]

        if hasattr(args, 'git_dir') and args.git_dir:
            self.trops_git_dir = args.git_dir
        else:
            self.trops_git_dir = self.trops_dir + \
                f'/repo/{ self.trops_env }.git'

        self.trops_conf = self.trops_dir + '/trops.cfg'
        self.trops_log_dir = self.trops_dir + '/log'

    def _setup_dirs(self):

        # Create trops_dir
        try:
            os.makedirs(self.trops_dir, exist_ok=True)
        except FileExistsError:
            print(f"{ self.trops_dir } already exists")

        # Create trops_dir/log
        try:
            os.mkdir(self.trops_log_dir)
        except FileExistsError:
            print(f'{ self.trops_log_dir} already exists')

        # Create trops_dir/repo
        repo_dir = f"{self.trops_dir}/repo"
        try:
            os.mkdir(repo_dir)
        except FileExistsError:
            print(f'{ repo_dir } already exists')

    def _setup_trops_conf(self):

        config = ConfigParser()
        if os.path.isfile(self.trops_conf):
            config.read(self.trops_conf)
            if config.has_section(self.trops_env):
                print(
                    f"The '{ self.trops_env }' environment already exists on { self.trops_conf }")
                exit(1)

        config[self.trops_env] = {'git_dir': f'$TROPS_DIR/repo/{ self.trops_env }.git',
                                  'sudo': 'False',
                                  'work_tree': f'{ self.trops_work_tree}'}
        if self.trops_git_remote:
            config[self.trops_env]['git_remote'] = self.trops_git_remote
        with open(self.trops_conf, mode='w') as configfile:
            config.write(configfile)

    def _setup_bare_git_repo(self):

        # Create trops's bare git directory
        if not os.path.isdir(self.trops_git_dir):
            cmd = ['git', 'init', '--bare', self.trops_git_dir]
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode == 0:
                print(result.stdout.decode('utf-8'))
            else:
                print(result.stderr.decode('utf-8'))
                exit(result.returncode)

        # Prepare for updating trops.git/config
        git_cmd = ['git', '--git-dir=' + self.trops_git_dir]
        git_conf = ConfigParser()
        git_conf.read(self.trops_git_dir + '/config')
        # Set "status.showUntrackedFiles no" locally
        if not git_conf.has_option('status', 'showUntrackedFiles'):
            cmd = git_cmd + ['config', '--local',
                             'status.showUntrackedFiles', 'no']
            subprocess.call(cmd)
        # Set $USER as user.name
        if not git_conf.has_option('user', 'name'):
            username = os.environ['USER']
            cmd = git_cmd + ['config', '--local', 'user.name', username]
            subprocess.call(cmd)
        # Set $USER@$HOSTNAME as user.email
        if not git_conf.has_option('user', 'email'):
            useremail = username + '@' + os.uname().nodename
            cmd = git_cmd + ['config', '--local', 'user.email', useremail]
            subprocess.call(cmd)

        # TODO: branch name should become an option, too
        # Set branch name as trops
        cmd = git_cmd + ['branch', '--show-current']
        branch_name = subprocess.check_output(cmd).decode("utf-8")
        new_branch_name = 'trops/' + self.trops_env
        if new_branch_name not in branch_name:
            cmd = git_cmd + ['--work-tree=/',
                             'checkout', '-b', new_branch_name]
            subprocess.call(cmd)

    def create(self):

        self._setup_dirs()
        self._setup_trops_conf()
        self._setup_bare_git_repo()

    def delete(self):

        config = ConfigParser()
        if os.path.isfile(self.trops_conf):
            config.read(self.trops_conf)
            if config.has_section(self.trops_env):
                if yes_or_no(f"Really want to remove { self.trops_env } from { self.trops_conf }?"):
                    config.remove_section(self.trops_env)
                    print(
                        f"Deleting { self.trops_env } from { self.trops_conf }..")
                    with open(self.trops_conf, mode='w') as configfile:
                        config.write(configfile)

        # Check if the self.trops_git_dir ends with .git
        dirname = os.path.basename(self.trops_git_dir)
        if dirname[-4:] == '.git':
            really_ok1 = True
        else:
            really_ok1 = False

        # Check if self.trops_git_dir/config
        # has_option('status', 'showUntrackedFiles')
        git_config_file = f"{ self.trops_git_dir }/config"
        git_config = ConfigParser()
        if os.path.isfile(git_config_file):
            git_config.read(git_config_file)
            if git_config.has_option('status', 'showUntrackedFiles'):
                really_ok2 = True
            else:
                really_ok2 = False

        # then delete it
        if really_ok1 and really_ok2:
            if yes_or_no(f"Really want to delete { self.trops_git_dir }?"):
                rmtree(self.trops_git_dir)
                print(f"Deleting { self.trops_git_dir }..")

    def update(self):

        config = ConfigParser()
        if os.path.isfile(self.trops_conf):
            config.read(self.trops_conf)
            if not config.has_section(self.trops_env):
                print(
                    f"The '{ self.trops_env }' environment does not exists on { self.trops_conf }")
                exit(1)

        config[self.trops_env]['git_dir'] = self.trops_git_dir
        config[self.trops_env]['sudo'] = 'False'
        config[self.trops_env]['work_tree'] = self.trops_work_tree
        if self.trops_git_remote:
            config[self.trops_env]['git_remote'] = self.trops_git_remote
        with open(self.trops_conf, mode='w') as configfile:
            config.write(configfile)

    def list(self):

        config = ConfigParser()
        config.read(self.trops_conf)
        current_env = self.trops_env

        for envname in config.sections():
            if envname == 'active':
                pass
            elif envname == current_env:
                print(f'- { envname }*')
            else:
                print(f'- { envname}')

    def show(self):

        print('ENV')
        try:
            print(f"  TROPS_DIR = {os.environ['TROPS_DIR']}")
        except KeyError:
            print(f"  {os.environ['TROPS_DIR']} = None")
            exit(1)
        try:
            print(f"  TROPS_ENV = {os.environ['TROPS_ENV']}")
            trops_env = os.environ['TROPS_ENV']
        except KeyError:
            print('  TROPS_ENV = None')
            trops_env = 'default'
        print(f"  TROPS_SID = {os.environ['TROPS_SID']}")

        config = ConfigParser()
        config.read(self.trops_conf)
        print('Git')
        if config.has_option(trops_env, 'git_dir'):
            print(f"  git-dir = { config.get(trops_env, 'git_dir') }")
        if config.has_option(trops_env, 'work_tree'):
            print(f"  work-tree = { config.get(trops_env, 'work_tree') }")
        if config.has_option(trops_env, 'git_remote'):
            print(f"  git_remote = { config.get(trops_env, 'git_remote') }")
        if config.has_option(trops_env, 'logfile'):
            print(f"  logfile = { config.get(trops_env, 'logfile') }")
        else:
            print(f"  logfile = $TROPS_DIR/log/trops.log")


def env_create(args, other_args):
    """Setup trops project"""

    trenv = TropsEnv(args, other_args)
    trenv.create()


def env_delete(args, other_args):
    """Setup trops project"""

    trenv = TropsEnv(args, other_args)
    trenv.delete()


def env_show(args, other_args):

    trenv = TropsEnv(args, other_args)
    trenv.show()


def env_update(args, other_args):

    trenv = TropsEnv(args, other_args)
    trenv.update()


def env_list(args, other_args):

    trenv = TropsEnv(args, other_args)
    trenv.list()


def add_env_subparsers(subparsers):

    # trops env
    parser_env = subparsers.add_parser(
        'env', help='initialize trops environment')
    env_subparsers = parser_env.add_subparsers()
    # trops env show
    perser_env_show = env_subparsers.add_parser(
        'show', help='show current environment')
    perser_env_show.set_defaults(handler=env_show)
    # trops env list
    perser_env_list = env_subparsers.add_parser(
        'list', help='show list of environment')
    perser_env_list.set_defaults(handler=env_list)
    # trops env create <env>
    parser_env_create = env_subparsers.add_parser(
        'create', help='create trops environment')
    parser_env_create.add_argument(
        '-w', '--work-tree', default='/', help='Set work-tree (default: %(default)s)')
    parser_env_create.add_argument(
        'env', help='Set environment name (default: %(default)s)')
    parser_env_create.add_argument(
        '--git-remote', help='Remote git repository')
    parser_env_create.set_defaults(handler=env_create)
    # trops env delete <env>
    parser_env_delete = env_subparsers.add_parser(
        'delete', help='delete trops environment')
    parser_env_delete.add_argument(
        'env', help='Set environment name (default: %(default)s)')
    parser_env_delete.set_defaults(handler=env_delete)
    # trops env update
    parser_env_update = env_subparsers.add_parser(
        'update', help='update trops environment')
    parser_env_update.add_argument(
        '-w', '--work-tree', default='/', help='work-tree')
    parser_env_update.add_argument(
        '-g', '--git-dir', help='git-dir')
    parser_env_update.add_argument(
        '--git-remote', help='Remote git repository')
    parser_env_update.add_argument(
        '--logfile', help='Path of log file')
    parser_env_update.add_argument(
        '-e', '--env', help='Set environment name')
    parser_env_update.set_defaults(handler=env_update)
    # TODO: Add trops deactivate
