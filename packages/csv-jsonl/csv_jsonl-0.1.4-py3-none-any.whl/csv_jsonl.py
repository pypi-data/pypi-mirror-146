"""
Add ``DictWriter`` style class using bits of the built-in ``csv`` module to
handle writing ``jsonl`` files as defined at jsonlines.org.
"""

import csv
import json
import dataclasses
from typing import Mapping, Iterable, Any, TextIO, Union

class JSONLinesWriter:
    """
    Dump json-encoded dictionaries to file in ``jsonl`` format.
    """

    def __init__(self, _fh: TextIO):
        """
        Args:
            f (TextIO): File-like object.
        """
        self._fh = _fh


    def writerow(self, rowdict: Mapping[str, Union[str, int, float, bool]]):
        """
        Write a dictionary as a ``utf-8`` encoded string.
        Test for encoding.

        The ``jsonlines`` format allows for anything ``json`` will allow, so
        we comply.

        Args:
            rowdict (Mapping[str, Any]): dictionary with string values, su
        """

        # The most common values will be objects or arrays, but any JSON value
        # is permitted.
        row = json.dumps(rowdict)

        # JSON allows encoding Unicode strings with only ASCII escape sequences,
        # however those escapes will be hard to read when viewed in a text
        # editor. The author of the JSON Lines file may choose to escape
        # characters to work with plain ASCII files.

        # Encodings other than UTF-8 are very unlikely to be valid when decoded
        # as UTF-8 so the chance of accidentally misinterpreting characters in
        # JSON Lines files is low.
        assert bytes(row, "utf-8"), "JSON dictonary must be utf-8."

        # The last character in the file may be a line separator, and it will
        # be treated the same as if there was no line separator present.
        self._fh.write(f"{row}\n")


    def writerows(self, row_iterable: Iterable[Mapping[str, Any]]):
        """
        Write an iterable of dictionary-like objects (with ``__getitem__``)
        as ``\\n``-separated ``json`` objects.

        Args:
            row_iterable(Iterable[Mapping[str, Any]]): List of dictionaries.
        """

        assert iter(row_iterable), "object must be iterable."

        for rowdict in row_iterable:
            self.writerow(rowdict)


class JSONLinesDictWriter(csv.DictWriter):
    """
    Write ``json`` formatted dictionaries, separated by newlines.

    Example
    ::
        >>> from csv_jsonl import JSONLinesDictWriter
        >>> l = [{"foo": "bar", "bat": 1}, {"foo": "bar", "bat": 2}]
        >>> with open("foo.jsonl", "w", encoding="utf-8") as _fh:
        ...     writer = JSONLinesDictWriter(_fh)
        ...     writer.writerows(l)
        ...
        >>> d = {"foo": "bar", "bat": 1}
        >>> with open("bar.jsonl", "w", encoding="utf-8") as _fh:
        ...     writer = JSONLinesDictWriter(_fh)
        ...     writer.writerow(d)
        ...
        >>> from collections import OrderedDict
        >>> od = OrderedDict([('foo', 'bar'), ('bat', 1)])
        >>> with open("qux.jsonl", "w", encoding="utf-8") as _fh:
        ...     writer = JSONLinesDictWriter(_fh)
        ...     writer.writerow(od)
        ...
        >>> fieldnames = ["foo", "bar"] # keys = ["foo", "bat"] expect fail
        >>> with open("baz.jsonl", "w", encoding="utf-8") as _fh:
        ...     writer = JSONLinesDictWriter(_fh, fieldnames=fieldnames)
        ...     writer.writerows(l)
        ...
        Expect ValueError
    """

    def __init__(self, _fh, fieldnames=None, extrasaction="raise"):

        super().__init__(_fh, fieldnames, extrasaction)

        self.fieldnames = fieldnames
        self.extrasaction = extrasaction

        if extrasaction.lower() not in ("raise", "ignore"):
            raise ValueError(
                "extrasaction (%s) must be 'raise' or 'ignore'" % extrasaction
            )

        self.writer = JSONLinesWriter(_fh)


    def _dict_to_list(self, rowdict):
        """
        Keeping the name ``_dict_to_list`` due to laziness. Still optionally
        doing fieldname checks, just passing the dictionary rather than
        returning <dict>.values()
        """

        # Don't confuse json with dictish objects or dataclasses
        if hasattr(rowdict, "_asdict"):
            rowdict = dict(rowdict._asdict())

        if dataclasses.is_dataclass(rowdict):
            rowdict = dataclasses.asdict(rowdict)

        if not self.fieldnames:
            self.fieldnames = list(rowdict.keys())

        if self.extrasaction == "raise":

            if self.fieldnames:
                wrong_fields = rowdict.keys() - self.fieldnames
                if wrong_fields:
                    raise ValueError(
                        "dict contains fields not in fieldnames: "
                        + ", ".join([repr(x) for x in wrong_fields])
                    )

        return rowdict

    def writeheader(self):
        raise NotImplementedError("Use JSONLinesListWriter")


class JSONLinesListWriter(csv.DictWriter):

    """
    Write a list of lists. Optionally supply header.

    Example
    ::
        >>> from csv_jsonl import JSONLineslistWriter
        >>> l = zip(["foo", "bar", "bat"], range(3), range(3))
        >>> with open("foo.jsonl", "w", encoding="utf-8") as _fh:
        ...     writer = JSONLinesListWriter(_fh)
        ...     writer.writerows(l)
        ...
        >>> l = zip(["foo", "bar", "bat"], range(3), range(3))
        >>> with open("bar.jsonl", "w", encoding="utf-8") as _fh:
        ...     writer = JSONLinesDictWriter(_fh)
        ...     writer.writerow(next(l))
        ...
        >>> fieldnames = ["baz", "qux", "quux"]
        >>> l = zip(["foo", "bar", "bat"], range(3), range(3))
        >>> with open("foo.jsonl", "w", encoding="utf-8") as _fh:
        ...     writer = JSONLinesListWriter(_fh, fieldnames=fieldnames)
        ...     writer.writeheader()
        ...     writer.writerows(l)
        ...
    """

    def __init__(self, _fh, fieldnames=None, extrasaction="raise"):

        super().__init__(_fh, fieldnames, extrasaction)

        self.fieldnames = fieldnames
        self.extrasaction = extrasaction

        if extrasaction.lower() not in ("raise", "ignore"):
            raise ValueError(
                "extrasaction (%s) must be 'raise' or 'ignore'" % extrasaction
            )

        self.writer = JSONLinesWriter(_fh)


    def _dict_to_list(self, rowlist):
        """
        Again, not renaming because lazy.

        Args:
            rowlist (list): object that can be converted to a list.
        """

        assert list(rowlist), f"{rowlist} is not iterable."

        if self.extrasaction == "raise":

            if self.fieldnames:
                mismatch = len(rowlist) - len(self.fieldnames)
                if mismatch:
                    raise ValueError("Row length != length of fieldnames.")

        return rowlist


    def writeheader(self):
        """
        Write fieldnames as first list
        """

        assert list(self.fieldnames), f"{self.fieldnames} is not iterable."
        self.writer.writerow(self.fieldnames)
