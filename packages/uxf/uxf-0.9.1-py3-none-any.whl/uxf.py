#!/usr/bin/env python3
# Copyright © 2022 Mark Summerfield. All rights reserved.
# License: GPLv3

'''
UXF is a plain text human readable storage format that may serve as a
convenient alternative to csv, ini, json, sqlite, toml, xml, or yaml.

The uxf module can be used as an executable. Run

    python3 -m uxf -h

to see the command line help.

uxf's public API provides two functions and three classes.

    def read(filename_or_filelike): -> (data, custom_header)

In the returned 2-tuple the data is a dict (i.e., a UXF map), list, or
uxf.Table, and the custom_header is a (possibly empty) custom string.

    def write(filename_or_filelike, data, custom)

This writes the data (and custom header if supplied) into the given file as
UXF data. The data must be a single dict, list, or uxf.Table.

    class Error

Used to propagate errors (and warnings if warn_is_error is True).

    class Table

Used to store uxf.Tables. A uxf.Table has a list of fieldnames and a records
list which is a lists of lists with each sublist having the same number of
items as the number of fieldnames.

    class NTuple

Use to store 2-12 ints or 2-12 floats. If one_way_conversion is True then
complex numbers are converted to two-item uxf.NTuples. NTuples are ideal for
storing complex numbers, points (2D or 3D), IP addresses, and RGB and RGBA
values.

Note that the __version__ is the module version (i.e., the versio of this
implementation), while the VERSION is the maximum UXF version that this
module can read (and the UXF version that it writes).
'''

import collections
import datetime
import enum
import gzip
import re
import sys
from xml.sax.saxutils import escape, unescape

try:
    from dateutil.parser import isoparse
except ImportError:
    isoparse = None


__all__ = ('__version__', 'VERSION', 'read', 'write', 'Table', 'NTuple')
__version__ = '0.9.1' # uxf module version
VERSION = 1.0 # uxf file format version

UTF8 = 'utf-8'


def read(filename_or_filelike, *, warn_is_error=False):
    '''
    Returns a 2-tuple, the first item of which is a dict (i.e., a UXF map),
    list, or uxf.Table containing all the UXF data read. The second item is
    the custom string (if any) from the file's header.

    filename_or_filelike is sys.stdin or a filename or an open readable file
    (text mode UTF-8 encoded).

    If warn_is_error is True warnings raise Error exceptions.
    '''
    data = None
    tokens, custom, text = _tokenize(
        filename_or_filelike, warn_is_error=warn_is_error)
    data = _parse(tokens, text=text, warn_is_error=warn_is_error)
    return data, custom


def _tokenize(filename_or_filelike, *, warn_is_error=False):
    text = _read_text(filename_or_filelike)
    lexer = _Lexer(warn_is_error=warn_is_error)
    tokens = lexer.tokenize(text)
    return tokens, lexer.custom, text


def _read_text(filename_or_filelike):
    if not isinstance(filename_or_filelike, str):
        return filename_or_filelike.read()
    try:
        with gzip.open(filename_or_filelike, 'rt', encoding=UTF8) as file:
            return file.read()
    except gzip.BadGzipFile:
        with open(filename_or_filelike, 'rt', encoding=UTF8) as file:
            return file.read()


class _ErrorMixin:

    def warn(self, message):
        if self.warn_is_error:
            self.error(message)
        lino = self.text.count('\n', 0, self.pos) + 1
        print(f'warning:{self._what}:{lino}: {message}')


    def error(self, message):
        lino = self.text.count('\n', 0, self.pos) + 1
        raise Error(f'{self._what}:{lino}: {message}')


class _Lexer(_ErrorMixin):

    def __init__(self, *, warn_is_error=False):
        self.warn_is_error = warn_is_error
        self._what = 'lexer'


    def clear(self):
        self.text_kind = _Kind.STR
        self.pos = 0 # current
        self.custom = None
        self.tokens = []


    def tokenize(self, text):
        self.clear()
        self.text = text
        self.scan_header()
        while not self.at_end():
            self.scan_next()
        self.add_token(_Kind.EOF)
        return self.tokens


    def scan_header(self):
        i = self.text.find('\n')
        if i == -1:
            self.error('missing UXF file header or empty file')
        self.pos = i
        parts = self.text[:i].split(None, 2)
        if len(parts) < 2:
            self.error('invalid UXF file header')
        if parts[0] != 'uxf':
            self.error('not a UXF file')
        try:
            version = float(parts[1])
            if version > VERSION:
                self.warn(f'version ({version}) > current ({VERSION})')
        except ValueError:
            self.warn('failed to read UXF file version number')
        if len(parts) > 2:
            self.custom = parts[2]


    def at_end(self):
        return self.pos >= len(self.text)


    def scan_next(self):
        c = self.getch()
        if c.isspace():
            pass
        elif c == '[':
            if self.peek() == '=':
                self.pos += 1
                self.add_token(_Kind.TABLE_BEGIN)
                self.text_kind = _Kind.TABLE_NAME
            else:
                self.add_token(_Kind.LIST_BEGIN)
        elif c == '=':
            if self.peek() == ']':
                self.pos += 1
                self.add_token(_Kind.TABLE_END)
                self.text_kind = _Kind.STR
            elif self.text_kind is _Kind.TABLE_FIELD_NAME:
                self.add_token(_Kind.TABLE_ROWS)
                self.text_kind = _Kind.STR
            else:
                self.error(f'unexpected character encountered: {c!r}')
        elif c == ']':
            self.add_token(_Kind.LIST_END)
        elif c == '{':
            self.add_token(_Kind.DICT_BEGIN)
        elif c == '}':
            self.add_token(_Kind.DICT_END)
        elif c == '<':
            self.read_string_or_name()
        elif c == '(':
            if self.peek() == ':':
                self.read_ntuple()
            else:
                self.read_bytes()
        elif c == '-' and self.peek().isdecimal():
            c = self.getch() # skip the - and get the first digit
            self.read_negative_number(c)
        elif c.isdecimal():
            self.read_positive_number_or_date(c)
        elif c.isalpha():
            self.read_const()
        else:
            self.error(f'invalid character encountered: {c!r}')


    def read_string_or_name(self):
        value = self.match_to('>', error_text='unterminated string or name')
        self.add_token(self.text_kind, unescape(value))
        if self.text_kind is _Kind.TABLE_NAME:
            self.text_kind = _Kind.TABLE_FIELD_NAME


    def read_ntuple(self):
        self.pos += 1 # skip the leading : of (:
        value = self.match_to(':', error_text='unterminated ntuple')
        if self.peek() != ')':
            self.error(f'expected \')\', got {self.peek()!r}')
        self.pos += 1 # skip the trailing ) of :)
        parts = value.split()
        if not (2 <= len(parts) <= 12):
            self.error(f'expected 2-12 ints or floats, got {len(parts)}')
        try:
            int(parts[0])
            Class = int
        except ValueError:
            Class = float
        numbers = [Class(s) for s in parts]
        self.add_token(_Kind.NTUPLE, NTuple(*numbers))


    def read_bytes(self):
        value = self.match_to(')', error_text='unterminated bytes')
        self.add_token(_Kind.BYTES, bytes.fromhex(value))


    def read_negative_number(self, c):
        is_real = False
        start = self.pos - 1
        while not self.at_end() and (c in '.eE' or c.isdecimal()):
            if c in '.eE':
                is_real = True
            c = self.text[self.pos]
            self.pos += 1
        convert = float if is_real else int
        text = self.text[start:self.pos]
        try:
            value = convert(text)
            self.add_token(_Kind.REAL if is_real else _Kind.INT,
                           -value)
        except ValueError as err:
            self.error(f'invalid number: {text}: {err}')


    def read_positive_number_or_date(self, c):
        is_real = is_datetime = False
        hyphens = 0
        start = self.pos - 1
        while not self.at_end() and (c in '-+.:eETZ' or c.isdecimal()):
            if c in '.eE':
                is_real = True
            elif c == '-':
                hyphens += 1
            elif c in ':TZ':
                is_datetime = True
            c = self.text[self.pos]
            self.pos += 1
        self.pos -= 1 # wind back to terminating non-numeric non-date char
        text = self.text[start:self.pos]
        if is_datetime:
            if isoparse is None:
                convert = datetime.datetime.fromisoformat
                if text.endswith('Z'):
                    text = text[:-1] # Py std lib can't handle UTC 'Z'
            else:
                convert = isoparse
            convert = (datetime.datetime.fromisoformat if isoparse is None
                       else isoparse)
            token = _Kind.DATE_TIME
        elif hyphens == 2:
            convert = (datetime.date.fromisoformat if isoparse is None
                       else isoparse)
            token = _Kind.DATE
        elif is_real:
            convert = float
            token = _Kind.REAL
        else:
            convert = int
            token = _Kind.INT
        try:
            value = convert(text)
            if token is _Kind.DATE and isoparse is not None:
                value = value.date()
            self.add_token(token, value)
        except ValueError as err:
            self.error(f'invalid number or date/time: {text}: {err}')


    def read_const(self):
        match = self.match_any_of('no', 'yes', 'null', 'true', 'false')
        if match == 'null':
            self.add_token(_Kind.NULL)
        elif match in {'no', 'false'}:
            self.add_token(_Kind.BOOL, False)
        elif match in {'yes', 'true'}:
            self.add_token(_Kind.BOOL, True)
        else:
            i = self.text.find('\n', self.pos)
            text = self.text[self.pos - 1:i if i > -1 else self.pos + 8]
            self.error(f'expected const got: {text!r}')


    def peek(self):
        return '\0' if self.at_end() else self.text[self.pos]


    def getch(self): # advance
        c = self.text[self.pos]
        self.pos += 1
        return c


    def match_to(self, c, *, error_text):
        if not self.at_end():
            i = self.text.find(c, self.pos)
            if i > -1:
                text = self.text[self.pos:i]
                self.pos = i + 1 # skip past target c
                return text
        self.error(error_text)


    def match_any_of(self, *targets):
        if self.at_end():
            return None
        start = self.pos - 1
        for target in targets:
            if self.text.startswith(target, start):
                self.pos += len(target) - 1 # skip past target
                return target


    def add_token(self, kind, value=None):
        self.tokens.append(_Token(kind, value, self.pos))


class Error(Exception):
    pass


class _Token:

    def __init__(self, kind, value=None, pos=-1):
        self.kind = kind
        self.value = value # literal, i.e., correctly typed item
        self.pos = pos


    def __str__(self):
        parts = [self.kind.name]
        if self.value is not None:
            parts.append(f'={self.value!r}')
        return ''.join(parts)


    def __repr__(self):
        parts = [f'{self.__class__.__name__}({self.kind.name}']
        if self.value is not None:
            parts.append(f', {self.value!r}')
        parts.append(')')
        return ''.join(parts)


@enum.unique
class _Kind(enum.Enum):
    TABLE_BEGIN = enum.auto()
    TABLE_NAME = enum.auto()
    TABLE_FIELD_NAME = enum.auto()
    TABLE_ROWS = enum.auto()
    TABLE_END = enum.auto()
    LIST_BEGIN = enum.auto()
    LIST_END = enum.auto()
    DICT_BEGIN = enum.auto()
    DICT_END = enum.auto()
    NTUPLE = enum.auto()
    NULL = enum.auto()
    BOOL = enum.auto()
    INT = enum.auto()
    REAL = enum.auto()
    DATE = enum.auto()
    DATE_TIME = enum.auto()
    STR = enum.auto()
    BYTES = enum.auto()
    EOF = enum.auto()


class NTuple:
    '''Used to store a UXF ntuple.

    A uxf.NTuple holds 2-12 ints or 2-12 floats.

    When using write() when one_way_conversion is True then complex numbers
    are converted to two-item uxf.NTuples.

    NTuples are ideal for storing complex numbers, points (2D or 3D), IP
    addresses, and RGB and RGBA values.

    Examples:

    >>> nt = NTuple(10, 20, 30, 40, 50)
    >>> nt[0], nt.a, nt.x, nt.first
    (10, 10, 10, 10)
    >>> nt[1], nt.b, nt.y, nt.second
    (20, 20, 20, 20)
    >>> nt[2], nt.c, nt.z, nt.third
    (30, 30, 30, 30)
    >>> nt[3], nt.d, nt.fourth
    (40, 40, 40)

    Every item can be accessed by index 0 <= min(len(), 11) or by fieldname.
    The first three items can also be accessed as attributes .x, .y, and .z,
    respectively. All items can be accessed as attributes .a, .b, .c, ...,
    .j, .k, .l, respectively, and as .first, .second, .third, ..., .tenth,
    .eleventh, .twelth, respectively. In addition, for NTuples of length
    two, the first item can be accessed as attribute .real and the second as
    .imag or .imaginary.
    '''

    __slots__ = ('_items',)

    def __init__(self, a, b, *args):
        kind = type(a)
        if type(b) is not kind:
            raise Error(f'{self.__class__.__name__} may only hold all '
                        'ints or all floats')
        self._items = [a, b]
        for n in args:
            if type(n) is not kind:
                raise Error(f'{self.__class__.__name__} only holds all '
                            'ints or all floats')
            self._items.append(n)
            if len(self._items) > 12:
                raise Error(f'{self.__class__.__name__} may only hold '
                            '2-12 ints or 2-12 floats')


    @property
    def asuxf(self):
        items = ' '.join([str(n) for n in self._items])
        return f'(:{items}:)'


    def __getattr__(self, name):
        if name in {'a', 'x', 'first'}:
            return self._items[0]
        if name in {'b', 'y', 'second'}:
            return self._items[1]
        if name in {'c', 'z', 'third'}:
            return self._items[2]
        if name in {'d', 'fourth'}:
            return self._items[3]
        if name in {'e', 'fifth'}:
            return self._items[4]
        if name in {'f', 'sixth'}:
            return self._items[5]
        if name in {'g', 'seventh'}:
            return self._items[6]
        if name in {'h', 'eighth'}:
            return self._items[7]
        if name in {'i', 'ninth'}:
            return self._items[8]
        if name in {'j', 'tenth'}:
            return self._items[9]
        if name in {'k', 'eleventh'}:
            return self._items[10]
        if name in {'l', 'twelth'}:
            return self._items[11]
        if len(self._items) == 2:
            if name == 'real':
                return self._items[0]
            elif name in {'imag', 'imaginary'}:
                return self._items[1]
        raise AttributeError(f'{self.__class__.__name__!r} object has '
                             f'no attribute {name!r}')


    def __getitem__(self, index):
        return self._items[index]


    def __repr__(self):
        items = ', '.join([str(n) for n in self._items])
        return f'{self.__class__.__name__}({items})'


    def __len__(self):
        return len(self._items)


class Table:
    '''Used to store a UXF table.

    A uxf.Table has a list of fieldnames and a records list which is a
    lists of lists with each sublist having the same number of items as
    the number of fieldnames.

    When a uxf.Table is iterated each row is returned as a namedtuple.
    '''

    def __init__(self, *, name=None, fieldnames=None, records=None):
        '''
        A Table may be created empty, e.g., Table(). However, if records is
        not None, then both name and fieldnames must be given.

        records can be a flat list of values (which will be put into a list
        of lists with each sublist being len(fieldnames) long), or a list of
        lists in which case each list is _assumed_ to be len(fieldnames)
        long.
        '''
        self.name = name
        self._Class = None
        self.fieldnames = [] if fieldnames is None else fieldnames
        self.records = []
        if records:
            if not name:
                raise Error('can\'t create an unnamed nonempty table')
            if not fieldnames:
                raise Error(
                    'can\'t create a nonempty table without field names')
            if isinstance(records, list):
                if self._Class is None:
                    self._make_class()
                self.records = records
            else:
                for value in records:
                    self.append(value)


    def append_fieldname(self, name):
        self.fieldnames.append(name)


    def append(self, value):
        if self._Class is None:
            self._make_class()
        if (not self.records or
                len(self.records[-1]) >= len(self.fieldnames)):
            self.records.append([])
        self.records[-1].append(value)


    def _make_class(self):
        if not self.name:
            raise Error('can\'t use an unnamed table')
        if not self.fieldnames:
            raise Error('can\'t create a table with no field names')
        self._Class = collections.namedtuple(
            _canonicalize(self.name, 'Table'),
            [_canonicalize(name, f'Field{i}')
             for i, name in enumerate(self.fieldnames, 1)])


    def __iadd__(self, value):
        if not self.name:
            raise Error('can\'t append to an unnamed table')
        if not self.fieldnames:
            raise Error('can\'t append to a table with no field names')
        if isinstance(value, (list, tuple)): # or: collections.abc.Sequence?
            for v in value:
                self.append(v)
        else:
            self.append(value)
        return self


    def __iter__(self):
        if self._Class is None:
            self._make_class()
        for record in self.records:
            yield self._Class(*record)


    def __len__(self):
        return len(self.records)


    def __str__(self):
        return (f'Table {self.name!r} {self.fieldnames!r} with '
                f'{len(self.records)} records')


    def __repr__(self):
        return (f'{self.__class__.__name__}(name={self.name!r}, '
                f'fieldnames={self.fieldnames!r}, '
                f'records={self.records!r})')


def _canonicalize(s, prefix):
    s = re.sub(r'\W+', '', s)
    if not s:
        s = f'{prefix}{id(s):X}'
    elif not s.isalpha():
        s = prefix + s
    return s


def _parse(tokens, *, text, warn_is_error=False):
    parser = _Parser()
    return parser.parse(tokens, text)


class _Parser(_ErrorMixin):

    def __init__(self, *, warn_is_error=False):
        self.warn_is_error = warn_is_error
        self._what = 'parser'


    def clear(self):
        self.keys = []
        self.stack = []
        self.pos = -1
        self.states = [_Expect.COLLECTION]


    def parse(self, tokens, text):
        self.clear()
        self.tokens = tokens
        self.text = text
        data = None
        for token in tokens:
            if token.kind is _Kind.EOF:
                break
            self.pos = token.pos
            state = self.states[-1]
            if state is _Expect.COLLECTION:
                if not self._is_collection_start(token.kind):
                    self.error(f'expected dict (UXF map), list, or '
                               f'uxf.Table, got {token}')
                self.states.pop() # _Expect.COLLECTION
                self._on_collection_start(token.kind)
                data = self.stack[0]
            elif state is _Expect.TABLE_NAME:
                self._handle_table_name(token)
            elif state is _Expect.TABLE_FIELD_NAME:
                self._handle_field_name(token)
            elif state is _Expect.TABLE_VALUE:
                self._handle_table_value(token)
            elif state is _Expect.DICT_KEY:
                self._handle_map_key(token)
            elif state is _Expect.DICT_VALUE:
                self._handle_map_value(token)
            elif state is _Expect.EOF:
                if token.kind is not _Kind.EOF:
                    self.error(f'expected EOF, got {token}')
                break # should be redundant
            elif state is _Expect.ANY_VALUE:
                if token.kind is not _Kind.EOF:
                    self._handle_any_value(token)
        return data


    def _is_collection_start(self, kind):
        return kind in {_Kind.DICT_BEGIN, _Kind.LIST_BEGIN,
                        _Kind.TABLE_BEGIN}


    def _is_collection_end(self, kind):
        return kind in {_Kind.DICT_END, _Kind.LIST_END,
                        _Kind.TABLE_END}


    def _on_collection_start(self, kind):
        if kind is _Kind.DICT_BEGIN:
            self.states.append(_Expect.DICT_KEY)
            self._on_collection_start_helper(dict)
        elif kind is _Kind.LIST_BEGIN:
            self.states.append(_Expect.ANY_VALUE)
            self._on_collection_start_helper(list)
        elif kind is _Kind.TABLE_BEGIN:
            self.states.append(_Expect.TABLE_NAME)
            self._on_collection_start_helper(Table)
        else:
            self.error('expected to create dict (UXF map), list, or '
                       f'uxf.Table, not {kind}')


    def _on_collection_start_helper(self, Class):
        if self.stack and isinstance(self.stack[-1], list):
            self.stack[-1].append(Class())
            self.stack.append(self.stack[-1][-1])
        else:
            self.stack.append(Class())


    def _on_collection_end(self, token):
        self.states.pop()
        self.stack.pop()
        if self.stack:
            if isinstance(self.stack[-1], list):
                self.states.append(_Expect.ANY_VALUE)
            elif isinstance(self.stack[-1], dict):
                self.states.append(_Expect.DICT_KEY)
            elif isinstance(self.stack[-1], Table):
                self.states.append(_Expect.TABLE_VALUE)
            else:
                self.error(f'unexpected token, {token}')
        else:
            self.states.append(_Expect.EOF)


    def _handle_table_name(self, token):
        if token.kind is not _Kind.TABLE_NAME:
            self.error(f'expected table name, got {token}')
        self.stack[-1].name = token.value
        self.states[-1] = _Expect.TABLE_FIELD_NAME


    def _handle_field_name(self, token):
        if token.kind is _Kind.TABLE_ROWS:
            self.states[-1] = _Expect.TABLE_VALUE
        else:
            if token.kind is not _Kind.TABLE_FIELD_NAME:
                self.error(f'expected table field name, got {token}')
            self.stack[-1].append_fieldname(token.value)


    def _handle_table_value(self, token):
        if token.kind is _Kind.TABLE_END:
            self._on_collection_end(token)
        elif token.kind in {
                _Kind.NULL, _Kind.BOOL, _Kind.INT,
                _Kind.REAL, _Kind.DATE, _Kind.DATE_TIME,
                _Kind.STR, _Kind.BYTES}:
            self.stack[-1] += token.value
        else:
            self.error('table values may only be null, bool, int, real, '
                       f'date, datetime, str, or bytes, got {token}')


    def _handle_map_key(self, token):
        if token.kind is _Kind.DICT_END:
            self._on_collection_end(token)
        elif token.kind in {
                _Kind.INT, _Kind.DATE, _Kind.DATE_TIME,
                _Kind.STR, _Kind.BYTES}:
            self.keys.append(token.value)
            self.states[-1] = _Expect.DICT_VALUE
        else:
            self.error('dict (UXF map) keys may only be int, date, '
                       f'datetime, str, or bytes, got {token}')


    def _handle_map_value(self, token):
        if self._is_collection_start(token.kind):
            # this adds a new list, map, or table to the stack
            self._on_collection_start(token.kind)
            # this adds a key-value item to the map that contains the above
            # list, map, or table, the key being the key acquired earlier,
            # the value being the new list, map, or table
            self.stack[-2][self.keys[-1]] = self.stack[-1]
        elif self._is_collection_end(token.kind):
            self.states[-1] = _Expect.DICT_KEY
            self.stack.pop()
            if self.stack and isinstance(self.stack[-1], dict):
                self.keys.pop()
        else: # a scalar
            self.states[-1] = _Expect.DICT_KEY
            self.stack[-1][self.keys.pop()] = token.value


    def _handle_any_value(self, token):
        if self._is_collection_start(token.kind):
            # this adds a new list, map, or table to the stack
            self._on_collection_start(token.kind)
        elif self._is_collection_end(token.kind):
            self.states.pop()
            if self.states and self.states[-1] is _Expect.DICT_VALUE:
                self.states[-1] = _Expect.DICT_KEY
            self.stack.pop()
        else: # a scalar
            self.stack[-1].append(token.value)


@enum.unique
class _Expect(enum.Enum):
    COLLECTION = enum.auto()
    DICT_KEY = enum.auto()
    DICT_VALUE = enum.auto()
    ANY_VALUE = enum.auto()
    TABLE_NAME = enum.auto()
    TABLE_FIELD_NAME = enum.auto()
    TABLE_VALUE = enum.auto()
    EOF = enum.auto()


def write(filename_or_filelike, *, data, custom='', compress=False,
          indent=2, one_way_conversion=False):
    '''
    filename_or_filelike is sys.stdout or a filename or an open writable
    file (text mode UTF-8 encoded).

    data is a list, dict (i.e., UXF map), or uxf.Table that this function
    will write to the filename_or_filelike in UXF format.

    custom is an optional short user string (with no newlines), e.g., a file
    type description.

    If compress is True and the filename_or_filelike is a file (not stdout)
    then gzip compression is used.

    Set indent to 0 to minimize the file size.

    Set one_way_conversion to True to convert bytearray items to bytes,
    complex items to uxf.NTuples, and sets, frozensets, tuples, and
    collections.deques to lists rather than raise an Error.
    '''
    pad = ' ' * indent
    close = False
    if isinstance(filename_or_filelike, str):
        opener = gzip.open if compress else open
        file = opener(filename_or_filelike, 'wt', encoding=UTF8)
        close = True
    else:
        file = filename_or_filelike
    try:
        _Writer(file, custom, data, pad, one_way_conversion)
    finally:
        if close:
            file.close()


class _Writer:

    def __init__(self, file, custom, data, pad, one_way_conversion):
        self.file = file
        self.one_way_conversion = one_way_conversion
        self.write_header(custom)
        self.write_value(data, pad=pad)


    def write_header(self, custom):
        self.file.write(f'uxf {VERSION}')
        if custom:
            self.file.write(f' {custom}')
        self.file.write('\n')


    def write_value(self, item, indent=0, *, pad, map_value=False):
        if isinstance(item, (set, frozenset, tuple, collections.deque)):
            if self.one_way_conversion:
                item = list(item)
            else:
                raise Error(f'can only convert {type(item)} to list if '
                            'one_way_conversion is True')
        if isinstance(item, list):
            return self.write_list(item, indent, pad=pad,
                                   map_value=map_value)
        if isinstance(item, dict):
            return self.write_map(item, indent, pad=pad,
                                  map_value=map_value)
        if isinstance(item, Table):
            return self.write_table(item, indent, pad=pad,
                                    map_value=map_value)
        return self.write_scalar(item, indent=indent, pad=pad,
                                 map_value=map_value)


    def write_list(self, item, indent=0, *, pad, map_value=False):
        tab = '' if map_value else pad * indent
        if len(item) == 0:
            self.file.write(f'{tab}[]\n')
        else:
            self.file.write(f'{tab}[')
            indent += 1
            is_scalar = _is_scalar(item[0])
            if is_scalar:
                kwargs = dict(indent=0, pad=' ', map_value=False)
            else:
                self.file.write('\n')
                kwargs = dict(indent=indent, pad=pad, map_value=False)
            for value in item:
                self.write_value(value, **kwargs)
                if is_scalar:
                    kwargs['indent'] = 1 # 0 for first item
            tab = pad * (indent - 1)
            self.file.write(']\n' if is_scalar else f'{tab}]\n')
        return True


    def write_map(self, item, indent=0, *, pad, map_value=False):
        tab = '' if map_value else pad * indent
        if len(item) == 0:
            self.file.write(f'{tab}{{}}\n')
        elif len(item) == 1:
            self.file.write(f'{tab}{{')
            key, value = list(item.items())[0]
            self.write_scalar(key, 1, pad=' ')
            self.file.write(' ')
            self.write_value(value, 1, pad=' ', map_value=True)
            self.file.write('}\n')
        else:
            self.file.write(f'{tab}{{\n')
            indent += 1
            for key, value in item.items():
                self.write_scalar(key, indent, pad=pad)
                self.file.write(' ')
                if not self.write_value(value, indent, pad=pad,
                                        map_value=True):
                    self.file.write('\n')
            tab = pad * (indent - 1)
            self.file.write(f'{tab}}}\n')
        return True


    def write_table(self, item, indent=0, *, pad, map_value=False):
        tab = '' if map_value else pad * indent
        self.file.write(f'{tab}[= <{escape(item.name)}>')
        for name in item.fieldnames:
            self.file.write(f' <{escape(name)}>')
        if len(item) == 0:
            self.file.write(' = =]\n')
        else:
            self.file.write(' =\n')
            indent += 1
            for record in item:
                self.file.write(pad * indent)
                sep = ''
                for value in record:
                    self.file.write(sep)
                    self.write_scalar(value, pad=pad)
                    sep = ' '
                self.file.write('\n')
            tab = pad * (indent - 1)
            self.file.write(f'{tab}=]\n')
        return True


    def write_scalar(self, item, indent=0, *, pad, map_value=False):
        if not map_value:
            self.file.write(pad * indent)
        if item is None:
            self.file.write('null')
        elif isinstance(item, bool):
            self.file.write('yes' if item else 'no')
        elif isinstance(item, int):
            self.file.write(str(item))
        elif isinstance(item, float):
            self.file.write(_realstr(item))
        elif isinstance(item, (datetime.date, datetime.datetime)):
            self.file.write(item.isoformat())
        elif isinstance(item, str):
            self.file.write(f'<{escape(item)}>')
        elif isinstance(item, bytes):
            self.file.write(f'({item.hex().upper()})')
        elif isinstance(item, bytearray):
            if not self.one_way_conversion:
                raise Error('can only convert bytearray to bytes if '
                            'one_way_conversion is True')
            self.file.write(f'({item.hex().upper()})')
        elif isinstance(item, complex):
            if not self.one_way_conversion:
                raise Error('can only convert complex to ntuple if '
                            'one_way_conversion is True')
            self.file.write(
                f'(:{_realstr(item.real)} {_realstr(item.imag)}:)')
        elif isinstance(item, NTuple):
            self.file.write(item.asuxf)
        else:
            print(f'error: ignoring unexpected item of type {type(item)}: '
                  f'{item!r}', file=sys.stderr)
        return False


def _realstr(s):
    value = str(s)
    if '.' not in value:
        i = value.find('e')
        if i == -1:
            i = value.find('E')
        if i == -1:
            value += '.0'
        else:
            value = value[:i] + '.0' + value[i:]
    return value


def _is_scalar(x):
    return x is None or isinstance(
        x, (bool, int, float, datetime.date, datetime.datetime, str, bytes,
            bytearray))


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in {'-h', '--help', 'help'}:
        raise SystemExit('''\
usage: uxf.py [-z|--compress] [-iN|--indent=N] <infile.uxf> [<outfile.uxf>]
   or: python3 -m uxf ...same options as above...

gzip compression is ignored if no outfile (i.e., for stdout).
indent defaults to 2 (range 0-8) e.g., -i0 or --indent=0 (with no space)

To uncompress a .uxf file run: uxf.py infile.uxf outfile.uxf

To compress and minimize a .uxf file run: uxf.py -i0 -z infile.uxf outfile.uxf
''')
    compress = False
    indent = 2
    args = sys.argv[1:]
    infile = outfile = None
    for arg in args:
        if arg in {'-z', '--compress'}:
            compress = True
        elif arg.startswith(('-i', '--indent=')):
            if arg[1] == 'i':
                indent = int(arg[2:])
            else:
                indent = int(arg[9:])
            if not 0 <= indent <= 9:
                indent = 2
        elif infile is None:
            infile = arg
        else:
            outfile = arg
    try:
        data, custom = read(infile)
        outfile = sys.stdout if outfile is None else outfile
        write(outfile, data=data, custom=custom, compress=compress,
              indent=indent)
    except Error as err:
        print(f'Error:{err}')
