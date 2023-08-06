"""Module containing the logic for describe-get-system to interpret
user describing problem"""


import re
import operator
import yaml

from textwrap import indent

from dgspoc.utils import DotObject
from dgspoc.utils import Misc
# from dgspoc.utils import File
from dgspoc.utils import Text

from dgspoc.constant import FWTYPE

from dgspoc.exceptions import NotImplementedFrameworkError
from dgspoc.exceptions import ComparisonOperatorError
from dgspoc.exceptions import ConnectDataStatementError
from dgspoc.exceptions import UseTestcaseStatementError
from dgspoc.exceptions import ConnectDeviceStatementError
from dgspoc.exceptions import DisconnectDeviceStatementError
from dgspoc.exceptions import ReleaseDeviceStatementError
from dgspoc.exceptions import ReleaseResourceStatementError


class ScriptInfo(DotObject):
    def __init__(self, *args, testcase='', **kwargs):
        super().__init__(*args, **kwargs)
        self.testcase = testcase
        self.devices_vars = dict()
        self.variables = dict(
            test_resource_var='test_resource',
            test_resource_ref='',
            test_data_var='test_data'
        )
        self._enabled_testing = False

    @property
    def is_testing_enabled(self):
        return self._enabled_testing

    def enable_testing(self):
        self._enabled_testing = True

    def disable_testing(self):
        self._enabled_testing = False

    def load_testing_data(self):
        if not self.is_testing_enabled:
            return

        data = """
            devices:
              1.1.1.1:
                name: device1
              1.1.1.2:
                name: device2
            testcases:
              test1:
                ref_1: blab blab
                script_builder:
                  class_name: Testcase1
                  test_precondition: precondition
                  test_case1: case1
                  test_case2: case2
              test2:
                ref_2: blab blab
                script_builder:
                  class_name: Testcase2
                  test_precondition: precondition
                  test_case1: case1
                  test_case2: case2
        """
        self.update(yaml.safe_load(data))

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

    def reset_devices_vars(self):
        self.devices_vars = dict()

    def reset_global_vars(self):
        self.variables = dict(
            test_resource_var='test_resource',
            test_resource_ref='',
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
        pattern = r'setup *$'
        is_matched = self.is_matched_statement(pattern)
        return is_matched

    @property
    def is_cleanup_statement(self):
        pattern = r'cleanup *$'
        is_matched = self.is_matched_statement(pattern)
        return is_matched

    @property
    def is_teardown_statement(self):
        pattern = r'teardown *$'
        is_matched = self.is_matched_statement(pattern)
        return is_matched

    @property
    def is_cleanup_or_teardown_statement(self):
        return self.is_cleanup_statement or self.is_teardown_statement

    @property
    def is_section_statement(self):
        pattern = r'section'
        is_matched = self.is_matched_statement(pattern)
        return is_matched

    @property
    def is_base_statement(self):
        is_base_stmt = self.is_setup_statement
        is_base_stmt |= self.is_section_statement
        is_base_stmt |= self.is_cleanup_or_teardown_statement
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
            fmt = ('{!r} framework is not implemented.  It MUST be '
                   '"unittest", "pytest", or "robotframework"')
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

    def try_to_get_base_statement(self):
        if self.is_base_statement:
            tbl = dict(setup=SetupStatement,
                       cleanup=CleanupStatement,
                       teardown=TeardownStatement)
            key = self.statement_data.lower().strip()
            cls = tbl.get(key, SectionStatement)
            stmt = cls(self.data, framework=self.framework,
                       indentation=self.indentation)
            return stmt if isinstance(stmt, Statement) else self

        else:
            return self


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
            SCRIPTINFO.variables.test_resource_var = var_name
            SCRIPTINFO.variables.test_resource_ref = test_resource_ref
            self.var_name = var_name
            self.test_resource_ref = test_resource_ref
            with open(test_resource_ref) as stream:
                content = stream.read().strip()
                if not content:
                    if SCRIPTINFO.is_testing_enabled:
                        SCRIPTINFO.load_testing_data()
                        return
                    fmt = '"{}" test resource reference has no data'
                    raise ConnectDataStatementError(fmt.format(test_resource_ref))
                yaml_obj = yaml.safe_load(content)
                
                if not Misc.is_dict(yaml_obj):
                    if SCRIPTINFO.is_testing_enabled:
                        SCRIPTINFO.load_testing_data()
                        return
                    fmt = '"" test resource reference has invalid format'
                    raise ConnectDataStatementError(fmt.format(test_resource_ref))
                
                SCRIPTINFO.update(yaml_obj)
        except Exception as ex:
            if SCRIPTINFO.is_testing_enabled:
                SCRIPTINFO.load_testing_data()
            else:
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

        if test_name in SCRIPTINFO.get('testcases', dict()):
            self.reserve_data(test_name, var_name)
            self.name = 'use_testcase'
            self._is_parsed = True
        else:
            fmt = 'CANT find "{}" test name in test resource'
            raise UseTestcaseStatementError(fmt.format(test_name))

    def reserve_data(self, test_name, var_name):
        variables = SCRIPTINFO.get('variables', dict())
        SCRIPTINFO.variables = variables
        SCRIPTINFO.variables.test_data_var = self.var_name
        self.var_name = var_name
        self.test_name = test_name


class ConnectDeviceStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)

        self.devices_vars = dict()
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
        devices_vars = SCRIPTINFO.get('devices_vars', dict())
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


class DisconnectStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)

        self.vars_lst = []
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        if not self.vars_lst:
            fmt = 'Failed to generate invalid disconnect device statement - {}'
            failure = fmt.format(self.statement_data)
            raise DisconnectDeviceStatementError(failure)

        lst = []
        for var_name in self.vars_lst:
            if self.framework == FWTYPE.ROBOTFRAMEWORK:
                stmt = "disconnect device   ${%s}" % var_name
            else:
                stmt = "ta.disconnect_device(self.%s)" % var_name
            lst.append(stmt)

        level = self.parent.level + 1 if self.parent else self.level
        disconnect_device_statements = self.indent_data('\n'.join(lst), level)

        return disconnect_device_statements

    def parse(self):
        pattern = r'(?i) *disconnect *(device)? +(?P<devices_info>.+) *$'
        match = re.match(pattern, self.statement_data)
        if not match:
            self._is_parsed = False
            return

        devices_info = match.group('devices_info').strip()
        devices_info = devices_info.replace('{', '').replace('}', '')

        pattern = r'(?i)(?P<host>\S+)$'
        for index, device_info in enumerate(devices_info.split(',')):
            match = re.match(pattern, device_info.strip())
            if match:
                host = match.group('host')
                self.reserve_data(host, index)
            else:
                fmt = 'Invalid disconnect device statement - {}'
                failure = fmt.format(self.statement_data)
                raise DisconnectDeviceStatementError(failure)

        self.name = 'disconnect_device'
        self._is_parsed = True

    def reserve_data(self, host, index):
        for var_name, host_name in SCRIPTINFO.devices_vars.items():
            if host == host_name:
                self.vars_lst.append(var_name)
                return

        self.vars_lst.append('device{}'.format(index + 1))


class ReleaseDeviceStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)

        self.vars_lst = []
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        if not self.vars_lst:
            fmt = 'Failed to generate invalid release device statement - {}'
            failure = fmt.format(self.statement_data)
            raise ReleaseDeviceStatementError(failure)

        lst = []
        for var_name in self.vars_lst:
            if self.framework == FWTYPE.ROBOTFRAMEWORK:
                stmt = "release device   ${%s}" % var_name
            else:
                stmt = "ta.release_device(self.%s)" % var_name
            lst.append(stmt)

        level = self.parent.level + 1 if self.parent else self.level
        release_device_statements = self.indent_data('\n'.join(lst), level)

        return release_device_statements

    def parse(self):
        pattern = r'(?i) *release +device +(?P<devices_info>.+) *$'
        match = re.match(pattern, self.statement_data)
        if not match:
            self._is_parsed = False
            return

        devices_info = match.group('devices_info').strip()
        devices_info = devices_info.replace('{', '').replace('}', '')

        pattern = r'(?i)(?P<host>\S+)$'
        for index, device_info in enumerate(devices_info.split(',')):
            match = re.match(pattern, device_info.strip())
            if match:
                host = match.group('host')
                self.reserve_data(host, index)
            else:
                fmt = 'Invalid release device statement - {}'
                failure = fmt.format(self.statement_data)
                raise ReleaseDeviceStatementError(failure)

        self.name = 'release_device'
        self._is_parsed = True

    def reserve_data(self, host, index):
        for var_name, host_name in SCRIPTINFO.devices_vars.items():
            if host == host_name:
                self.vars_lst.append(var_name)
                return

        self.vars_lst.append('device{}'.format(index + 1))


class ReleaseResourceStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)

        self.var_name = ''
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        if not self.var_name:
            fmt = 'Failed to generate invalid release resource statement - {}'
            failure = fmt.format(self.statement_data)
            raise ReleaseResourceStatementError(failure)

        if self.framework == FWTYPE.ROBOTFRAMEWORK:
            stmt = "release resource   ${%s}" % self.var_name
        else:
            stmt = "ta.release_resource(self.%s)" % self.var_name

        level = self.parent.level + 1 if self.parent else self.level
        release_resource_statement = self.indent_data(stmt, level)

        return release_resource_statement

    def parse(self):
        pattern = r'(?i) *release +resource +(?P<resource_ref>\w(\S*\w)?) *$'
        match = re.match(pattern, self.statement_data)
        if not match:
            self._is_parsed = False
            return

        resource_ref = match.group('resource_ref').strip()

        if SCRIPTINFO.variables.test_resource_ref != resource_ref:  # noqa
            if SCRIPTINFO.is_testing_enabled:
                self.var_name = 'test_resource'
            else:
                fmt = 'CANT find {!r} resource for release resource statement'
                failure = fmt.format(resource_ref)
                raise ReleaseResourceStatementError(failure)
        else:
            self.var_name = SCRIPTINFO.variables.test_resource_var  # noqa

        self.name = 'release_resource'
        self._is_parsed = True


class CleanupStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)

        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        lst = []
        txt = 'tearDown' if self.name == 'teardown' else 'cleanUp'

        if self.framework == FWTYPE.UNITTEST:
            lst.append('def %s(self):' % txt)
        elif self.framework == FWTYPE.PYTEST:
            lst.append('def %s_class(self):' % txt.lower())
        else:   # i.e ROBOTFRAMEWORK
            lst.append(txt.lower())

        for child in self.children:
            lst.append(child.snippet)

        level = 0 if self.framework == FWTYPE.ROBOTFRAMEWORK else 1
        script = self.indent_data('\n'.join(lst), level)
        return script

    def parse(self):
        if self.is_cleanup_or_teardown_statement:
            self.name = self.statement_data.strip().lower()
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
                data = 'dummy_pass - Dummy %s' % self.name.title()
                dummy_stmt = DummyStatement(data, **kwargs, parent=self)
                self.add_child(dummy_stmt)
        else:
            self._is_parsed = False

    def create_child(self, node):
        kwargs = dict(framework=self.framework, indentation=self.indentation)
        next_line = node.get_next_statement_data()

        if node.is_matched_statement('(?i) +disconnect( +device)? ', next_line):
            other = DisconnectStatement(node.remaining_data, **kwargs)
        elif node.is_matched_statement('(?i) +release +device', next_line):
            other = ReleaseDeviceStatement(node.remaining_data, **kwargs)
        elif node.is_matched_statement('(?i) +release +resource', next_line):
            other = ReleaseResourceStatement(node.remaining_data, **kwargs)
        else:
            return None

        other.prev = node
        # node.next = other
        if node.name == 'cleanup' or node.name == 'teardown':
            other.parent = node
            other.update_level_from_parent()
        else:
            other.parent = node.parent
            other.update_level_from_parent()
        return other


class TeardownStatement(CleanupStatement):
    """Teardown Statement class"""


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


class ScriptBuilder:
    def __init__(self, data, framework='', indentation=4,
                 username='', email='', company='',):
        self.data = data
        self.framework = str(framework).strip()
        self.indentation = indentation
        self.username = str(username).strip()
        self.email = str(email).strip()
        self.company = str(company).strip() or self.username

        self.setup_statement = None
        self.cleanup_statement = None
        self.section_statements = []
        self.build()

    @property
    def testscript(self):
        if self.setup_statement and self.cleanup_statement:
            if self.framework == FWTYPE.UNITTEST:
                script = self.unittest_script
                return script
            elif self.framework == FWTYPE.PYTEST:
                script = self.pytest_script
                return script
            else:
                script = self.robotframework_script
                return script
        else:
            pass

    @property
    def unittest_script(self):
        cls_name = SCRIPTINFO.get_class_name()
        lst = [
            self.script_intro,
            '',
            'import unittest',
            'import dgspoc as ta',
            '\n',
            'class {}(unittest.Testcase):'.format(cls_name),
            self.setup_statement.snippet,
            '',
            self.cleanup_statement.snippet,
        ]

        for stmt in self.section_statements:
            lst.append('')
            lst.append(stmt.snippet)

        script = '\n'.join(lst)
        return script

    @property
    def pytest_script(self):
        cls_name = SCRIPTINFO.get_class_name()
        lst = [
            self.script_intro,
            '',
            '# import pytest',
            'import dgspoc as ta',
            '\n',
            'class {}:'.format(cls_name),
            self.setup_statement.snippet,
            '',
            self.cleanup_statement.snippet,
        ]

        for stmt in self.section_statements:
            lst.append('')
            lst.append(stmt.snippet)

        script = '\n'.join(lst)
        return script

    @property
    def robotframework_script(self):
        lst = [
            self.script_intro,
            '',
            '*** Settings ***',
            'library         builtin',
            'library         collections',
            'library         describegetsystempoc',
            'test setup      setup',
            'test teardown   {}'.format(self.cleanup_statement.name),
        ]

        if self.section_statements:
            cls_name = SCRIPTINFO.get_class_name()
            lst.append('\n*** Test Cases ***')
            lst.append(cls_name)
            for stmt in self.section_statements:
                lst.append(stmt.name)

        lst.append('\n*** Keywords ***')
        lst.append(self.setup_statement.snippet)
        lst.append('')
        lst.append(self.cleanup_statement.snippet)

        for stmt in self.section_statements:
            lst.append('')
            lst.append(stmt.snippet)

        script = '\n'.join(lst)
        return script

    @property
    def script_intro(self):
        fmt = '# {} script is generated by Describe-Get-System Proof of Concept'
        user_fmt = '# Created by  : {0.username}'
        email_fmt = '# Email       : {0.email}'
        company_fmt = '# Company     : {0.company}'
        date_fmt = '# Created date: {}'
        lst = [fmt.format(self.framework.lower())]
        self.username and lst.append(user_fmt.format(self))
        self.email and lst.append(email_fmt.format(self))
        self.company and lst.append(company_fmt.format(self))
        not SCRIPTINFO.is_testing_enabled and lst.append(date_fmt)

        intro = '\n'.join(['#' * 80] + lst + ['#' * 80])
        return intro

    def build(self):
        data = self.data
        count = 2000

        while data.strip() and count > 0:
            stmt = Statement(data, framework=self.framework,
                             indentation=self.indentation)
            stmt = stmt.try_to_get_base_statement()
            self.add_statement(stmt)
            data = stmt.remaining_data
            count -= 1

    def add_statement(self, stmt):
        if stmt.is_setup_statement:
            if not self.setup_statement:
                self.setup_statement = stmt
            else:
                self.warn_duplicate_statement(stmt)
        elif stmt.is_cleanup_or_teardown_statement:
            if not self.cleanup_statement:
                self.cleanup_statement = stmt
            else:
                self.warn_duplicate_statement(stmt)
        elif stmt.is_section_statement:
            if self.is_uniq_section_statement(stmt):
                self.section_statements.append(stmt)
            else:
                self.warn_duplicate_statement(stmt)
        else:
            self.warn_not_implement_statement(stmt)

    def is_uniq_section_statement(self, stmt):
        if not self.section_statements:
            return True

        chk = stmt.snippet
        is_duplicate = any(chk == k.snippet for k in self.section_statements)
        return not is_duplicate

    def warn_duplicate_statement(self, stmt):
        fmt = 'TODO - Need to implement warn_duplicate_statement\n{}'
        raise NotImplementedError(fmt.format(stmt.statement_data))

    def warn_not_implement_statement(self, stmt):
        fmt = 'TODO - Need to implement warn_not_implement_statement\n{}'
        raise NotImplementedError(fmt.format(stmt.statement_data))
