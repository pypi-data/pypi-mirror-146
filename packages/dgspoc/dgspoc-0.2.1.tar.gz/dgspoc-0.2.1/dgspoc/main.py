"""Module containing the logic for describe-get-system proof of conception entry-points."""

import sys
import re
import argparse

from dgspoc import version
from dgspoc.config import Data

from dgspoc.utils import Printer
from dgspoc.utils import Text

from dgspoc.constant import ECODE

from dgspoc.usage import get_global_usage
from dgspoc.usage import validate_usage
# from dgspoc.usage import show_usage
from dgspoc.usage import validate_example_usage

from dgspoc.operation import do_build_template
from dgspoc.operation import do_search_template
from dgspoc.operation import do_test_template
from dgspoc.operation import do_test_verification


class ArgumentParser(argparse.ArgumentParser):

    def parse_args(self, *args, **kwargs):
        try:
            options = super().parse_args(*args, **kwargs)
        except BaseException as ex:    # noqa
            if isinstance(ex, SystemExit):
                if ex.code == ECODE.SUCCESS:
                    sys.exit(ECODE.SUCCESS)
                else:
                    self.print_help()
                    sys.exit(ECODE.BAD)
            else:
                Printer.print_message('\n{}\n', Text(ex))
                self.print_help()
                sys.exit(ECODE.BAD)

        if options.help:
            if not options.command:
                self.print_help()
                sys.exit(ECODE.SUCCESS)
            else:
                if options.command in Cli.commands:
                    command = options.command
                    feature = options.operands[0].lower() if options.operands else ''
                    name = '{}_{}'.format(command, feature) if feature else command
                    validate_usage(name, ['usage'])
                else:
                    self.print_help()
                    sys.exit(ECODE.BAD)
        return options


def show_info(options):
    command, operands = options.command, options.operands
    if command == 'info':
        name = command
        validate_usage(command, operands)
        validate_example_usage(name, operands)

        op_txt = ' '.join(operands).lower()

        lst = []
        default_lst = [
            'Describe-Get-System Proof of Concept',
            Data.get_app_info()
        ]

        is_showed_all = options.all or re.search('all', op_txt)
        is_showed_dependency = options.dependency or re.search('depend', op_txt)
        is_showed_storage = options.template_storage or re.search('template|storage', op_txt)

        if is_showed_all:
            lst.extend(default_lst)

        if is_showed_all or is_showed_dependency:
            lst and lst.append('--------------------')
            for pkg in Data.get_dependency().values():
                lst.append('  + Package: {0[package]}'.format(pkg))
                lst.append('             {0[url]}'.format(pkg))

        if is_showed_all or is_showed_storage:
            lst and lst.append('--------------------', )
            lst.append(Data.get_template_storage_info())

        Printer.print(lst) if lst else Printer.print(default_lst)
        sys.exit(ECODE.SUCCESS)


def show_version(options):
    if options.command == 'version':
        print('{} v{}'.format(Cli.prog, version))
        sys.exit(ECODE.SUCCESS)


def show_global_usage(options):
    if options.command == 'usage':
        print(get_global_usage())
        sys.exit(ECODE.SUCCESS)


class Cli:
    """describe-get-system proof of concept console CLI application."""
    prog = 'dgs'
    prog_fn = 'describe-get-system'
    commands = ['build', 'info', 'run', 'search', 'test', 'version', 'usage']

    def __init__(self):
        # parser = argparse.ArgumentParser(
        parser = ArgumentParser(
            prog=self.prog,
            usage='%(prog)s [options] command operands',
            description='{} Proof of Concept'.format(self.prog_fn.title()),
            add_help=False
        )

        parser.add_argument(
            '-h', '--help', action='store_true',
            help='show this help message and exit'
        )

        parser.add_argument(
            '-v', '--version', action='version',
            version='%(prog)s v{}'.format(version)
        )

        parser.add_argument(
            '--author', type=str, default='',
            help="author's name"
        ),

        parser.add_argument(
            '--email', type=str, default='',
            help="author's email"
        ),

        parser.add_argument(
            '--company', type=str, default='',
            help="author's company"
        ),

        parser.add_argument(
            '--save-to', type=str, dest='filename', default='',
            help="saving to file"
        ),

        parser.add_argument(
            '--template-id', type=str, dest='tmplid', default='',
            help="template ID"
        ),

        parser.add_argument(
            '--test-file', type=str, dest='testfile', default='',
            help="test data file"
        ),

        parser.add_argument(
            '--adaptor', type=str, default='',
            help="connector adaptor"
        ),

        parser.add_argument(
            '--execution', type=str, default='',
            help="command line"
        ),

        parser.add_argument(
            '--select-statement', type=str, default='', dest='stmt',
            help='the select statement of verification'
        )

        parser.add_argument(
            '--replaced', action='store_true',
            help='overwrite template ID/file'
        )

        parser.add_argument(
            '--ignore-case', action='store_true', dest='ignore_case',
            help='case insensitive matching'
        )

        parser.add_argument(
            '--showed', action='store_true',
            help='showing result'
        )

        parser.add_argument(
            '--tabular', action='store_true',
            help='showing result in tabular format'
        )

        parser.add_argument(
            '--all', action='store_true',
            help='showing all information'
        )

        parser.add_argument(
            '--dependency', action='store_true',
            help='showing package dependency'
        )

        parser.add_argument(
            '--template-storage', action='store_true',
            help='showing template storage information'
        )

        parser.add_argument(
            'command', nargs='?', type=str, default='',
            help='command must be either build, '
                 'info, run, search, test, version, or usage'
        )
        parser.add_argument(
            'operands', nargs='*', type=str,
            help='operands can be template, unittest, '
                 'pytest, robotframework, script, or data such command-line, '
                 'config-lines, or filename'
        )

        self.kwargs = dict()
        self.parser = parser
        self.options = self.parser.parse_args()

    def validate_command(self):
        """Validate argparse `options.command`.

        Returns
        -------
        bool: show ``self.parser.print_help()`` and call ``sys.exit(ECODE.BAD)`` if
        command is neither build, info, run, search,
        test, version, nor usage otherwise, return True
        """
        self.options.command = self.options.command.lower()

        if self.options.command:
            if self.options.command in self.commands:
                return True
            else:
                self.parser.print_help()
                sys.exit(ECODE.BAD)
        return True

    def run(self):
        """Take CLI arguments, parse it, and process."""
        self.validate_command()

        show_version(self.options)
        show_global_usage(self.options)
        show_info(self.options)

        # operation
        do_build_template(self.options)
        do_search_template(self.options)
        do_test_template(self.options)

        do_test_verification(self.options)


def execute():
    """Execute template console CLI."""
    app = Cli()
    app.run()
