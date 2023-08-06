from .fmtpy import main as _main, opts


def main():
    args = opts()
    for file in args.files:
        _main(file, **vars(args))
