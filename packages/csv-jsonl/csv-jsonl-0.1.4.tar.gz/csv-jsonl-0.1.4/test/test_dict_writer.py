from collections import OrderedDict
from collections import namedtuple
from dataclasses import dataclass
from pathlib import Path
import tempfile

import pytest


from csv_jsonl import JSONLinesDictWriter

LOD = [{"foo": "bar", "bat": 1}, {"foo": "bar", "bat": 2}]
LOOD = [OrderedDict([('foo', 'bar'), ('bat', 1)]), OrderedDict([('foo', 'bar'), ('bat', 2)])]

def lood_gen():
    for _ in LOOD:
        yield _

def named_tuple_gen():
    Foo = namedtuple("test", "foo, bar, bat")
    for a, b, c in zip(["a", "b", "c"], range(3), range(3)):
        yield Foo(a, b, c)

def dataclass_gen():

    @dataclass
    class DCTest:
        foo: str
        bar: int

    for foo, bar in zip(["foo", "bar"], range(2)):
        yield DCTest(foo, bar)

def _writerow(data):
    with tempfile.TemporaryDirectory() as tempdir:
        with open(Path(tempdir, "foo.jsonl"), "w", encoding="utf-8") as _fh:
            writer = JSONLinesDictWriter(_fh)
            writer.writerow(data[0])

def _writerows(data):
    with tempfile.TemporaryDirectory() as tempdir:
        with open(Path(tempdir, "foo.jsonl"), "w", encoding="utf-8") as _fh:
            writer = JSONLinesDictWriter(_fh)
            writer.writerows(data)

def _writerows_fieldnames(data, fieldnames):
    with tempfile.TemporaryDirectory() as tempdir:
        with open(Path(tempdir, "foo.jsonl"), "w", encoding="utf-8") as _fh:
            writer = JSONLinesDictWriter(_fh, fieldnames=fieldnames)
            writer.writerows(data)

def test_writerow():
    assert _writerow(LOD) == None

def test_writerows():
    assert _writerows(LOD) == None

def test_writerows_ordered_dict():
    assert _writerows(LOOD) == None

def test_writerows_fieldnames():
    assert _writerows_fieldnames(LOD, fieldnames = list(LOD[0].keys())) == None

def test_writerows_fieldnames_bad():
    error_string = "dict contains fields not in fieldnames: 'bat'"
    with pytest.raises(ValueError, match = error_string):
        _writerows_fieldnames(LOD, fieldnames = ["foo", "bar",])

def test_writerows_with_writeheader():
    error_string = "Use JSONLinesListWriter"
    with pytest.raises(NotImplementedError, match = error_string):
        with tempfile.TemporaryDirectory() as tempdir:
            with open(Path(tempdir, "foo.jsonl"), "w", encoding="utf-8") as _fh:
                writer = JSONLinesDictWriter(_fh, fieldnames=["foo", "bar"])
                writer.writeheader()

def test_writerows_list_of_tuples():
    error_string = "'tuple' object has no attribute 'keys'"
    with pytest.raises(AttributeError, match = error_string):
        with tempfile.TemporaryDirectory() as tempdir:
            with open(Path(tempdir, "foo.jsonl"), "w", encoding="utf-8") as _fh:
                writer = JSONLinesDictWriter(_fh)
                _writerows([("foo", "bar", 123)])

def test_writerows_list_of_tuples_fieldnames():
    error_string = "'tuple' object has no attribute 'keys'"
    with pytest.raises(AttributeError, match = error_string):
        with tempfile.TemporaryDirectory() as tempdir:
            with open(Path(tempdir, "foo.jsonl"), "w", encoding="utf-8") as _fh:
                writer = JSONLinesDictWriter(_fh, fieldnames = ["foo", "bar", "bat"])
                _writerows([("foo", "bar", 123)])


def test_non_dict_iterables():
    error_string = "'int' object has no attribute 'keys'"
    with pytest.raises(AttributeError, match = error_string):
        _writerows(range(10))

def test_writerows_newlines_in_values():
    annoyance = [
        {"foo": "bar", "bat": "qux\nuux"},
        {"foo": "bar", "bat": "qux\r\nquux"},
    ]
    assert _writerow(annoyance) == None

def test_writerows_ordered_dict_from_generator():
    assert _writerows(lood_gen()) == None

def test_writerows_dataclass_from_generator():
    assert _writerows(dataclass_gen()) == None

def test_writerows_dataclass_from_generator_with_fieldnames():
    assert _writerows_fieldnames(dataclass_gen(), fieldnames = ["foo", "bar"]) == None

def test_writerows_named_tuple_from_generator():
    assert _writerows(named_tuple_gen()) == None

def test_writerows_named_tuple_from_generator_with_fieldnames():
    assert _writerows_fieldnames(named_tuple_gen(), fieldnames = ["foo", "bar", "bat"]) == None


