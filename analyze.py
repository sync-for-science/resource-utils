import argparse
from collections import Counter
from collections.abc import Mapping, Sequence
from functools import total_ordering
from pprint import pprint
import sys

import msgpack


EMPTY = object()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', required=True)
    parser.add_argument('-p', '--path', default='')
    parser.add_argument('-a', '--aggregate')

    args = parser.parse_args()
    args.path = args.path.split('.') if args.path else list()
    return args


@total_ordering
class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

    def __lt__(self, other):
        return sorted(self.items()) < sorted(other.items())

    def __repr__(self):
        contents = ', '.join(f'{k!r}: {v!r}' for k, v in sorted(self.items()))
        return '{' + contents + '}'


def freeze(obj):
    if isinstance(obj, list):
        return tuple(freeze(x) for x in obj)
    if isinstance(obj, dict):
        return HashableDict((k, freeze(v)) for k, v in obj.items())
    return obj


class Observer:
    def __init__(self, aggregate=None):
        self._counter = Counter()
        self._total = 0
        self._aggregate = aggregate

    def __call__(self, data):
        if self._aggregate:
            data = {x[self._aggregate] for x in freeze(data) if self._aggregate in x}
        elif isinstance(data, Sequence) and not isinstance(data, (str, bytes)):
            for x in data:
                self(x)
            return
        elif isinstance(data, Mapping):
            data = data.keys()

        self._counter.update(data)

        self._total += 1

    def print_results(self):
        print('Required:')
        for prop, count in sorted((prop, count) for prop, count in self._counter.items() if count == self._total):
            print(f' - {prop} ({count})')
        print('Optional:')
        for prop, count in sorted((prop, count) for prop, count in self._counter.items() if count < self._total):
            print(f' - {prop} ({count})')


def traverse(obj, path):
    if not path:
        yield obj
    elif isinstance(obj, Sequence) and not isinstance(obj, (str, bytes)):
        for subobj in obj:
            yield from traverse(subobj, path)
    elif isinstance(obj, Mapping) and path[0] in obj:
        yield from traverse(obj[path[0]], path[1:])


def get_objs(d, path):
    with open(f'{d}/resources.pck', 'rb') as f:
        for resource in msgpack.Unpacker(f, raw=False):
            yield from traverse(resource, path)


if __name__ == '__main__':
    args = parse_args()
    o = Observer(args.aggregate)
    for obj in get_objs(args.dir, args.path):
        try:
            o(obj)
        except:
            pprint(obj)
            raise
    o.print_results()
