# -*- coding: UTF-8 -*-
# This is a collection of "tests" done on the package data. The resut of the
# tests is used to give the package a rating.
#
# Each test has a couple of attributes. Both attributes are checked only after
# the test is performed so the test can choose to set the attributes dependning
# on the severity of the failure.
#
#     fatal:    If set to True, the failure of this test will cause the 
#               package to achieve the rating of 1, which is minimum
#     weight:   The relative importance of the test.
#               If the test has required set to True this is ignored.
#
# Tests have two methods:
#     test(data): Performs the test on the given data. Returns True for pass
#                 False for fail and None for not applicable (meaning it will
#                 not be counted).

LEVELS = ["I don't think that's really cheese",
          "Vieux Bologne",
          "Limburger",
          "Gorgonzola",
          "Stilton",
          "Brie",
          "Compté",
          "Jarlsberg",
          "Philadelphia",
          "Cottage Cheese",
          "Your cheese is so fresh most people think it's a cream: Mascarpone"]

# All modules in stdlib. No attempt to differentiate between different
# versions is made at the moment, but this test is made here rather than in
# the projectdata.py so that it is possible to extend the test to differentiate
# on Python version if so desired.
STDLIB = set([
'_abcoll', 'abc', 'aifc', 'antigravity', 'anydbm', 'argparse', 'ast', 
'asynchat', 'asyncore', 'atexit', 'audiodev', 'base64', 'BaseHTTPServer', 
'Bastion', 'bdb', 'binhex', 'bisect', 'calendar', 'CGIHTTPServer', 'cgi', 
'cgitb', 'chunk', 'cmd', 'codecs', 'codeop', 'code', 'collections', 'colorsys',
'commands', 'compileall', 'ConfigParser', 'contextlib', 'cookielib', 'Cookie',
'copy', 'copy_reg', 'cProfile', 'csv', 'dbhash', 'decimal', 'difflib',
'dircache', 'dis', 'doctest', 'DocXMLRPCServer', 'dumbdbm', 'dummy_threading',
'dummy_thread', 'filecmp', 'fileinput', 'fnmatch', 'formatter', 'fpformat',
'fractions', 'ftplib', 'functools', '__future__', 'genericpath', 'getopt',
'getpass', 'gettext', 'glob', 'gzip', 'hashlib', 'heapq', 'hmac',
'htmlentitydefs', 'htmllib', 'HTMLParser', 'httplib', 'ihooks', 'imaplib',
'imghdr', 'imputil', 'inspect', 'io', 'keyword', 'linecache', 'locale',
'_LWPCookieJar', 'macpath', 'macurl2path', 'mailbox', 'mailcap', 'markupbase',
'md5', 'mhlib', 'mimetools', 'mimetypes', 'MimeWriter', 'mimify',
'modulefinder', '_MozillaCookieJar', 'multifile', 'mutex', 'netrc', 'new',
'nntplib', 'ntpath', 'nturl2path', 'numbers', 'opcode', 'optparse',
'os2emxpath', 'os', 'pdb', 'pickle', 'pickletools', 'pipes', 'pkgutil', 
'platform', 'plistlib', 'popen2', 'poplib', 'posixfile', 'posixpath', 'pprint',
'profile', 'pstats', 'pty', 'pyclbr', 'py_compile', 'pydoc', '_pyio', 'Queue',
'quopri', 'random', 'repr', 're', 'rexec', 'rfc822', 'rlcompleter',
'robotparser', 'runpy', 'sched', 'sets', 'sgmllib', 'sha', 'shelve', 'shlex',
'shutil', 'SimpleHTTPServer', 'SimpleXMLRPCServer', 'site', 'smtpd', 'smtplib',
'sndhdr', 'socket', 'SocketServer', 'sre_compile', 'sre_constants', 'sre_parse',
'sre', 'ssl', 'stat', 'statvfs', 'StringIO', 'stringold', 'stringprep', 
'string', '_strptime', 'struct', 'subprocess', 'sunaudio', 'sunau', 'symbol', 
'symtable', 'sys', 'sysconfig', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile',
'textwrap', 'this', '_threading_local', 'threading', 'timeit', 'toaiff', 
'tokenize', 'token', 'traceback', 'trace', 'tty', 'types', 'unittest', 
'urllib2', 'urllib', 'urlparse', 'UserDict', 'UserList', 'user', 'UserString', 
'uuid', 'uu', 'warnings', 'wave', 'weakref', '_weakrefset', 'webbrowser', 
'whichdb', 'xdrlib', 'xmllib', 'xmlrpclib', 'zipfile'])

# Some packages will install other modules. This is bad form, but it happens.
# If you install setuptools you also get a 'pkg_resources' module, for example.
ALIASES = {'setuptools': ['pkg_resources'],
           }

class BaseTest(object):
    fatal = False
    weight = 0
    
class FieldTest(BaseTest):
    """Tests that a specific field is in the data and is not empty or False"""
    
    def test(self, data):
        return bool(data.get(self.field))
    
    def message(self):
        return ("Your package does not have %s data" % self.field) + (self.fatal and '!' or '')

class Name(FieldTest):
    
    fatal = True
    field = 'name'

class Version(FieldTest):
    
    fatal = True
    field = 'version'
        
class Description(BaseTest):
    weight = 100
    
    def test(self, data):
        description = data.get('description')
        if not description:
            # No description at all. That's fatal.
            self.fatal = True
        return len(description) > 10
    
    def message(self):
        if self.fatal:
            return 'The package had no description!'
        else:
            return 'The packages description should be longer than 10 characters'

class LongDescription(BaseTest):    
    weight = 50
    
    def test(self, data):
        return len(data.get('long_description')) > 100
    
    def message(self):
        return 'The packages long_description is quite short'

class Classifiers(FieldTest):
    
    weight = 100
    field = 'classifiers'

class PythonVersion(BaseTest):
    
    weight = None # This has several levels of failure.
    
    def test(self, data):
        self._major_version_specified = False
        self.weight = 100
        
        classifiers = data.get('classifiers', [])
        for classifier in classifiers:
            # There are at least some classifiers:
            self.weight = 25
            parts = [p.strip() for p in classifier.split('::')]
            if parts[0] == 'Programming Language' and parts[1] == 'Python':
                if len(parts) == 2:
                    # Specified Python, but no version.
                    return False
                version = parts[2]
                try:
                    float(version)
                except ValueError:
                    # Not a proper Python version
                    continue
                try:
                    int(version)
                except ValueError:
                    # It's a valid float, but not a valid int. Hence it's 
                    # something like "2.7" or "3.3" but not just "2" or "3".
                    # This is a good specification
                    self.weight = 100
                    return True
                # It's a valid int, meaning it specified "2" or "3".
                # That's not good enough.
                self._major_version_specified = False
                self.weight = 50
                    
        # None of the specifications where any good.
        return False

    def message(self):
        if self._major_version_specified:
            return "The classifiers should specify what minor versions of "\
                   "Python you support as well as what major version"
        return "You should specify what Python versions you support"
        
        
class Keywords(FieldTest):    
    weight = 50
    field = 'keywords'

class Author(FieldTest):    
    weight = 100
    field = 'author'

class AuthorEmail(FieldTest):    
    weight = 100
    field = 'author_email'

class Url(FieldTest):    
    weight = 20
    field = 'url'

class License(FieldTest):    
    weight = 50
    field = 'license'

class ZipSafe(BaseTest):
    weight = 20
    
    def test(self, data):
        return 'zip_safe' in data
    
    def message(self):
        return "It's not specified if this package is zip_safe or not, which "\
               "is usually an oversight. You should specify it, as it "\
               "defaults to True, which you probably do not want."

class TestSuite(FieldTest):
    weight = 50
    field = 'test_suite'
    
    def message(self):
        return "Setuptools and Distribute support running tests. By "\
               "specifying a test suite, it's easy to find and run tests "\
               "both for automated tools and humans."

class Dependencies(BaseTest):
    weight = 100
    
    def test(self, data):
        declared_dependencies = data.get('install_requires', []) + \
                                data.get('tests_require', []) + \
                                data.get('setup_requires', [])
        for r in data.get('extras_require', {}).values():
            declared_dependencies.extend(r)
            
        # Update the declared with aliases:
        for d in declared_dependencies:
            declared_dependencies.extend(ALIASES.get(d, []))
            
        # Add the packages in the module to the declared dependencies.
        declared_dependencies.extend(data['packages'])
        
        dependencies = data['_imports'] - STDLIB
        self._undeclared = dependencies - set(declared_dependencies)
        return not bool(self._undeclared)
        
    def message(self):
        undeclared = ', '.join(self._undeclared)
        return "You did not declare the following dependencies: " + undeclared


ALL_TESTS = [
    Name(), 
    Version(), 
    Description(), 
    LongDescription(), 
    Classifiers(), 
    PythonVersion(), 
    Keywords(),
    Author(), 
    AuthorEmail(), 
    Url(), 
    License(), 
    ZipSafe(), 
    TestSuite(), 
    Dependencies(), 
]

def rate(data):
    if not data:
        # No data was gathered. Fail:
        return (0, ["I couldn't find any package data"])  
    fails = []
    good = 0
    bad = 0
    fatality = False
    for test in ALL_TESTS:
        res = test.test(data)
        if res is False:
            bad += test.weight
            fails.append(test.message())
            if test.fatal:
                fatality = True
        elif res is True:
            good += test.weight
    # If res is None, it's ignored. 
    if fatality:
        # A fatal tests failed. That means we give a 0 rating:
        return 0, fails
    # Multiply good by 9, and add 1 to get a rating between 
    # 1: All non-fatal tests failed.
    # 10: All tests succeeded.
    return (good*9)//(good+bad)+1, fails