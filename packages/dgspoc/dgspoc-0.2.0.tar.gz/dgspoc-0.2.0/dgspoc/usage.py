"""Module containing the logic for console command line usage"""

import sys
import re
from enum import IntFlag

from dgspoc.utils import Printer
from dgspoc.utils import Misc

from dgspoc.constant import ECODE

from dgspoc import example
from dgspoc.example import get_number_of_example

tool = 'dgs'


class FLAG(IntFlag):
    AUTHOR = pow(2, 0)
    EMAIL = pow(2, 1)
    COMPANY = pow(2, 2)
    SAVE_TO = pow(2, 3)
    TEMPLATE_ID = pow(2, 4)
    TEST_FILE = pow(2, 5)
    ADAPTOR = pow(2, 6)
    EXECUTION = pow(2, 7)
    SELECT_STATEMENT = pow(2, 8)
    REPLACED = pow(2, 9)
    IGNORE_CASE = pow(2, 10)
    SHOWED = pow(2, 11)
    TABULAR = pow(2, 12)
    ALL = pow(2, 13)
    DEPENDENCY = pow(2, 14)
    TEMPLATE_STORAGE = pow(2, 15)
    HELP = pow(2, 16)

    BUILD_TEMPLATE = AUTHOR | EMAIL | COMPANY | SAVE_TO | TEMPLATE_ID | REPLACED | HELP
    SEARCH_TEMPLATE = IGNORE_CASE | SHOWED | HELP
    TEST_TEMPLATE = TEST_FILE | ADAPTOR | EXECUTION | SHOWED | TABULAR | HELP
    TEST_VERIFICATION = TEST_TEMPLATE | TEMPLATE_ID | SELECT_STATEMENT
    INFO_USAGE = ALL | DEPENDENCY | TEMPLATE_STORAGE | HELP


class UData:
    def __init__(self, *args, is_header=False):
        self.args = args
        lst = []
        if self.args:
            for arg in self.args:
                if Misc.is_list(arg):
                    lst.extend([str(item) for item in arg])
                else:
                    lst.append(str(arg))
            self.data = '\n'.join(lst)
            if is_header:
                self.data = '{0}\n{1}\n{0}'.format('+' * 80, self.data)
        else:
            self.data = ''

        if not self.data.strip():
            self.data = self.data.strip()

        self.data_len = len(self.data)

        self._count = len(lst)

    def __len__(self):
        return self.data_len

    def __repr__(self):
        return self.data

    def __str__(self):
        return self.data

    @property
    def count(self):
        return self._count


class UsageData(UData):
    def __init__(self, header_data, body_data):
        super().__init__(header_data, '{}\n'.format(body_data), is_header=False)
        self._count = body_data.count


class UHeaderData(UData):
    def __init__(self, *args):
        if len(args) > 1:
            item0 = args[0]
            lst = [item0, '-' * len(str(item0)), *args[1:]]
        else:
            lst = args
        super().__init__(*lst, is_header=True)


class UBodyData(UData):
    def __init__(self, *args):
        super().__init__(*args, is_header=False)


def get_usage_header(name, flags=0):
    name = str(name).lower()
    lst = ['{} {} usage'.format(tool, name.replace('_', ' '))]
    args = [
        "  --author AUTHOR         author's name",
        "  --email EMAIL           author's email",
        "  --company COMPANY       author's company",
        '  --save-to FILENAME      saving to file',
        '  --template-id TMPLID    template ID',
        '  --test-file TESTFILE    test data file',
        '  --adaptor ADAPTOR       connector adaptor',
        '  --execution EXECUTION   command line',
        '  --select-statement STMT the select statement for verification',
        '  --replaced              overwrite template ID/file',
        '  --ignore-case           case insensitive matching',
        '  --showed                showing result',
        '  --tabular               showing result in tabular format',
        '  --all                   showing all information',
        '  --dependency            showing package dependencies',
        '  --template-storage      showing template storage information',
        '  -h, --help              show this help message and exit',
    ]
    if flags:
        bits = list(map(int, list(bin(int(flags))[2:][::-1])))
        lst.append('optional arguments:')
        lst.append('-------------------')
        for index, bit in enumerate(bits):
            bit and lst.append(args[index])

    header_usage = UHeaderData(lst)
    return header_usage


def get_usage(name, flags=0):
    count = get_number_of_example(name)
    name = str(name).lower()
    header_usage = get_usage_header(name, flags=flags)

    lst = ['{} {} operands [options]'.format(tool, name.replace('_', ' '))]
    if count > 0:
        lst1 = list(map(str, range(1, count + 1)))
        s = lst1[0] if len(lst1) == 1 else '{%s}' % (','.join(lst1))
        lst.append('%s %s example %s' % (tool, name.replace('_', ' '), s))

    body_usage = UBodyData(*lst)

    usage = UsageData(header_usage, body_usage)
    return usage


def get_example_usage(name):
    count = get_number_of_example(name)
    name = str(name).lower()
    fmt = '{} {} example {}'

    example_usage = UsageData(
        UHeaderData('{} {} example syntax:'.format(tool, name.replace('_', ' '))),
        UBodyData(*[fmt.format(tool, name, i + 1) for i in range(count)])
    )
    return example_usage


class BuildTemplateUsage:
    usage = get_usage('build_template', flags=FLAG.BUILD_TEMPLATE)
    other_usage = get_usage('build_template', flags=FLAG.BUILD_TEMPLATE)
    example_usage = get_example_usage('build_template')


class BuildUsage:
    usage = '\n'.join([
        Printer.get('build command has two features: template or script'),
        str(BuildTemplateUsage.usage),
        '',
        # BuildScriptUsage.usage,
    ])


class InfoUsage:
    usage = get_usage('info', flags=FLAG.INFO_USAGE)
    other_usage = get_usage('info', flags=FLAG.INFO_USAGE)
    example_usage = get_example_usage('info')


class SearchTemplateUsage:
    usage = get_usage('search_template', flags=FLAG.SEARCH_TEMPLATE)
    other_usage = get_usage('search_template', flags=FLAG.SEARCH_TEMPLATE)
    example_usage = get_example_usage('search_template')


class TestTemplateUsage:
    usage = get_usage('test_template', flags=FLAG.TEST_TEMPLATE)
    other_usage = get_usage('test_template', flags=FLAG.TEST_TEMPLATE)
    example_usage = get_example_usage('test_template')


class TestVerificationUsage:
    usage = get_usage('test_verification', flags=FLAG.TEST_VERIFICATION)
    other_usage = get_usage('test_verification', flags=FLAG.TEST_VERIFICATION)
    example_usage = get_example_usage('test_verification')


class Usage:
    info = InfoUsage
    build = BuildUsage
    build_template = BuildTemplateUsage
    search_template = SearchTemplateUsage
    test_template = TestTemplateUsage
    test_verification = TestVerificationUsage


def validate_usage(name, operands):
    result = ''.join(operands) if Misc.is_list(operands) else str(operands)
    if result.strip().lower() == 'usage':
        show_usage(name, exit_code=ECODE.SUCCESS)


def show_usage(name, *args, exit_code=None):
    obj = getattr(Usage, name, None)
    if getattr(obj, 'usage', None):
        attr = '_'.join(list(args) + ['usage'])
        print(getattr(obj, attr))
        Misc.is_integer(exit_code) and sys.exit(exit_code)
    else:
        fmt = '*** ErrorUsage: "{}" has not defined or unavailable.'
        print(fmt.format(name))
        sys.exit(ECODE.BAD)


def validate_example_usage(name, operands):
    max_count = get_number_of_example(name)
    pattern = r'example *(?P<index>[0-9]+)$'
    txt = ' '.join(operands).strip().lower()
    m = re.match(pattern, txt)
    if m:
        index = m.group('index')
        if 1 <= int(index) <= max_count:
            cls_name = '{}Example'.format(name.title().replace('_', ''))
            cls = getattr(example, cls_name)
            result = cls.get(str(index))
            print('\n\n{}\n'.format(result))
            sys.exit(ECODE.SUCCESS)
        else:
            show_usage(name, 'example', exit_code=ECODE.BAD)
    else:
        if re.match('example', txt):
            show_usage(name, 'example', exit_code=ECODE.BAD)


def get_global_usage():
    lst = [
        UHeaderData('{} other usages'.format(tool)),
        UBodyData(
            '{} version'.format(tool),
        ),
        '',
        InfoUsage.usage,
        BuildTemplateUsage.usage,
        SearchTemplateUsage.usage,
        TestTemplateUsage.usage,
    ]

    return '\n'.join(str(item) for item in lst)
