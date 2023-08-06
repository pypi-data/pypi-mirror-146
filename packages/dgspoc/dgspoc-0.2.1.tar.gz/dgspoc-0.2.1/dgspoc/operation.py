"""Module containing the logic for describe-get-system operation"""

import sys
import re
import argparse

from dgspoc.utils import File
from dgspoc.utils import Printer
from dgspoc.utils import Text
from dgspoc.utils import DictObject

from dgspoc.constant import ECODE

from dgspoc.storage import TemplateStorage

from dgspoc.usage import validate_usage
from dgspoc.usage import validate_example_usage
from dgspoc.usage import show_usage

from dgspoc.adaptor import Adaptor

from templateapp import TemplateBuilder

from io import StringIO
from textfsm import TextFSM
from pprint import pprint
from dlapp.collection import Tabular


def do_build_template(options):
    command, operands = options.command, list(options.operands)
    op_count = len(operands)
    feature = str(operands[0]).lower().strip() if op_count > 0 else ''
    if command == 'build' and feature == 'template':
        operands = operands[1:]
        name = '{}_{}'.format(command, feature)
        validate_usage(name, operands)
        validate_example_usage(name, operands)

        op_txt = ' '.join(operands).rstrip()

        if not op_txt:
            show_usage(name, exit_code=ECODE.BAD)

        if File.is_exist(op_txt):
            with open(op_txt) as stream:
                user_data = stream.read()
        else:
            user_data = op_txt

        try:
            factory = TemplateBuilder(
                user_data=user_data, author=options.author, email=options.email,
                company=options.company
            )

            template_id = options.tmplid.strip()
            filename = options.filename.strip()

            fmt1 = '+++ Successfully uploaded generated template to "{}" template ID.'
            fmt2 = '+++ Successfully saved generated template to {}'
            fmt3 = 'CANT save generated template to existing {} file.  Use replaced flag accordingly.'

            if template_id or filename:
                is_ok = True
                lst = []
                if template_id:
                    is_uploaded = TemplateStorage.upload(
                        template_id, factory.template, replaced=options.replaced
                    )
                    is_ok &= is_uploaded
                    msg = fmt1.format(template_id) if is_uploaded else TemplateStorage.message
                    lst.append(msg)
                if filename:
                    filename = File.get_path(filename)
                    if File.is_exist(filename) and not options.replaced:
                        msg = fmt3.format(filename)
                        is_ok &= False
                    else:
                        is_saved = File.save(options.filename, factory.template)
                        is_ok &= is_saved
                        msg = fmt2.format(filename) if is_saved else File.message

                    lst and lst.append('=' * 20)
                    lst.append(msg)

                lst and Printer.print(lst)
                sys.exit(ECODE.SUCCESS if is_ok else ECODE.BAD)
            else:
                print(factory.template)
                sys.exit(ECODE.SUCCESS)

        except Exception as ex:
            print(Text(ex))
            sys.exit(ECODE.BAD)

    elif command == 'build' and feature != 'template':
        if feature == 'script':
            return
        else:
            exit_code = ECODE.SUCCESS if feature == 'usage' else ECODE.BAD
            show_usage(command, exit_code=exit_code)


def do_search_template(options):
    command, operands = options.command, list(options.operands)
    op_count = len(operands)
    feature = str(operands[0]).lower().strip() if op_count > 0 else ''
    if command == 'search' and feature == 'template':
        operands = operands[1:]
        name = '{}_{}'.format(command, feature)
        validate_usage(name, operands)
        validate_example_usage(name, operands)

        op_txt = ' '.join(operands).rstrip()

        if not op_txt:
            show_usage(name, exit_code=ECODE.BAD)

        tmpl_id_pattern = operands[0]
        is_found = TemplateStorage.search(tmpl_id_pattern,
                                          ignore_case=options.ignore_case,
                                          showed=options.showed)
        print(TemplateStorage.message)
        sys.exit(ECODE.SUCCESS if is_found else ECODE.BAD)

    elif command == 'search' and feature != 'template':
        exit_code = ECODE.SUCCESS if feature == 'usage' else ECODE.BAD
        show_usage('{}_template'.format(command), exit_code=exit_code)


def validate_test_data_flag(options):
    command = options.command
    feature = options.operands[0] if options.operands else ''
    if options.testfile == '' and options.adaptor == '':
        lst = ['CANT run {} test WITHOUT test data.'.format(feature),
               'Please use --test-file=<test-file-name> or',
               '           --adaptor=<adaptor_name> --execution="<device cmdline>"']
        Printer.print(lst)
        show_usage('{}_{}'.format(command, feature), exit_code=ECODE.BAD)


def get_test_from_adaptor(options):
    command = options.command
    feature = options.operands[0] if options.operands else ''
    name = '{}_{}'.format(command, feature)
    execution = options.execution.strip()
    if not execution:
        lst = [
            'ExecutionSyntaxError: must be',
            '--execution="--host=<addr_or_name> <cmdline>"',
            '--execution="--host=<addr_or_name> --test_case=<testcase_name> <cmdline>"'
        ]
        Printer.print(lst)
        show_usage(name, exit_code=ECODE.BAD)

    try:

        lst = execution.split(' ')

        parser = argparse.ArgumentParser(exit_on_error=False)
        parser.add_argument('items', nargs='*')
        parser.add_argument('--host', type=str, default='')
        parser.add_argument('--testcase', type=str, default='')
        parser.add_argument('other_items', nargs='*')
        parser_args = parser.parse_args(lst)

        host = parser_args.host
        testcase = parser_args.testcase
        cmdline = ' '.join(parser_args.items + parser_args.other_items)

        if not parser_args.host:
            lst = [
                'ExecutionSyntaxError: must be',
                '--execution="--host=<addr_or_name> <cmdline>"',
                '--execution="--host=<addr_or_name> --test_case=<testcase_name> <cmdline>"'
            ]
            Printer.print(lst)
            show_usage(name, exit_code=ECODE.BAD)

        device = Adaptor(options.adaptor, host, testcase=testcase)
        device.connect()
        test_data = device.execute(cmdline)
        device.disconnect()
        device.release()
        return test_data
    except Exception as ex:
        failure = 'AdaptorInquiryError - ({})'.format(Text(ex))
        Printer.print(failure)
        sys.exit(ECODE.BAD)


def get_test_data_from_provided_file(options):
    if File.is_exist(options.testfile):
        test_data = open(options.testfile).read()
        return test_data
    else:
        fmt = '*** "{}" test data file is NOT existed.'
        failure = fmt.format(options.testfile)
        Printer.print(failure)
        sys.exit(ECODE.BAD)


def get_test_data(options):
    validate_test_data_flag(options)
    test_data = ''
    if options.adaptor:
        test_data = get_test_from_adaptor(options)
    elif options.testfile:
        test_data = get_test_data_from_provided_file(options)
    return test_data


def get_parsed_result(options, test_data):

    command = options.command
    feature = options.operands[0] if options.operands else ''
    name = '{}_{}'.format(command, feature)

    tmpl_ref = options.tmplid
    if not tmpl_ref:
        tmpl_ref = options.operands[1] if len(options.operands) > 1 else ''

    if not tmpl_ref:
        show_usage(name, exit_code=ECODE.BAD)

    template = ''
    if TemplateStorage.check(tmpl_ref):
        template = TemplateStorage.get(tmpl_ref)
    elif File.is_exist(tmpl_ref):
        template = open(tmpl_ref).read()

    if not template:
        lst = [
            '"{}" is NOT template ID or template filename.'.format(tmpl_ref),
            'Please provide the valid template_id or template_file'
        ]
        Printer.print(lst)
        sys.exit(ECODE.BAD)

    try:
        stream = StringIO(template)
        parser = TextFSM(stream)
        rows = parser.ParseTextToDicts(test_data)

        result = DictObject(
            test_data=test_data, template=template,
            records=rows, records_count=len(rows)
        )
        return result
    except Exception as ex:
        failure = 'BAD-TEMPLATE ({})'.format(Text(ex))
        Printer.print(failure)
        sys.exit(ECODE.BAD)


def do_test_template(options):
    command, operands = options.command, list(options.operands)
    op_count = len(operands)
    feature = str(operands[0]).lower().strip() if op_count > 0 else ''
    if command == 'test' and feature == 'template':
        operands = operands[1:]
        name = '{}_{}'.format(command, feature)
        validate_usage(name, operands)
        validate_example_usage(name, operands)

        op_txt = ' '.join(operands).rstrip()
        if op_txt == options.tmplid and not options.tmplid:
            show_usage(name, exit_code=ECODE.BAD)

        test_data = get_test_data(options)
        result = get_parsed_result(options, test_data)

        if options.showed:
            Printer.print('Test Data:')
            print(result.test_data)     # noqa
            print()
            Printer.print('Template:')
            print(result.template)      # noqa
            print()

        lst = ['Result:']
        if result.records_count:        # noqa
            fmt = '+++ Template parsed {} record(s).'
            lst.append(fmt.format(result.records_count))    # noqa
        else:
            lst.append('*** Template could NOT find and parse any record.')
        Printer.print(lst)

        records = result.records        # noqa
        records and Tabular(records).print() if options.tabular else pprint(records)
        sys.exit(ECODE.SUCCESS if result.records_count > 0 else ECODE.BAD)  # noqa

    elif command == 'test' and feature != 'template':
        if feature == 'verification':
            return
        exit_code = ECODE.SUCCESS if feature == 'usage' else ECODE.BAD
        show_usage('{}_template'.format(command), exit_code=exit_code)


def do_test_verification(options):
    command, operands = options.command, list(options.operands)
    op_count = len(operands)
    feature = str(operands[0]).lower().strip() if op_count > 0 else ''
    if command == 'test' and feature == 'verification':
        operands = operands[1:]
        name = '{}_{}'.format(command, feature)
        validate_usage(name, operands)
        validate_example_usage(name, operands)

        select_stmt = options.stmt.strip() or ' '.join(operands).rstrip()
        if not select_stmt:
            show_usage(name, exit_code=ECODE.BAD)

        test_data = get_test_data(options)
        result = get_parsed_result(options, test_data)

        if options.showed:
            Printer.print('Test Data:')
            print(result.test_data)     # noqa
            print()
            Printer.print('Template:')
            print(result.template)      # noqa
            print()

        lst = ['Result:']
        if result.records_count:        # noqa
            fmt = '+++ Template parsed {} record(s).'
            lst.append(fmt.format(result.records_count))    # noqa
        else:
            lst.append('*** Verification could NOT find and parse any record.')
        Printer.print(lst)

        if result.records_count:        # noqa
            Printer.print('Select Statement:')
            print(select_stmt)

            items = re.split('(?i) *must *be *', select_stmt)
            print(items)

        else:
            Printer.print(
                ['Results:',
                 '*** Verification could NOT find and parse any record.']
            )
            sys.exit(ECODE.BAD)

    elif command == 'test' and feature != 'verification':
        if feature == 'template':
            return
        exit_code = ECODE.SUCCESS if feature == 'usage' else ECODE.BAD
        show_usage('{}_template'.format(command), exit_code=exit_code)
