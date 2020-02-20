from __future__ import print_function
import io
import sys

if sys.version_info < (3, 0):
    import codecs
    # Use UTF8 reader/writer for stdin/stdout
    # http://stackoverflow.com/a/1169209
    input_stream = codecs.getreader('utf8')(sys.stdin)
    output_stream = codecs.getwriter('utf8')(sys.stdout)
else:
    # Wrap input/output stream in UTF-8 encoded text wrapper
    # https://stackoverflow.com/a/16549381
    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    output_stream = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

__version__ = '0.2.8'

try:
    # Jupyter >= 4
    from nbformat import read, write, NO_CONVERT
except ImportError:
    # IPython 3
    try:
        from IPython.nbformat import read, write, NO_CONVERT
    except ImportError:
        # IPython < 3
        from IPython.nbformat import current

        def read(f, as_version):
            return current.read(f, 'json')

        def write(nb, f):
            return current.write(nb, f, 'json')


def _cells(nb):
    """Yield all cells in an nbformat-insensitive manner"""
    if nb.nbformat < 4:
        for ws in nb.worksheets:
            for cell in ws.cells:
                yield cell
    else:
        for cell in nb.cells:
            yield cell


def strip(nb):
    """strip the outputs from a notebook object"""
    nb.metadata.pop('signature', None)
    for cell in _cells(nb):
        if (cell.metadata.get('init_cell') or cell.metadata.get('keep_output')):
            # Leave these cells alone
            continue
        if 'outputs' in cell:
            cell['outputs'] = []
        if 'prompt_number' in cell:
            cell['prompt_number'] = None
        if 'execution_count' in cell:
            cell['execution_count'] = None
        for output_style in ['collapsed', 'scrolled']:
            if output_style in cell.metadata:
                cell.metadata[output_style] = False
    return nb

def strip_output(ASSIGNMENT):
    try:
        with io.open(ASSIGNMENT, 'r', encoding='utf8') as f:
            nb = read(f, as_version=NO_CONVERT)
        nb = strip(nb)
        with io.open(ASSIGNMENT, 'w', encoding='utf8') as f:
            write(nb, f)
    except Exception:
        # Ignore exceptions for non-notebook files.
        print("Could not strip '{}'".format(ASSIGNMENT))
        raise
