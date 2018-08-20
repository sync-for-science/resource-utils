import json
import sys


INDENT = '  '
def print_tree(data, type_, level=0):
    for k, v in sorted(data.items()):
        stats = v['stats'][type_]
        if not stats or stats['required'] not in (True, False):
            continue

        min_ = stats["min"] if stats["required"] else 0
        print(f'{level*INDENT}* {k} ({min_}..{stats["max"]})')

        subdata = v.get('props')
        if subdata:
            print_tree(subdata, type_, level=level+1)

        collection = stats['collection']
        if 1 <= len(collection) <= 25:  # don't show large collections
            print(f'{(level+1)*INDENT}* possible values:')
            for item in collection:
                print(f'{(level+2)*INDENT}* {item}')


if __name__ == '__main__':
    data = json.load(sys.stdin)
    print_tree(data, sys.argv[1])
