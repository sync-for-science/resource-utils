import glob
import json
import sys

import msgpack
from tqdm import tqdm


def main(d):
    resources = glob.glob(f'{d}/*.json')
    with open(f'{d}/resources.pck', 'wb') as f_out:
        for path in tqdm(resources):
            with open(path) as f_in:
                data = json.load(f_in)
            f_out.write(msgpack.packb(data))


if __name__ == '__main__':
    main(sys.argv[1])
