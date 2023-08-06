"""Module containing the logic for describe-get-system to interpret
user describing problem"""


import re
import operator
import yaml

from textwrap import indent

from dgspoc.utils import DictObject
from dgspoc.utils import Misc
from dgspoc.utils import File
from dgspoc.utils import Text

from dgspoc.constant import FWTYPE

from dgspoc.exceptions import NotImplementedFrameworkError
from dgspoc.exceptions import ComparisonOperatorError
from dgspoc.exceptions import ConnectDataStatementError
from dgspoc.exceptions import UseTestcaseStatementError
from dgspoc.exceptions import ConnectDeviceStatementError


class ScriptInfo(DictObject):
    def __init__(self, *args, testcase='', **kwargs):
        super().__init__(*args, **kwargs)
        self.testcase = testcase
        self.variables = DictObject(
            test_resource_var='test_resource', test_resource_ref='',
            test_data_var='test_data'
        )

    def get_class_name(self):
        node = self.get(self.testcase)
        cls_name = node.get('class_name', 'TestClass') if node else 'TestClass'
        return cls_name

    def get_method_name(self, value):
        node = self.get(self.testcase)
        if node:
            for method_name, val in node.items():
                if val == value:
                    return method_name
            else:
                return 'test_step'

    def clear_devices_vars(self):
        setattr(self, 'devices_vars', DictObject())

    def reset_global_vars(self):
        self.variables = DictObject(
            test_resource_var='test_resource', test_resource_ref='',
            test_data_var='test_data'
        )


SCRIPTINFO = ScriptInfo()


class Statement:
    def __init__(self, data, parent=None, framework='', indentation=4):
        self.data = data
        self.prev = None
        self.next = None
        self.current = None
        self.parent = parent
        self.framework = str(framework).strip()
        self._children = []
        self._name = ''
        self._is_parsed = False

        self._stmt_data = ''
        self._remaining_data = ''

        self._prev_spacers = ''
        self._spacers = ''
        self._level = 0
        self.indentation = indentation

        self.spacer_pattern = r'(?P<spacers> *)[^ ].*'

        self.validate_framework()
        self.prepare()

    def __len__(self):
        return 1 if self.name != '' else 0

    @property
    def is_parsed(self):
        return self._is_parsed

    @property
    def name(self):
        return self._name

    @property
    def children(self):
        return self._children

    @property
    def level(self):
        return self._level

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def is_empty(self):
        return self.data.strip() == ''

    @property
    def is_statement(self):
        return self._name != ''

    @property
    def statement_data(self):
        return self._stmt_data

    @property
    def remaining_data(self):
        return self._remaining_data

    @property
    def is_setup_statement(self):
        pattern = r'setup'
        is_matched = self.is_matched_statement(pattern)
        return is_matched

    @property
    def is_teardown_statement(self):
        pattern = r'cleanup|teardown'
        is_matched = self.is_matched_statement(pattern)
        return is_matched

    @property
    def is_section_statement(self):
        pattern = r'section'
        is_matched = self.is_matched_statement(pattern)
        return is_matched

    @property
    def is_base_statement(self):
        is_base_stmt = self.is_setup_statement
        is_base_stmt |= self.is_section_statement
        is_base_stmt |= self.is_teardown_statement
        return is_base_stmt

    def is_matched_statement(self, pat, data=None):
        data = data or [self.name, self.statement_data]
        lst = data if Misc.is_list(data) else [data]
        is_matched = any(bool(re.match(pat, str(item), re.I)) for item in lst)
        return is_matched

    def prepare(self):
        if self.is_empty:
            self._stmt_data = ''
            self._remaining_data = ''
        else:
            lst = self.data.splitlines()
            for index, line in enumerate(lst):
                line = str(line).rstrip()
                if line.strip():
                    match = re.match(self.spacer_pattern, line)
                    if match:
                        self._spacers = match.group('spacers')
                        length = len(self._spacers)
                        if length == 0:
                            self.set_level(level=0)
                        else:
                            if self.parent:
                                chk_lst = ['setup', 'cleanup', 'teardown', 'section']
                                if self.parent.name in chk_lst:
                                    self.set_level(level=1)
                                else:
                                    self.increase_level()
                            else:
                                if self._prev_spacers > self._spacers:
                                    self.increase_level()

                    self._prev_spacers = self._spacers
                    self._stmt_data = line
                    self._remaining_data = '\n'.join(lst[index+1:])

                    if self.is_base_statement:
                        self.set_level(level=0)
                        self._spacers = ''

                    return

    def add_child(self, child):
        if isinstance(child, Statement):
            self._children.append(child)
            if isinstance(child.parent, Statement):
                child.set_level(level=self.level+1)

    def set_level(self, level=0):
        self._level = level

    def increase_level(self):
        self.set_level(level=self.level+1)

    def update_level_from_parent(self):
        if isinstance(self.parent, Statement):
            self.set_level(level=self.parent.level+1)

    def get_next_statement_data(self):
        for line in self.remaining_data.splitlines():
            if line.strip():
                return line
        else:
            return ''

    def has_next_statement(self):
        next_stmt_data = self.get_next_statement_data()
        return next_stmt_data.strip() != ''

    def check_next_statement(self, op):
        op = str(op).strip().lower()
        if op not in ['eq', 'le', 'lt', 'gt', 'ge', 'ne']:
            failure = 'Operator MUST BE eq, ne, le, lt, ge, or gt'
            raise ComparisonOperatorError(failure)

        if not self.has_next_statement():
            return False
        next_stmt_data = self.get_next_statement_data()
        match = re.match(self.spacer_pattern, next_stmt_data)
        spacers = match.group('spacers') if match else ''

        result = getattr(operator, op)(spacers, self._spacers)
        return result

    def is_next_statement_sibling(self):
        result = self.check_next_statement('eq')
        return result

    def is_next_statement_children(self):
        result = self.check_next_statement('gt')
        return result

    def is_next_statement_ancestor(self):
        result = self.check_next_statement('lt')
        return result

    def validate_framework(self):

        if self.framework.strip() == '':
            failure = 'framework MUST be "unittest", "pytest", or "robotframework"'
            raise NotImplementedFrameworkError(failure)

        is_valid_framework = self.framework == FWTYPE.UNITTEST
        is_valid_framework |= self.framework == FWTYPE.PYTEST
        is_valid_framework |= self.framework == FWTYPE.ROBOTFRAMEWORK

        if not is_valid_framework:
            fmt = '{!r} framework is not implemented.'
            raise NotImplementedFrameworkError(fmt.format(self.framework))

    def indent_data(self, data, lvl):
        new_data = indent(data, ' ' * lvl * self.indentation)
        return new_data

    def get_display_statement(self, message=''):
        message = getattr(self, 'message', message)
        is_logger = getattr(self, 'is_logger', False)
        func_name = 'self.logger.info' if is_logger else 'print'
        if self.framework == FWTYPE.UNITTEST:
            stmt = '%s(%r)' % (func_name, message)
        elif self.framework == FWTYPE.PYTEST:
            stmt = '%s(%r)' % (func_name, message)
        else:   # i.e ROBOTFRAMEWORK
            stmt = 'log   %s' % message

        level = self.parent.level + 1 if self.parent else self.level
        stmt = self.indent_data(stmt, level)
        return stmt

    def get_assert_statement(self, expected_result, assert_only=False):
        is_eresult_number, eresult = Misc.try_to_get_number(expected_result)
        if Misc.is_boolean(eresult):
            eresult = int(eresult)

        if self.framework == FWTYPE.UNITTEST:
            fmt1 = 'self.assertTrue(True == %s)'
            fmt2 = 'total_count = len(result)\nself.assertTrue(total_count == %s)'
        elif self.framework == FWTYPE.PYTEST:
            fmt1 = 'assert True == %s'
            fmt2 = 'total_count = len(result)\nassert total_count == %s'
        else:   # i.e ROBOTFRAMEWORK
            fmt1 = 'should be true   True == %s'
            fmt2 = ('${total_count}=   get length ${result}\nshould be '
                    'true   ${result} == %s')

        fmt = fmt1 if assert_only else fmt2
        eresult = expected_result if assert_only else eresult
        level = self.parent.level + 1 if self.parent else self.level
        stmt = self.indent_data(fmt % eresult, level)
        return stmt


class DummyStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)
        self.case = ''
        self.message = ''
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        fmt = 'DUMMY {} - {}'
        expected_result = True if self.case.lower() == 'pass' else False

        message = fmt.format(self.case.upper(), self.message)
        displayed_stmt = self.get_display_statement(message=message)
        assert_stmt = self.get_assert_statement(expected_result, assert_only=True)
        return '{}\n{}'.format(displayed_stmt, assert_stmt)

    def parse(self):
        pattern = ' *dummy[_. -]*(?P<case>pass|fail) *[^a-z0-9]*(?P<message> *.+) *$'
        match = re.match(pattern, self.statement_data, re.I)
        if match:
            self._is_parsed = True
            self.case = match.group('case').lower()
            self.message = match.group('message')
            self.name = 'dummy'
        else:
            self._is_parsed = False


class SetupStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)

        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        lst = []

        if self.framework == FWTYPE.UNITTEST:
            lst.append('def setUp(self):')
        elif self.framework == FWTYPE.PYTEST:
            lst.append('def setup_class(self):')
        else:   # i.e ROBOTFRAMEWORK
            lst.append('setup')

        for child in self.children:
            lst.append(child.snippet)

        level = 0 if self.framework == FWTYPE.ROBOTFRAMEWORK else 1
        script = self.indent_data('\n'.join(lst), level)
        return script

    def parse(self):
        if self.is_setup_statement:
            self.name = 'setup'
            self._is_parsed = True
            if self.is_next_statement_children():
                node = self.create_child(self)
                self.add_child(node)
                while node and node.is_next_statement_sibling():
                    node = self.create_child(node)
                    self.add_child(node)
                if self.children:
                    last_child = self._children[-1]
                    self._remaining_data = last_child.remaining_data
            if not self.children:
                kwargs = dict(framework=self.framework, indentation=self.indentation)
                data = 'dummy_pass - Dummy Setup'
                dummy_stmt = DummyStatement(data, **kwargs, parent=self)
                self.add_child(dummy_stmt)
        else:
            self._is_parsed = False

    def create_child(self, node):
        kwargs = dict(framework=self.framework, indentation=self.indentation)
        next_line = node.get_next_statement_data()

        if node.is_matched_statement('(?i) +connect +data', next_line):
            other = ConnectDataStatement(node.remaining_data, **kwargs)
        elif node.is_matched_statement('(?i) +use +testcase', next_line):
            other = UseTestCaseStatement(node.remaining_data, **kwargs)
        elif node.is_matched_statement('(?i) +connect +device', next_line):
            other = ConnectDeviceStatement(node.remaining_data, **kwargs)
        else:
            return None

        other.prev = node
        # node.next = other
        if node.name == 'setup':
            other.parent = node
            other.update_level_from_parent()
        else:
            other.parent = node.parent
            other.update_level_from_parent()
        return other


class ConnectDataStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)
        self.var_name = ''
        self.test_resource_ref = ''
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        if self.framework == FWTYPE.ROBOTFRAMEWORK:
            fmt = "${%s}=   connect data   filename=%s\nset global variable   ${%s}"
            stmt = fmt % (self.var_name, self.test_resource_ref, self.var_name)
        else:
            fmt = "self.%s = ta.connect_data(filename=%r)"
            stmt = fmt % (self.var_name, self.test_resource_ref)

        level = self.parent.level + 1 if self.parent else self.level
        stmt = self.indent_data(stmt, level)

        return stmt

    def parse(self):
        pattern = r'(?i) *connect +data +(?P<capture_data>.+)'
        match = re.match(pattern, self.statement_data)
        if match:
            capture_data = match.group('capture_data').strip()
            pattern = r'(?i)(?P<test_resource_ref>.+?)( +as +(?P<var_name>[a-z]\w*))?$'
            match = re.match(pattern, capture_data)
            
            if not match:
                fmt = 'Invalid connect data statement - "{}"'
                raise ConnectDataStatementError(fmt.format(self.statement_data))
            
            test_resource_ref = match.group('test_resource_ref').strip()
            var_name = match.group('var_name') or 'test_resource'
            self.reserve_data(test_resource_ref, var_name)
            self.name = 'connect_data'
            self._is_parsed = True
        else:
            self._is_parsed = False

    def reserve_data(self, test_resource_ref, var_name):
        try:
            with open(test_resource_ref) as stream:
                content = stream.read().strip()
                if not content:
                    fmt = '"{}" test resource reference has no data'
                    raise ConnectDataStatementError(fmt.format(test_resource_ref))
                yaml_obj = yaml.safe_load(content)
                
                if not Misc.is_dict(yaml_obj):
                    fmt = '"" test resource reference has invalid format'
                    raise ConnectDataStatementError(fmt.format(test_resource_ref))
                
                SCRIPTINFO.update(yaml_obj)
                variables = SCRIPTINFO.get('variables', DictObject())
                SCRIPTINFO.variables = variables
                SCRIPTINFO.variables.test_resource_var = var_name
                SCRIPTINFO.variables.test_resource_ref = test_resource_ref
                self.var_name = var_name
                self.test_resource_ref = test_resource_ref
        except Exception as ex:
            raise ConnectDataStatementError(Text(ex))


class UseTestCaseStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)
        self.var_name = ''
        self.test_name = ''
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        test_resource_var = SCRIPTINFO.variables.get('test_resource_var', 'test_resource')

        if self.framework == FWTYPE.ROBOTFRAMEWORK:
            fmt = "${%s}=  use testcase   ${%s}  testcase=%s\nset global variable   ${%s}"
            stmt = fmt % (self.var_name, test_resource_var, self.test_name, self.var_name)
        else:
            fmt = "self.%s = ta.use_testcase(self.%s, testcase=%r)"
            stmt = fmt % (self.var_name, test_resource_var, self.test_name)

        level = self.parent.level + 1 if self.parent else self.level
        stmt = self.indent_data(stmt, level)

        return stmt

    def parse(self):
        pattern = r'(?i) *use +testcase +(?P<capture_data>[a-z0-9].+)'
        match = re.match(pattern, self.statement_data)
        if not match:
            self._is_parsed = False
            return

        capture_data = match.group('capture_data').strip()
        pattern = r'(?i)(?P<test_name>.+?)( +as +(?P<var_name>[a-z]\w*))? *$'
        match = re.match(pattern, capture_data)
        if not match:
            fmt = 'Invalid use testcase statement - {}'
            raise UseTestcaseStatementError(fmt.format(self.statement_data))

        test_name = match.group('test_name')
        var_name = match.group('var_name') or 'test_data'

        if test_name in SCRIPTINFO.get('testcases', DictObject()):
            self.reserve_data(test_name, var_name)
            self.name = 'use_testcase'
            self._is_parsed = True
        else:
            fmt = 'CANT find "{}" test name in test resource'
            raise UseTestcaseStatementError(fmt.format(test_name))

    def reserve_data(self, test_name, var_name):
        variables = SCRIPTINFO.get('variables', DictObject())
        SCRIPTINFO.variables = variables
        SCRIPTINFO.variables.test_data_var = self.var_name
        self.var_name = var_name
        self.test_name = test_name


class ConnectDeviceStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)

        self.devices_vars = DictObject()
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        if not self.has_devices_variables():
            fmt = 'Failed to generate invalid connect device statement - {}'
            failure = fmt.format(self.statement_data)
            raise ConnectDeviceStatementError(failure)

        test_resource_var = SCRIPTINFO.variables.test_resource_var  # noqa

        lst = []
        for var_name, device_name in self.devices_vars.items():
            if self.framework == FWTYPE.ROBOTFRAMEWORK:
                fmt = "${%s}=   connect device   ${%s}   name=%s\nset global variable   ${%s}"
                stmt = fmt % (var_name, test_resource_var, device_name, var_name)

            else:
                fmt = "self.%s = ta.connect_device(self.%s, name=%r)"
                stmt = fmt % (var_name, test_resource_var, device_name)
            lst.append(stmt)

        level = self.parent.level + 1 if self.parent else self.level
        connect_device_statements = self.indent_data('\n'.join(lst), level)

        return connect_device_statements

    def parse(self):
        pattern = r'(?i) *connect +device +(?P<devices_info>.+) *$'
        match = re.match(pattern, self.statement_data)
        if not match:
            self._is_parsed = False
            return

        devices_info = match.group('devices_info').strip()
        devices_info = devices_info.replace('{', '').replace('}', '')

        pattern = r'(?i)(?P<host>\S+)( +as +(?P<var_name>[a-z]\w*))?$'
        for device_info in devices_info.split(','):
            match = re.match(pattern, device_info.strip())
            if match:
                host, var_name = match.group('host'), match.group('var_name')
                self.reserve_data(host, var_name)
            else:
                fmt = 'Invalid connect device statement - {}'
                failure = fmt.format(self.statement_data)
                raise ConnectDeviceStatementError(failure)

        self.name = 'connect_device'
        self._is_parsed = True

    def reserve_data(self, host, var_name):
        devices_vars = SCRIPTINFO.get('devices_vars', DictObject())
        SCRIPTINFO.devices_vars = devices_vars

        pattern = r'device[0-9]+$'

        if var_name and str(var_name).strip():
            if var_name not in devices_vars:
                devices_vars[var_name] = host
                self.devices_vars[var_name] = host
            else:
                failure = 'Duplicate device variable - "{}"'.format(var_name)
                raise ConnectDeviceStatementError(failure)
        else:
            var_names = [k for k in devices_vars if re.match(pattern, k)]
            if var_names:
                new_index = int(var_names[-1].strip('device')) + 1
                key = 'device{}'.format(new_index)
                devices_vars[key] = host
                self.devices_vars[key] = host
            else:
                devices_vars['device1'] = host
                self.devices_vars['device1'] = host

    def has_devices_variables(self):
        return bool(list(self.devices_vars))


class SectionStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)


class LoopStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)


class PerformerStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)


class VerificationStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)


class SystemStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)
