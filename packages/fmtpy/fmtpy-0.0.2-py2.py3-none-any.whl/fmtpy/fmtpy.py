import argparse
import collections
import functools
import importlib
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.syntax import Syntax
from yapf.yapflib.yapf_api import FormatCode


@functools.lru_cache
def get_std_library_names():
    result = requests.get(
        'https://github.com/python/cpython/tree/main/Doc/library')
    soup = BeautifulSoup(result.text, features="lxml")
    rst_files = soup.find_all(title=re.compile(r'\.rst$'))
    names = [i.extract().get_text() for i in rst_files]
    std_lib_names = []
    for name in names:
        if name.endswith('.rst') and not any(x in name for x in [' ', '-']):
            std_lib_names.append(name.split('.')[0])
    return list(set(std_lib_names))


def sort_imports(file_path, only_imports=False):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    imports = collections.defaultdict(list)
    non_imports = []
    top_lines = []
    std_lib_names = get_std_library_names()

    for line in lines:
        if (line.startswith('#!')
                and 'python' in line) or (line.startswith('#')
                                          and 'coding:' in line):
            if not only_imports:
                top_lines.append(line)
            continue
        if line.startswith('import '):
            module_name = line.split('import ')[1].strip().replace('\n', '')
        elif line.startswith('from ') and ' import ' in line:
            module_name = line.split('from')[1].split('import')[0].strip()
        else:
            if not only_imports:
                non_imports.append(line)
            continue

        spec = importlib.util.find_spec(module_name)
        if spec:
            if module_name in std_lib_names:
                if line.startswith('import '):
                    imports['std_lib_imports'].append(line)
                else:
                    imports['partial_std_lib_imports'].append(line)
            else:
                if Path(spec.loader.path).parent == Path(
                        Path(file_path).absolute()).parent:
                    if line.startswith('import '):
                        imports['relative_imports'].append(line)
                    elif line.startswith('from ') and ' import ' in line:
                        imports['partial_relative_imports'].append(line)
                else:
                    if line.startswith('import '):
                        imports['external_imports'].append(line)
                    elif line.startswith('from ') and ' import ' in line:
                        imports['partial_external_imports'].append(line)

    order = [
        'std_lib_imports', 'partial_std_lib_imports', 'external_imports',
        'partial_external_imports', 'relative_imports',
        'partial_relative_imports'
    ]
    imports_sorted = {k: sorted(list(set(imports[k]))) for k in order}
    vals = list(imports_sorted.values())
    
    out_file = []
    if not only_imports:
        out_file.append(top_lines + ['\n'])
    out_file.append(sum(vals[:2], []) + ['\n'])
    out_file.append(sum(vals[2:4], []) + ['\n'])
    out_file.append(sum(vals[4:], []) + ['\n'])
    if not only_imports:
        out_file.append(non_imports)
    return sum(out_file, [])


def opts():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s',
                        '--style',
                        type=str,
                        choices=['pep8', 'google', 'yapf', 'facebook'],
                        default='pep8',
                        help='Formatting style')
    parser.add_argument('-i',
                        '--in-place',
                        help='Make changes in-place',
                        action='store_true')
    parser.add_argument('-o',
                        '--only-imports',
                        help='Only return sorted import statements',
                        action='store_true')
    parser.add_argument('-n',
                        '--show-line-numbers',
                        help='Render a column for line numbers',
                        action='store_true')
    parser.add_argument('files', nargs='+', help='files to format')

    return parser.parse_args()


def main(file_path, only_imports, in_place, show_line_numbers, style, *args,
         **kwargs):
    out_file = sort_imports(file_path, only_imports)
    reformatted_code, _ = FormatCode(''.join(out_file), style_config=style)

    if in_place and only_imports:
        raise TypeError(
            'Can\'t use `--only-imports` and `--in-place` together!')
    if in_place:
        with open(file_path, 'w') as f:
            f.writelines(reformatted_code)
    else:
        console = Console()
        console.print(
            Syntax(reformatted_code,
                   'python',
                   line_numbers=show_line_numbers,
                   theme='dracula'))


if __name__ == '__main__':
    args = opts()
    for file in args.files:
        main(file, **vars(args))
