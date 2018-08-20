import argparse
from collections import Counter, OrderedDict
from collections.abc import Hashable
from functools import partial
import json
import multiprocessing as mp

import msgpack


class Cardinality:
    def __init__(self):
        self._min = self._max = None

    def update(self, obj):
        if isinstance(obj, dict):
            self._min = self._max = 1
        elif isinstance(obj, list):
            l = len(obj)
            self._min = l if self._min is None else min(l, self._min)
            self._max = l if self._max is None else max(l, self._max)

    def __str__(self):
        return f'{self.min}..{self.max}'

    @property
    def min(self):
        return self._min if self._min is not None else 1

    @property
    def max(self):
        return self._max if self._max is not None else 1


MARKERS = {'system', 'code', 'url'}
class Node:
    def __init__(self):
        self._total = 0
        self._counter = Counter()
        self._cardinalities = dict()
        self._children = dict()
        self._collections = dict()

    def update(self, obj):
        self._total += 1
        self._counter.update(obj.keys())

        for k, v in obj.items():
            child = self._children.setdefault(k, Node())
            if isinstance(v, dict):
                child.update(v)
            if isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        child.update(item)

            card = self._cardinalities.setdefault(k, Cardinality())
            card.update(v)

            if k in MARKERS and isinstance(v, Hashable):
                collection = self._collections.setdefault(k, Counter())
                collection.update((v,))

    def to_dict(self):
        if not self._children:
            return None

        return OrderedDict(
            (k, {
                'stats': {
                    'min': self._cardinalities[k].min,
                    'max': self._cardinalities[k].max,
                    'count': self._counter[k],
                    'total': self._total,
                    'required': self._total == self._counter[k],
                    'collection': self._collections.get(k, dict())
                },
                'props': v.to_dict()
            })
            for k, v in sorted(self._children.items())
        )

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)


def merge_trees(trees):
    all_keys = set()
    for tree in trees.values():
        all_keys.update(tree._children.keys())

    return {
        key: {
            'stats': {
                label: (tree.to_dict() or {}).get(key, dict()).get('stats')
                for label, tree in trees.items()
            },
            'props': merge_trees({
                label: tree._children[key]
                for label, tree in trees.items()
                if key in tree._children
            })
        }        
        for key in sorted(all_keys)
    }
        


def load_resources(name, count=None):
    node = Node()
    with open(f'{name}/resources.pck', 'rb') as f:
        for i, item in enumerate(msgpack.Unpacker(f, raw=False)):
            if count is not None and i >= count:
                break
            node.update(item)
    return node


def main(types, count):
    pool = mp.Pool()
    limited = partial(load_resources, count=count)
    trees = dict(zip(types, pool.map(limited, types)))
    print(json.dumps(merge_trees(trees), indent=2))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('types', nargs='+')
    parser.add_argument('--count', '-c', type=int)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args.types, args.count)
