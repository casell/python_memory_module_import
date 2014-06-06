"""Loads modules from base64 strings
The expected format is:
    tuple(FORMAT, CONTENT)
Supported formats are:
    zip, tar:gz, tar:bz, tar, plain

If plain is the wanted format the FORMAT argument should contain the name to be used as module name

All but plain format needs the modules to be in the root directory (see EGGS formats)
"""
import sys
import imp
from zipfile import PyZipFile
from tarfile import open as taropen
from StringIO import StringIO
from base64 import decodestring
from os.path import splitext


class Loader:
    def __init__(self, fullname, contents, path):
        self.fullname = fullname
        self.contents = contents
        self.path = path

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
        splittedFname = self.fullname.split('.')
        if (len(splittedFname) > 1 and splittedFname[1] == '__init__'):
            mod.__path__ = fullname
        mod.__file__ = "<%s>" % fullname
        mod.__loader__ = self
        code = compile(self.contents, mod.__file__, "exec")
        exec code in mod.__dict__
        return mod


class Finder:
    def __init__(self, modules):
        self.modules = modules

    def find_module(self, fullname, path=None):
        if (fullname in self.modules):
            return Loader(fullname, self.modules[fullname], path)
        elif (fullname + '.__init__' in self.modules) and (path is None):
            return Loader(fullname + '.__init__', self.modules[fullname + '.__init__'], path)
        return None


def get_modules_meta_paths(modules_descriptions):
    for module_description in modules_descriptions:
        yield get_module_meta_path(module_description)


def get_module_meta_path(module_description):
    raw_format = module_description[0].split(':')
    if raw_format[0] in ('zip', 'tar'):
        f = StringIO()
        f.write(decodestring(module_description[1]))
        f.seek(0)
        if raw_format[0] == 'zip':
            zipf = PyZipFile(f)
            module_dict = dict((splitext(z.filename)[0].replace('/', '.'), zipf.open(z.filename).read()) for z in zipf.infolist() if splitext(z.filename)[1] == ".py")
        elif raw_format[0] == 'tar':
            compression = raw_format[1] if len(raw_format) > 1 else ''
            tarf = taropen(fileobj=f, mode="r:" + compression)
            module_dict = dict((splitext(t.name)[0].replace('/', '.'), tarf.extractfile(t.name).read()) for t in tarf.getmembers() if splitext(t.name)[1] == ".py")
    else:
        module_dict = {module_description[0]: decodestring(module_description[1])}
    return Finder(module_dict)