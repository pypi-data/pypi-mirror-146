"""Module containing the logic for connector adaptor"""

from subprocess import getstatusoutput
import re

from dgspoc.exceptions import AdaptorAuthenticationError

from dgspoc.constant import ECODE


class Adaptor:
    def __init__(self, adaptor, *args, **kwargs):
        self.adaptor = adaptor.strip()
        if self.is_unreal_device_adaptor:
            addr = args[0]
            testcase = kwargs.get('testcase', '')
            self.device = UnrealDeviceAdaptor(addr, testcase=testcase)
        else:
            fmt = '*** Need to implement "{}" adaptor'
            NotImplementedError(fmt.format(adaptor))

    @property
    def is_unreal_device_adaptor(self):
        result = re.match('(?i)unreal-?device$', self.adaptor)
        return bool(result)

    def connect(self):
        result = self.device.connect()
        if self.is_unreal_device_adaptor:
            if self.device.result.startswith('UnrealDeviceConnectionError:'):
                raise AdaptorAuthenticationError(self.device.result)
        return result

    def execute(self, *args, **kwargs):
        result = self.device.execute(*args, **kwargs)
        return result

    def configure(self, *args, **kwargs):
        result = self.device.configure(*args, **kwargs)
        return result

    def disconnect(self, *args, **kwargs):
        result = self.device.disconnect(*args, **kwargs)
        return result

    def reload(self, *args, **kwargs):
        result = self.device.reload(*args, **kwargs)
        return result

    def release(self, *args, **kwargs):
        result = self.device.release(*args, **kwargs)
        return result


class UnrealDeviceAdaptor:
    def __init__(self, address, testcase=''):
        self.address = str(address).strip()
        self.name = self.address
        self.testcase = str(testcase).strip()
        self.result = ''
        self.exit_code = ECODE.SUCCESS

    @property
    def status(self):
        return True if self.exit_code == ECODE.SUCCESS else False

    def process(self, statement):
        self.exit_code, self.result = getstatusoutput(statement.strip())
        print(self.result)
        return self.status

    def connect(self):
        fmt = 'unreal-device connect {0.address} {0.testcase}'
        unreal_statement = fmt.format(self).strip()
        self.process(unreal_statement)
        return self.status

    def execute(self, *args, **kwargs):
        addr = kwargs.get('name', self.address)
        cmdline = args[0]
        fmt = 'unreal-device execute {}::{}'
        unreal_statement = fmt.format(addr, cmdline)
        self.process(unreal_statement)
        return self.result

    def configure(self, *args, **kwargs):
        addr = kwargs.get('name', self.address)
        cfg_reference = args[0]
        fmt = 'unreal-device configure {}::{}'
        unreal_statement = fmt.format(addr, cfg_reference)
        self.process(unreal_statement)
        return self.result

    def disconnect(self, *args, **kwargs):      # noqa
        addr = kwargs.get('name', self.address)
        fmt = 'unreal-device disconnect {}'
        unreal_statement = fmt.format(addr)
        self.process(unreal_statement)
        return self.status

    def reload(self, *args, **kwargs):      # noqa
        addr = kwargs.get('name', self.address)
        fmt = 'unreal-device reload {} {}'
        unreal_statement = fmt.format(addr, self.testcase)
        self.process(unreal_statement)
        return self.status

    def release(self, *args, **kwargs):     # noqa
        addr = kwargs.get('name', self.address)
        fmt = 'unreal-device destroy {}'
        unreal_statement = fmt.format(addr)
        self.process(unreal_statement)
        return self.status
