#!/usr/bin/python

import types

class FilterModule(object):
    def filters(self):
        return {
            'list_append': self.list_append
        }

    def enum_items(self, values):
        if isinstance(values, types.StringTypes):
            yield values
        else:
            try:
                for v in values:
                    yield v
            except TypeError:
                yield values

    def list_append(self, values, exts):
        return [[x, y] for x in self.enum_items(values) for y in self.enum_items(exts)]

