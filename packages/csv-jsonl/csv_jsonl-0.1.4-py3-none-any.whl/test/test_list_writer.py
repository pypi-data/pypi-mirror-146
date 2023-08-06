from pathlib import Path
import tempfile

import pytest

from csv_jsonl import JSONLinesListWriter

def list_gen():
    for foo in zip(["foo", "bar", "bat"], range(3), range(3)):
        yield foo

def _writerow(data):
    with tempfile.TemporaryDirectory() as tempdir:
        with open(Path(tempdir, "foo.jsonl"), "w", encoding="utf-8") as _fh:
            writer = JSONLinesListWriter(_fh)
            writer.writerow(data[0])

def _writerows(data):
    with tempfile.TemporaryDirectory() as tempdir:
        with open(Path(tempdir, "foo.jsonl"), "w", encoding="utf-8") as _fh:
            writer = JSONLinesListWriter(_fh)
            writer.writerows(data)

def _writerows_fieldnames(data, fieldnames):
    with tempfile.TemporaryDirectory() as tempdir:
        with open(Path(tempdir, "foo.jsonl"), "w", encoding="utf-8") as _fh:
            writer = JSONLinesListWriter(_fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

def test_writerow():
    assert _writerow(next(list_gen())) == None

def test_writerows():
    assert _writerows(list_gen()) == None

def test_writerows_fieldnames():
    assert _writerows_fieldnames(list_gen(), ["foo", "bar", "bat"]) == None

def test_writerow_string():
    "I'll let you, man, but you don't wanna."
    assert _writerow("foobarbat baz") == None
