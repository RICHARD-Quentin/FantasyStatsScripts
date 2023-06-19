#!/usr/bin/env python
import sys
from src.utils import init, release, autorelease, check, ligue_stats
import logging
from src.constants import ligues, base_path, args

switch_case = {
    'init': lambda: init(),
    'release': lambda: release(),
    'autorelease': lambda: autorelease(),
    'check': lambda: check(),
}

if __name__ == '__main__':
    logging.basicConfig(filename=f'{base_path}/fantasy.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.DEBUG)
    case = sys.argv[1]
    if case not in args and case not in ligues:
        print(f'Usage: {sys.argv[0]} {"|".join(args)}|{"|".join(ligues)}')
        sys.exit(1)

    if case in ligues:
        ligue_stats()

    if case in args:
        switch_case[case]()