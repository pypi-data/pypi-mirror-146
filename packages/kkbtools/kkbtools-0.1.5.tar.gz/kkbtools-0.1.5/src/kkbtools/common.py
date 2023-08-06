import os
import sys
from rich.console import Console
import os
import sys

from rich.console import Console


def usage():
    """
    kkb爬虫工具集
    usage: kkba [options]

    optional arguments:
    -h, --help        帮助文档
    -v, --version     查看版本
    """
    console = Console()
    console.print(f'[bold green]{usage.__doc__}[/]', justify='left')
    sys.exit()


def main():
    console = Console()
    args = sys.argv
    try:  # no params
        if args[1] in ("-H", "--help"):
            usage()

        elif args[1] in ("-V", "--version"):
            version_path = os.path.abspath(
                os.path.join(__file__, '../', 'VERSION')
            )
            with open(version_path, 'r') as f:
                version_str = f.read()
                console.print(f'[bold green]{version_str}[/]', justify='left')
            sys.exit()
    except IndexError:
        usage()


if __name__ == '__main__':
    main()
