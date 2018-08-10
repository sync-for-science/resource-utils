from collections.abc import Sequence, Mapping
from functools import total_ordering
from itertools import groupby
from operator import itemgetter
import sys

import msgpack


@total_ordering
class SortableNoneType:
    def __le__(self, other):
        return True

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return 'None'


SortableNone = SortableNoneType()


def partition(iterable):
    for g, items in groupby(iterable, itemgetter(0)):
        yield g, (item[1:] for item in items)


def search(obj, search_term, companion_term, path=''):
    if isinstance(obj, Sequence) and not isinstance(obj, (str, bytes)):
        for sub in obj:
            yield from search(sub, search_term, companion_term, path)
    elif isinstance(obj, Mapping):
        if search_term in obj:
            yield path, obj[search_term], obj.get(companion_term, SortableNone)
        for k, v in obj.items():
            if path:
                new_path = f'{path}.{k}'
            else:
                new_path = k
            yield from search(v, search_term, companion_term, new_path)
    else:
        pass


if __name__ == '__main__':
    result = set()
    with open(f'{sys.argv[3]}/resources.pck', 'rb') as f:
        for resource in msgpack.Unpacker(f, raw=False):
            result.update(search(resource, sys.argv[1], sys.argv[2]))

    for path, items in partition(sorted(result)):
        print(path)
        for system, codes in partition(items):
            print(f' - {system}')
            codes = list(codes)
            if len(codes) > 10:
                print('   * [more than 10 unique codes]')
            else:
                for code in codes:
                    print(f'   * {code[0]}')
