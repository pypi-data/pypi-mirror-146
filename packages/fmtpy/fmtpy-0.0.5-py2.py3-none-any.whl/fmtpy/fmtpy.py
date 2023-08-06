import argparse
import ast
import collections
import importlib
import json
import re
import sys
import tempfile
from pathlib import Path

import requests
from autoflake import _main
from bs4 import BeautifulSoup
from rich.console import Console
from rich.syntax import Syntax
from yapf.yapflib.yapf_api import FormatCode


def get_std_library_names():
    dotfile = f'{Path().home()}/.fmtpy'
    if Path(dotfile).exists():
        with open(dotfile) as j:
            loaded_dotfile = json.load(j)
            if [*sys.version_info][:3] == loaded_dotfile[0]:
                return loaded_dotfile[1]
    result = requests.get(
        'https://github.com/python/cpython/tree/main/Doc/library')
    soup = BeautifulSoup(result.text, features="lxml")
    rst_files = soup.find_all(title=re.compile(r'\.rst$'))
    names = [i.extract().get_text() for i in rst_files]
    std_lib_names = []
    for name in names:
        if name.endswith('.rst') and not any(x in name for x in [' ', '-']):
            std_lib_names.append(name.split('.')[0])
    std_lib_names_list = list(set(std_lib_names))
    with open(dotfile, 'w') as j:
        json.dump([[*sys.version_info][:3], std_lib_names_list], j)
    return std_lib_names_list


def sort_imports(file_path, only_imports=False, keep_external_unused_imports=False):
    with tempfile.NamedTemporaryFile() as fp:
        with open(file_path, 'rb') as f:
            fp.write(f.read())
        fp.seek(0)
        if keep_external_unused_imports:
            options = ['--in-place', '--ignore-init-module-imports']
        else:
            options = ['--remove-all-unused-imports', '--ignore-init-module-imports', '--in-place']
        _main([None, *options, fp.name],
              standard_out=sys.stdout,
              standard_error=sys.stderr)
        lines = [x.decode() for x in fp.readlines()]

    imports = collections.defaultdict(list)
    non_imports = []
    top_lines = []
    std_lib_names = get_std_library_names()
    imports_start = False

    for line in lines:
        if line.startswith('import '):
            imports_start = True
            module_name = line.split('import ')[1].strip().replace('\n', '')
        elif line.startswith('from ') and ' import ' in line:
            imports_start = True
            module_name = line.split('from')[1].split('import')[0].strip()
        elif not imports_start:
            if not only_imports:
                top_lines.append(line)
            continue
        else:
            if not only_imports:
                non_imports.append(line)
            continue

        if '.' in module_name and 'from .' not in line and 'from .' not in line:
            module_name = module_name.split('.')[0]

        valid_import = isinstance(
            ast.parse(line).body[0], (ast.ImportFrom, ast.Import))

        if valid_import:
            sys.path.insert(0, str(Path(file_path).absolute().parent))
            spec = importlib.util.find_spec(module_name)

            if module_name in std_lib_names:
                if line.startswith('import '):
                    imports['std_lib_imports'].append(line)
                else:
                    imports['partial_std_lib_imports'].append(line)
            else:
                if spec and spec.loader and (Path(spec.loader.path).parent == Path(
                        Path(file_path).absolute()).parent):

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
    parser.add_argument('-k',
                        '--keep-external-unused-imports',
                        help='Keep the import statement of external unused modules',
                        action='store_true')
    parser.add_argument('files', nargs='+', help='files to format')

    return parser.parse_args()


def main(file_path, only_imports, in_place, show_line_numbers, style, keep_external_unused_imports, *args,
         **kwargs):
    out_file = sort_imports(file_path, only_imports, keep_external_unused_imports)
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
