"""sonusai vars

usage: vars

options:
    -h, --help

List custom SonusAI variables.

"""

from docopt import docopt

import sonusai
from sonusai import mixture
from sonusai.utils import trim_docstring


def main():
    docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    print('Custom SonusAI variables:\n')
    print(f'  ${{default_noise}}: {mixture.default_noise}')
    print(f'  ${{frame_size}}:    {mixture.frame_size}')
    print()


if __name__ == '__main__':
    main()
