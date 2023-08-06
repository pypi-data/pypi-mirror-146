
"""Package up pure python version of `rolling_checksum_mod` module."""

import os
import sys
import subprocess

from setuptools import setup

version = '1.0.1'


def is_newer(filename1, filename2):
    """Return True if filename1 is newer than filename2."""
    time1 = os.stat(filename1).st_mtime
    time2 = os.stat(filename2).st_mtime

    if time1 > time2:
        return True
    else:
        return False


def m4_it(infilename, outfilename, define):
    """
    Create outfilename from infilename in a make-like manner.

    If outfilename doesn't exit, create it using m4.
    If outfilename exists but is older than infilename, recreate it using m4.
    """
    build_it = False
    if os.path.exists(outfilename):
        if is_newer(infilename, outfilename):
            # outfilename exists, but is older than infilename, build it
            build_it = True
    else:
        # outfilename does not exist, build it
        build_it = True

    if build_it:
        try:
            subprocess.check_call('m4 -D"%s"=1 < "%s" > "%s"' % (define, infilename, outfilename), shell=True)
        except subprocess.CalledProcessError:
            sys.stderr.write('You need m4 on your path to build this code\n')
            sys.exit(1)


if os.path.exists('../rolling_checksum_mod.m4'):
    m4_it('../rolling_checksum_mod.m4', 'rolling_checksum_py_mod.py', 'py')

setup(
    name='rolling_checksum_py_mod',
    py_modules=[
        'rolling_checksum_mod',
        'rolling_checksum_py_mod',
        ],
    version=version,
    description='Pure Python module providing a variable-length, content-based blocking algorithm',
    long_description="""
Chop a file into variable-length, content-based chunks.

Example use:
.. code-block:: python

    >>> import rolling_checksum_mod
    >>> with open('/tmp/big-file.bin', 'rb') as file_:
    >>>     for chunk in rolling_checksum_mod.min_max_chunker(file_):
    >>>         # chunk is now a piece of the data from file_, and it will not always have the same length.
    >>>         # Instead, it has the property that if you insert a byte at the beginning of /tmp/big-file.bin,
    >>>         # most of the chunks of the file will remain the same.  This can be nice for a deduplicating
    >>>         # backup program.
    >>>         print(len(chunk))
""",
    author='Daniel Richard Stromberg',
    author_email='strombrg@gmail.com',
    url='http://stromberg.dnsalias.org/~dstromberg/rolling_checksum_mod/',
    platforms='Cross platform',
    license='GPLv3',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        ],
    )
